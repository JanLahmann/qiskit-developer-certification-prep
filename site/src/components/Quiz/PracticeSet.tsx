/**
 * PracticeSet — per-section drill embedded in section pages.
 *
 * Loads its section's bank lazily, orders questions by a precomputed
 * "recommended" policy (unseen → previously wrong → weak streak → rest,
 * stable within groups), supports objective/difficulty filters and
 * shuffle. All state client-side; SSR renders a skeleton.
 */

import React, {useEffect, useMemo, useState} from 'react';
import type {BankQuestion, SectionBank, SectionId} from '@site/src/lib/bank';
import {loadSection, mulberry32, seededShuffle} from '@site/src/lib/bank';
import {getProgress} from '@site/src/lib/storage';
import QuizCard from './QuizCard';
import styles from './styles.module.css';

type Order = 'recommended' | 'shuffle' | 'sequential';

function recommendedOrder(questions: BankQuestion[]): BankQuestion[] {
  const prog = getProgress().questions;
  const rank = (q: BankQuestion): number => {
    const st = prog[q.id];
    if (!st || st.a === 0) {
      return 0; // unseen first
    }
    if (!st.r) {
      return 1; // last attempt wrong
    }
    if (st.s < 2) {
      return 2; // shaky streak
    }
    return 3; // mastered-ish last
  };
  return questions
    .map((q, i) => ({q, i, r: rank(q)}))
    .sort((a, b) => a.r - b.r || a.i - b.i)
    .map((x) => x.q);
}

export type PracticeSetProps = {
  section: SectionId;
  /** cap the number of questions shown (0 = all) */
  limit?: number;
};

export default function PracticeSet({
  section,
  limit = 0,
}: PracticeSetProps): React.ReactElement {
  const [bank, setBank] = useState<SectionBank | null>(null);
  const [failed, setFailed] = useState(false);
  const [order, setOrder] = useState<Order>('recommended');
  const [objective, setObjective] = useState<string>('all');
  const [difficulty, setDifficulty] = useState<string>('all');
  const [index, setIndex] = useState(0);
  const [results, setResults] = useState<Record<string, boolean>>({});
  const [epoch, setEpoch] = useState(0); // bump to re-shuffle / restart

  useEffect(() => {
    let alive = true;
    loadSection(section)
      .then((b) => alive && setBank(b))
      .catch(() => alive && setFailed(true));
    return () => {
      alive = false;
    };
  }, [section]);

  const questions = useMemo(() => {
    if (!bank) {
      return [];
    }
    let qs = bank.questions;
    if (objective !== 'all') {
      qs = qs.filter((q) => q.objectives.includes(objective));
    }
    if (difficulty !== 'all') {
      qs = qs.filter((q) => q.difficulty === Number(difficulty));
    }
    if (order === 'recommended') {
      qs = recommendedOrder(qs);
    } else if (order === 'shuffle') {
      qs = seededShuffle(qs, mulberry32(0x51 + epoch));
    }
    if (limit > 0) {
      qs = qs.slice(0, limit);
    }
    return qs;
  }, [bank, order, objective, difficulty, epoch, limit]);

  useEffect(() => {
    setIndex(0);
    setResults({});
  }, [order, objective, difficulty, epoch, section]);

  if (failed) {
    return (
      <div className={styles.emptyState}>
        Could not load this section&apos;s question set.
      </div>
    );
  }
  if (!bank) {
    return <div className={styles.emptyState}>Loading practice set…</div>;
  }
  if (bank.questions.length === 0) {
    return (
      <div className={styles.emptyState}>
        Practice questions for this section are being generated and verified —
        landing soon.
      </div>
    );
  }

  const done = Object.keys(results).length;
  const correct = Object.values(results).filter(Boolean).length;
  const q = questions[Math.min(index, questions.length - 1)];
  const finished = index >= questions.length;

  return (
    <div>
      <div className={styles.setToolbar}>
        <label>
          Order{' '}
          <select value={order} onChange={(e) => setOrder(e.target.value as Order)}>
            <option value="recommended">recommended (weakest first)</option>
            <option value="sequential">sequential</option>
            <option value="shuffle">shuffle</option>
          </select>
        </label>
        <label>
          Objective{' '}
          <select value={objective} onChange={(e) => setObjective(e.target.value)}>
            <option value="all">all</option>
            {bank.section.objectives.map((o) => (
              <option key={o.id} value={o.id}>
                {o.text}
              </option>
            ))}
          </select>
        </label>
        <label>
          Difficulty{' '}
          <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            <option value="all">all</option>
            <option value="1">● easy</option>
            <option value="2">●● medium</option>
            <option value="3">●●● hard</option>
          </select>
        </label>
        <span className={styles.spacer} />
        <span>
          {done}/{questions.length} answered · {correct} correct
        </span>
      </div>

      <div className={styles.setProgress} aria-hidden="true">
        <div
          className={styles.setProgressFill}
          style={{width: `${questions.length ? (done / questions.length) * 100 : 0}%`}}
        />
      </div>

      {finished ? (
        <div className={styles.emptyState}>
          <p>
            <strong>
              Set complete: {correct}/{questions.length} correct.
            </strong>
          </p>
          <button
            type="button"
            className="button button--primary"
            onClick={() => setEpoch((e) => e + 1)}>
            Practice again
          </button>
        </div>
      ) : q ? (
        <QuizCard
          key={q.id}
          question={q}
          onResult={(qid, ok) => setResults((r) => ({...r, [qid]: ok}))}
          onNext={() => setIndex((i) => i + 1)}
        />
      ) : (
        <div className={styles.emptyState}>No questions match these filters.</div>
      )}
    </div>
  );
}
