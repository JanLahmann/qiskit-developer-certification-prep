/**
 * MockExam — faithful C1000-179 simulator.
 *
 * 68 questions / 90 minutes / pass at 47, sampled from the verified bank
 * stratified by official section weights (largest-remainder method), with
 * a seeded shuffle so any exam can be reproduced from its seed. Deferred
 * grading; per-section score report vs the pass line; attempt history and
 * full review mode. Everything client-side.
 */

import React, {useCallback, useEffect, useMemo, useRef, useState} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import CodeBlock from '@theme/CodeBlock';
import type {BankQuestion, SectionBank} from '@site/src/lib/bank';
import {loadAllSections, mulberry32, seededShuffle} from '@site/src/lib/bank';
import {renderInline} from '@site/src/lib/md';
import {getMockState, recordMockAttempt, type MockAttempt} from '@site/src/lib/storage';
import QuizCard from '../Quiz/QuizCard';
import quizStyles from '../Quiz/styles.module.css';
import styles from './exam.module.css';

const EXAM = {questions: 68, minutes: 90, pass: 47};

type Phase = 'intro' | 'running' | 'report';

type ExamPaper = {
  seed: number;
  questions: BankQuestion[];
  /** actual pass line (scaled if the bank can't fill 68 yet) */
  passLine: number;
  totalSeconds: number;
};

/** Largest-remainder allocation of exam slots by section weight. */
function allocate(sections: SectionBank[], total: number): Map<string, number> {
  const weights = sections.map((s) => s.section.weightPct);
  const wSum = weights.reduce((a, b) => a + b, 0);
  const exact = sections.map((s) => (total * s.section.weightPct) / wSum);
  const base = exact.map(Math.floor);
  let assigned = base.reduce((a, b) => a + b, 0);
  const order = exact
    .map((x, i) => ({i, frac: x - Math.floor(x)}))
    .sort((a, b) => b.frac - a.frac);
  for (const {i} of order) {
    if (assigned >= total) {
      break;
    }
    base[i] += 1;
    assigned += 1;
  }
  return new Map(sections.map((s, i) => [s.section.id, base[i]]));
}

function buildPaper(sections: SectionBank[], seed: number): ExamPaper {
  const rand = mulberry32(seed);
  const available = sections.reduce((a, s) => a + s.questions.length, 0);
  const total = Math.min(EXAM.questions, available);
  const quota = allocate(sections, total);

  // Draw per section; collect shortfalls and refill from leftovers.
  const picked: BankQuestion[] = [];
  const leftovers: BankQuestion[] = [];
  for (const s of sections) {
    const want = quota.get(s.section.id) ?? 0;
    const shuffled = seededShuffle(s.questions, rand);
    picked.push(...shuffled.slice(0, want));
    leftovers.push(...shuffled.slice(want));
  }
  if (picked.length < total) {
    picked.push(...seededShuffle(leftovers, rand).slice(0, total - picked.length));
  }

  const questions = seededShuffle(picked, rand);
  const passLine =
    total === EXAM.questions
      ? EXAM.pass
      : Math.ceil((EXAM.pass / EXAM.questions) * total);
  const totalSeconds =
    total === EXAM.questions
      ? EXAM.minutes * 60
      : Math.round((EXAM.minutes * 60 * total) / EXAM.questions);
  return {seed, questions, passLine, totalSeconds};
}

