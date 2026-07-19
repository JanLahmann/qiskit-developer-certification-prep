/**
 * QuizCard — renders one question: stem, code, options, grading,
 * proof-backed explanations. Used by PracticeSet (instant feedback) and
 * the mock exam review screen (deferred feedback).
 */

import React, {useCallback, useEffect, useMemo, useState} from 'react';
import clsx from 'clsx';
import CodeBlock from '@theme/CodeBlock';
import type {BankQuestion} from '@site/src/lib/bank';
import {renderInline} from '@site/src/lib/md';
import {recordAnswer, toggleFlag} from '@site/src/lib/storage';
import styles from './styles.module.css';

const REPO = 'https://github.com/JanLahmann/qiskit-developer-certification-prep';

function issueUrl(q: BankQuestion): string {
  const title = `[${q.id}] Question feedback`;
  const body = [
    `**Question:** \`${q.id}\` (section ${q.section})`,
    '',
    '**What looks wrong / could be better?**',
    '',
    '',
    '---',
    '_All feedback welcome — questions are AI-generated and execution-verified; humans make them better._',
  ].join('\n');
  return `${REPO}/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
}

const TYPE_LABEL: Record<BankQuestion['type'], string> = {
  mcq: 'multiple choice',
  multi: 'multi-select',
  'predict-output': 'predict the output',
  'spot-bug': 'spot the bug',
};

export type QuizCardProps = {
  question: BankQuestion;
  /** show grading immediately after Check (practice) */
  onResult?: (qid: string, correct: boolean) => void;
  /** advance to next question (renders a Next button when set) */
  onNext?: () => void;
  /** capture keyboard (disable when multiple cards are on screen) */
  keyboard?: boolean;
  /**
   * review mode (mock-exam post-submit): render pre-graded with the given
   * selection; no interaction, no stat recording.
   */
  review?: string[];
};

export default function QuizCard({
  question: q,
  onResult,
  onNext,
  keyboard = true,
  review,
}: QuizCardProps): React.ReactElement {
  const [selected, setSelected] = useState<Set<string>>(
    () => new Set(review ?? []),
  );
  const [checked, setChecked] = useState(!!review);
  const [flagged, setFlagged] = useState(false);
  const [showAllExplanations, setShowAllExplanations] = useState(false);

  const isMulti = q.type === 'multi';
  const answerSet = useMemo(() => new Set(q.answer), [q]);

  // Reset per question.
  useEffect(() => {
    setSelected(new Set(review ?? []));
    setChecked(!!review);
    setShowAllExplanations(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q.id]);

  const correct =
    checked &&
    selected.size === answerSet.size &&
    [...selected].every((k) => answerSet.has(k));

  const toggle = useCallback(
    (key: string) => {
      if (checked) {
        return;
      }
      setSelected((prev) => {
        const next = new Set(prev);
        if (isMulti) {
          if (next.has(key)) {
            next.delete(key);
          } else {
            next.add(key);
          }
        } else {
          next.clear();
          next.add(key);
        }
        return next;
      });
    },
    [checked, isMulti],
  );

  const check = useCallback(() => {
    if (checked || selected.size === 0) {
      return;
    }
    const isCorrect =
      selected.size === answerSet.size &&
      [...selected].every((k) => answerSet.has(k));
    setChecked(true);
    recordAnswer(q.id, isCorrect);
    onResult?.(q.id, isCorrect);
  }, [checked, selected, answerSet, q.id, onResult]);

  useEffect(() => {
    if (!keyboard) {
      return undefined;
    }
    const handler = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target && ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) {
        return;
      }
      const upper = e.key.toUpperCase();
      const keys = q.options.map((o) => o.key);
      if (keys.includes(upper)) {
        toggle(upper);
      } else if (/^[1-6]$/.test(e.key)) {
        const idx = Number(e.key) - 1;
        if (idx < keys.length) {
          toggle(keys[idx]);
        }
      } else if (e.key === 'Enter') {
        if (!checked) {
          check();
        } else {
          onNext?.();
        }
      } else if (upper === 'F') {
        setFlagged(toggleFlag(q.id));
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [keyboard, q, toggle, check, checked, onNext]);

  const proofBadge =
    q.proof.status === 'executed' ? (
      <span
        className={clsx(styles.chip, styles.chipVerified)}
        title={`Proof executed against ${Object.entries(q.proof.versions ?? {})
          .map(([k, v]) => `${k} ${v}`)
          .join(', ')} on ${q.proof.verifiedOn ?? 'build'}`}>
        ✓ execution-verified
      </span>
    ) : (
      <span
        className={clsx(styles.chip, styles.chipCited)}
        title="Conceptual question — grounded in the cited official documentation">
        📖 doc-cited
      </span>
    );

  return (
    <div className={styles.card}>
      <div className={styles.metaRow}>
        <span className={styles.chip}>{q.id}</span>
        <span className={styles.chip}>{TYPE_LABEL[q.type]}</span>
        <span className={styles.difficulty} title={`difficulty ${q.difficulty}/3`}>
          {'●'.repeat(q.difficulty)}
          {'○'.repeat(3 - q.difficulty)}
        </span>
        {proofBadge}
        <span className={styles.spacer} />
        <button
          type="button"
          className={clsx(styles.flagBtn, flagged && styles.flagBtnActive)}
          title="Flag for review (F)"
          aria-label="Flag question for review"
          onClick={() => setFlagged(toggleFlag(q.id))}>
          {flagged ? '🚩' : '⚑'}
        </button>
      </div>

      <div className={styles.stem}>
        {renderInline(q.stem)}
        {isMulti ? <em> (Select all that apply.)</em> : null}
      </div>

      {q.code ? (
        <CodeBlock language="python">{q.code}</CodeBlock>
      ) : null}

      <div className={styles.options} role={isMulti ? 'group' : 'radiogroup'}>
        {q.options.map((opt) => {
          const isSelected = selected.has(opt.key);
          const isAnswer = answerSet.has(opt.key);
          const stateClass = !checked
            ? isSelected
              ? styles.optionSelected
              : undefined
            : isAnswer && isSelected
              ? styles.optionCorrect
              : isAnswer
                ? styles.optionMissed
                : isSelected
                  ? styles.optionWrong
                  : undefined;
          const showExplain =
            checked &&
            !isAnswer &&
            (isSelected || showAllExplanations) &&
            q.explanation.distractors[opt.key];
          return (
            <React.Fragment key={opt.key}>
              <button
                type="button"
                className={clsx(styles.option, stateClass)}
                onClick={() => toggle(opt.key)}
                disabled={checked}
                role={isMulti ? 'checkbox' : 'radio'}
                aria-checked={isSelected}>
                <span className={styles.optionKey}>{opt.key}</span>
                <span>{renderInline(opt.text)}</span>
              </button>
              {showExplain ? (
                <div className={styles.optionExplain}>
                  ✗ {renderInline(q.explanation.distractors[opt.key])}
                </div>
              ) : null}
            </React.Fragment>
          );
        })}
      </div>

      <div className={styles.actions}>
        {!checked ? (
          <>
            <button
              type="button"
              className="button button--primary"
              onClick={check}
              disabled={selected.size === 0}>
              Check answer
            </button>
            <span className={styles.kbdHint}>
              keys: A–{q.options[q.options.length - 1]?.key} select · Enter check
            </span>
          </>
        ) : (
          <>
            <span
              className={clsx(
                styles.result,
                correct ? styles.resultCorrect : styles.resultWrong,
              )}>
              {correct ? 'Correct.' : `Not quite — answer: ${q.answer.join(', ')}.`}
            </span>
            {onNext ? (
              <button
                type="button"
                className="button button--primary button--sm"
                onClick={onNext}>
                Next →
              </button>
            ) : null}
            <button
              type="button"
              className="button button--secondary button--sm"
              onClick={() => setShowAllExplanations((v) => !v)}>
              {showAllExplanations ? 'Hide' : 'Show'} all explanations
            </button>
          </>
        )}
      </div>

      {checked ? (
        <div className={styles.explainBox}>
          <div>
            <strong>Why {q.answer.join(' + ')}:</strong>{' '}
            {renderInline(q.explanation.correct)}
          </div>

          {q.proof.status === 'executed' && q.proof.evidence ? (
            <details className={styles.proofDetails}>
              <summary>Execution proof — what actually happened</summary>
              <ul className={styles.proofEvidence}>
                {q.options.map((opt) => (
                  <li key={opt.key}>
                    <strong>{opt.key}:</strong> {q.proof.evidence?.[opt.key]}
                  </li>
                ))}
              </ul>
              <div className={styles.proofMeta}>
                Executed at build time against{' '}
                {Object.entries(q.proof.versions ?? {})
                  .map(([k, v]) => `${k} ${v}`)
                  .join(' · ')}{' '}
                on {q.proof.verifiedOn}.
              </div>
            </details>
          ) : null}

          {q.explanation.citations.length > 0 ? (
            <div className={styles.citations}>
              <strong>Read more:</strong>{' '}
              {q.explanation.citations.map((url) => (
                <a key={url} href={url} target="_blank" rel="noopener noreferrer">
                  {new URL(url).pathname.split('/').filter(Boolean).slice(-1)[0]}
                  {' ↗'}
                </a>
              ))}
            </div>
          ) : null}

          <div className={styles.footerRow}>
            <span>
              AI-generated · {q.proof.status === 'executed' ? 'execution-verified' : 'doc-cited'} ·
              adversarially reviewed ×{q.provenance.adversarialRounds}
            </span>
            <a href={issueUrl(q)} target="_blank" rel="noopener noreferrer">
              Report an issue with this question
            </a>
          </div>
        </div>
      ) : null}
    </div>
  );
}