function fmtTime(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

export default function MockExam(): React.ReactElement {
  const [sections, setSections] = useState<SectionBank[] | null>(null);
  const [phase, setPhase] = useState<Phase>('intro');
  const [seedInput, setSeedInput] = useState('');
  const [paper, setPaper] = useState<ExamPaper | null>(null);
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string[]>>({});
  const [marked, setMarked] = useState<Set<string>>(new Set());
  const [remaining, setRemaining] = useState(0);
  const [attempt, setAttempt] = useState<MockAttempt | null>(null);
  const [reviewFilter, setReviewFilter] = useState<'wrong' | 'all'>('wrong');
  const deadlineRef = useRef(0);
  const submitRef = useRef<() => void>(() => {});

  useEffect(() => {
    loadAllSections().then(setSections).catch(() => setSections([]));
  }, []);

  const history = useMemo(
    () => (typeof window === 'undefined' ? [] : getMockState().attempts),
    [phase],
  );

  const bankTotal = useMemo(
    () => (sections ?? []).reduce((a, s) => a + s.questions.length, 0),
    [sections],
  );

  const start = useCallback(() => {
    if (!sections) {
      return;
    }
    const seed = /^\d+$/.test(seedInput.trim())
      ? Number(seedInput.trim()) >>> 0
      : Math.floor(Math.random() * 2 ** 31);
    const p = buildPaper(sections, seed);
    setPaper(p);
    setAnswers({});
    setMarked(new Set());
    setIdx(0);
    deadlineRef.current = Date.now() + p.totalSeconds * 1000;
    setRemaining(p.totalSeconds);
    setPhase('running');
  }, [sections, seedInput]);

  const submit = useCallback(() => {
    if (!paper) {
      return;
    }
    const perSection: Record<string, {correct: number; total: number}> = {};
    let score = 0;
    for (const q of paper.questions) {
      const sel = new Set(answers[q.id] ?? []);
      const ans = new Set(q.answer);
      const ok = sel.size === ans.size && [...sel].every((k) => ans.has(k));
      const ps = (perSection[q.section] ??= {correct: 0, total: 0});
      ps.total += 1;
      if (ok) {
        ps.correct += 1;
        score += 1;
      }
    }
    const a: MockAttempt = {
      date: new Date().toISOString(),
      seed: paper.seed,
      score,
      total: paper.questions.length,
      passed: score >= paper.passLine,
      durationSec:
        paper.totalSeconds -
        Math.max(0, Math.round((deadlineRef.current - Date.now()) / 1000)),
      perSection,
    };
    recordMockAttempt(a);
    setAttempt(a);
    setPhase('report');
  }, [paper, answers]);

  useEffect(() => {
    submitRef.current = submit;
  }, [submit]);

  // Timer (drift-corrected against the wall clock).
  useEffect(() => {
    if (phase !== 'running') {
      return undefined;
    }
    const t = window.setInterval(() => {
      const left = Math.max(0, Math.round((deadlineRef.current - Date.now()) / 1000));
      setRemaining(left);
      if (left <= 0) {
        submitRef.current();
      }
    }, 500);
    return () => window.clearInterval(t);
  }, [phase]);

  // Warn before leaving a running exam.
  useEffect(() => {
    if (phase !== 'running') {
      return undefined;
    }
    const h = (e: BeforeUnloadEvent) => {
      e.preventDefault();
    };
    window.addEventListener('beforeunload', h);
    return () => window.removeEventListener('beforeunload', h);
  }, [phase]);

  if (!sections) {
    return <div className={styles.wrap}>Loading question bank…</div>;
  }

  // ---------- intro ----------
  if (phase === 'intro') {
    const last = history[history.length - 1];
    return (
      <div className={styles.wrap}>
        <div className={styles.introCard}>
          <h1>Mock exam</h1>
          <p>
            Exactly like the real C1000-179: <strong>68 questions</strong> in{' '}
            <strong>90 minutes</strong>, pass at <strong>47 correct (69%)</strong>,
            sampled to match the official section weights. No feedback until you
            submit — then a full per-section diagnosis and complete review.
          </p>
          <div className={styles.factRow}>
            <div className={styles.fact}>
              <span className={styles.factValue}>{Math.min(68, bankTotal)}</span>
              <span className={styles.factLabel}>questions</span>
            </div>
            <div className={styles.fact}>
              <span className={styles.factValue}>
                {paperPreviewMinutes(bankTotal)}
              </span>
              <span className={styles.factLabel}>minutes</span>
            </div>
            <div className={styles.fact}>
              <span className={styles.factValue}>
                {bankTotal >= 68 ? 47 : Math.ceil((47 / 68) * Math.min(68, bankTotal))}
              </span>
              <span className={styles.factLabel}>to pass</span>
            </div>
            <div className={styles.fact}>
              <span className={styles.factValue}>{history.length}</span>
              <span className={styles.factLabel}>attempts so far</span>
            </div>
          </div>
          {bankTotal < 68 ? (
            <p>
              <em>
                The verified bank currently holds {bankTotal} questions, so this
                run is scaled down proportionally (time and pass line included).
              </em>
            </p>
          ) : null}
          <div className={styles.seedRow}>
            <label htmlFor="seed">Seed (optional, for a reproducible exam):</label>
            <input
              id="seed"
              value={seedInput}
              inputMode="numeric"
              placeholder="random"
              onChange={(e) => setSeedInput(e.target.value)}
            />
          </div>
          <button
            type="button"
            className="button button--primary button--lg"
            disabled={bankTotal === 0}
            onClick={start}>
            Start exam →
          </button>
          {last ? (
            <p className={styles.trend}>
              Last attempt: {last.score}/{last.total} (
              {last.passed ? 'passed' : 'not passed'}) on{' '}
              {new Date(last.date).toLocaleDateString()} · seed {last.seed}
            </p>
          ) : null}
        </div>
      </div>
    );
  }

  if (!paper) {
    return <div className={styles.wrap} />;
  }

  // ---------- running ----------
  if (phase === 'running') {
    const q = paper.questions[idx];
    const selected = new Set(answers[q.id] ?? []);
    const isMulti = q.type === 'multi';
    const answeredCount = paper.questions.filter(
      (question) => (answers[question.id] ?? []).length > 0,
    ).length;

    const toggle = (key: string) => {
      setAnswers((prev) => {
        const cur = new Set(prev[q.id] ?? []);
        if (isMulti) {
          if (cur.has(key)) {
            cur.delete(key);
          } else {
            cur.add(key);
          }
        } else {
          cur.clear();
          cur.add(key);
        }
        return {...prev, [q.id]: [...cur].sort()};
      });
    };

    return (
      <div className={styles.wrap}>
        <div className={styles.topBar}>
          <span
            className={clsx(styles.timer, remaining < 300 && styles.timerLow)}
            aria-live="polite">
            ⏱ {fmtTime(remaining)}
          </span>
          <span className={styles.progressText}>
            Question {idx + 1}/{paper.questions.length} · {answeredCount} answered
          </span>
          <span className={styles.spacer} />
          <button
            type="button"
            className="button button--secondary button--sm"
            onClick={() => {
              setMarked((prev) => {
                const next = new Set(prev);
                if (next.has(q.id)) {
                  next.delete(q.id);
                } else {
                  next.add(q.id);
                }
                return next;
              });
            }}>
            {marked.has(q.id) ? '★ Marked' : '☆ Mark for review'}
          </button>
          <button
            type="button"
            className="button button--danger button--sm"
            onClick={() => {
              const open = paper.questions.length - answeredCount;
              // eslint-disable-next-line no-alert
              if (open === 0 || window.confirm(`${open} question(s) unanswered. Submit anyway?`)) {
                submit();
              }
            }}>
            Submit exam
          </button>
        </div>

        <div className={styles.palette}>
          {paper.questions.map((question, i) => (
            <button
              key={question.id}
              type="button"
              className={clsx(
                styles.palItem,
                (answers[question.id] ?? []).length > 0 && styles.palAnswered,
                marked.has(question.id) && styles.palMarked,
                i === idx && styles.palCurrent,
              )}
              onClick={() => setIdx(i)}
              aria-label={`Go to question ${i + 1}`}>
              {i + 1}
            </button>
          ))}
        </div>

        <div className={quizStyles.card}>
          <div className={quizStyles.metaRow}>
            <span className={quizStyles.chip}>
              {isMulti ? 'multi-select' : 'single answer'}
            </span>
          </div>
          <div className={quizStyles.stem}>
            {renderInline(q.stem)}
            {isMulti ? <em> (Select all that apply.)</em> : null}
          </div>
          {q.code ? <CodeBlock language="python">{q.code}</CodeBlock> : null}
          <div className={quizStyles.options}>
            {q.options.map((opt) => (
              <button
                key={opt.key}
                type="button"
                className={clsx(
                  quizStyles.option,
                  selected.has(opt.key) && quizStyles.optionSelected,
                )}
                onClick={() => toggle(opt.key)}>
                <span className={quizStyles.optionKey}>{opt.key}</span>
                <span>{renderInline(opt.text)}</span>
              </button>
            ))}
          </div>
        </div>

        <div className={styles.navRow}>
          <button
            type="button"
            className="button button--secondary"
            disabled={idx === 0}
            onClick={() => setIdx((i) => i - 1)}>
            ← Previous
          </button>
          <button
            type="button"
            className="button button--primary"
            disabled={idx === paper.questions.length - 1}
            onClick={() => setIdx((i) => i + 1)}>
            Next →
          </button>
        </div>
      </div>
    );
  }

  // ---------- report ----------
  const a = attempt;
  if (!a) {
    return <div className={styles.wrap} />;
  }
  const passPct = (paper.passLine / paper.questions.length) * 100;
  const bySection = sections
    .map((s) => ({
      meta: s.section,
      stat: a.perSection[s.section.id],
    }))
    .filter((x) => x.stat && x.stat.total > 0);
  const weakest = [...bySection].sort(
    (x, y) => x.stat.correct / x.stat.total - y.stat.correct / y.stat.total,
  )[0];
  const wrongQuestions = paper.questions.filter((q) => {
    const sel = new Set(answers[q.id] ?? []);
    const ans = new Set(q.answer);
    return !(sel.size === ans.size && [...sel].every((k) => ans.has(k)));
  });
  const reviewList = reviewFilter === 'wrong' ? wrongQuestions : paper.questions;

  return (
    <div className={styles.wrap}>
      <div
        className={clsx(styles.scoreBanner, a.passed && styles.scoreBannerPass)}>
        <div className={styles.scoreHuge}>
          {a.score}/{a.total} — {a.passed ? 'PASS' : 'below the pass line'}
        </div>
        <div>
          Pass line: {paper.passLine} · time used {fmtTime(a.durationSec)} · seed{' '}
          {a.seed} (reuse it to retake the identical exam)
        </div>
        {history.length > 1 ? (
          <div className={styles.trend}>
            Attempt history:{' '}
            {history
              .map((h) => `${Math.round((h.score / h.total) * 100)}%`)
              .join(' → ')}
          </div>
        ) : null}
      </div>

      <h2>Section diagnosis</h2>
      <div className={styles.reportGrid}>
        {bySection.map(({meta, stat}) => {
          const pct = (stat.correct / stat.total) * 100;
          return (
            <div key={meta.id} className={styles.reportRow}>
              <Link to={`/docs/sections/${meta.id}`}>
                {meta.num} · {meta.title}
              </Link>
              <div className={styles.reportBarTrack}>
                <div
                  className={clsx(
                    styles.reportBarFill,
                    pct < passPct && styles.reportBarFillLow,
                  )}
                  style={{width: `${pct}%`}}
                />
                <div
                  className={styles.reportPassMark}
                  style={{left: `${passPct}%`}}
                  title={`pass line ${Math.round(passPct)}%`}
                />
              </div>
              <span>
                {stat.correct}/{stat.total}
              </span>
            </div>
          );
        })}
      </div>

      {weakest ? (
        <p>
          <strong>Where to focus next:</strong>{' '}
          <Link to={`/docs/sections/${weakest.meta.id}`}>
            Section {weakest.meta.num} — {weakest.meta.title}
          </Link>{' '}
          was your weakest area ({weakest.stat.correct}/{weakest.stat.total}).
          Re-study its resources, then drill it with &quot;weakest first&quot;
          ordering until your streaks recover.
        </p>
      ) : null}

      <div className={styles.reviewFilter}>
        <h2 style={{marginBottom: 0}}>Review</h2>
        <span className={styles.spacer} />
        <button
          type="button"
          className={clsx(
            'button button--sm',
            reviewFilter === 'wrong' ? 'button--primary' : 'button--secondary',
          )}
          onClick={() => setReviewFilter('wrong')}>
          Wrong only ({wrongQuestions.length})
        </button>
        <button
          type="button"
          className={clsx(
            'button button--sm',
            reviewFilter === 'all' ? 'button--primary' : 'button--secondary',
          )}
          onClick={() => setReviewFilter('all')}>
          All ({paper.questions.length})
        </button>
      </div>

      {reviewList.map((q) => (
        <QuizCard
          key={q.id}
          question={q}
          review={answers[q.id] ?? []}
          keyboard={false}
        />
      ))}

      <div className={styles.navRow}>
        <button
          type="button"
          className="button button--primary"
          onClick={() => setPhase('intro')}>
          Take another exam
        </button>
      </div>
    </div>
  );
}

function paperPreviewMinutes(bankTotal: number): number {
  return bankTotal >= 68
    ? 90
    : Math.max(1, Math.round((90 * Math.min(68, bankTotal)) / 68));
}
