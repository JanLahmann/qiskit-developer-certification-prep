/**
 * ProgressOverview — the learner's dashboard strip.
 *
 * Aggregates localStorage drill stats + mock attempts against the bank
 * metadata into a per-section progress view with a "continue where it
 * hurts" recommendation. Pure selection from precomputed data — no
 * runtime AI. SSR-safe (renders a neutral CTA until hydrated).
 */

import React, {useEffect, useMemo, useState} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import {getMockState, getProgress} from '@site/src/lib/storage';
import syllabusMeta from '@site/src/data/syllabus.json';
import styles from './progress.module.css';

type SectionMeta = {
  id: string;
  num: number;
  title: string;
  weightPct: number;
  bankCount: number;
};

type SectionView = SectionMeta & {
  attempted: number;
  mastered: number;
  accuracy: number | null;
};

function useSectionViews(): {views: SectionView[]; hydrated: boolean} {
  const [hydrated, setHydrated] = useState(false);
  useEffect(() => setHydrated(true), []);
  const views = useMemo(() => {
    const sections = (syllabusMeta.sections as SectionMeta[]).map((s) => ({
      ...s,
      attempted: 0,
      mastered: 0,
      accuracy: null as number | null,
    }));
    if (!hydrated) {
      return sections;
    }
    const prog = getProgress().questions;
    const bySection = new Map(sections.map((s) => [s.id, s]));
    let totalA = 0;
    let totalC = 0;
    for (const [qid, st] of Object.entries(prog)) {
      const sec = bySection.get(qid.split('-')[0]);
      if (!sec || st.a === 0) {
        continue;
      }
      sec.attempted += 1;
      if (st.s >= 2) {
        sec.mastered += 1;
      }
      totalA += st.a;
      totalC += st.c;
    }
    for (const sec of sections) {
      let a = 0;
      let c = 0;
      for (const [qid, st] of Object.entries(prog)) {
        if (qid.startsWith(`${sec.id}-`)) {
          a += st.a;
          c += st.c;
        }
      }
      sec.accuracy = a > 0 ? c / a : null;
    }
    void totalA;
    void totalC;
    return sections;
  }, [hydrated]);
  return {views, hydrated};
}

export default function ProgressOverview({
  compact = false,
}: {
  compact?: boolean;
}): React.ReactElement | null {
  const {views, hydrated} = useSectionViews();
  const mock = hydrated ? getMockState().attempts : [];

  const touched = views.filter((v) => v.attempted > 0);
  const weakest = touched
    .filter((v) => v.accuracy !== null && v.bankCount > 0)
    .sort((a, b) => (a.accuracy ?? 1) - (b.accuracy ?? 1))[0];
  const next =
    weakest ??
    views.find((v) => v.attempted === 0 && v.bankCount > 0) ??
    views[0];

  if (compact && hydrated && touched.length === 0 && mock.length === 0) {
    // Fresh visitor on the homepage: no progress strip, the hero CTA is enough.
    return null;
  }

  const lastMock = mock[mock.length - 1];

  return (
    <div className={clsx(styles.panel, compact && styles.panelCompact)}>
      <div className={styles.headRow}>
        <strong>
          {touched.length === 0
            ? 'Your study progress'
            : `Your progress: ${touched.length}/8 sections started`}
        </strong>
        {lastMock ? (
          <span className={styles.mockNote}>
            last mock: {lastMock.score}/{lastMock.total}{' '}
            {lastMock.passed ? '✅' : '— keep going'}
          </span>
        ) : null}
        {next ? (
          <Link
            className="button button--primary button--sm"
            to={`/docs/sections/${next.id}`}>
            {weakest
              ? `Strengthen section ${next.num} →`
              : `Continue with section ${next.num} →`}
          </Link>
        ) : null}
      </div>
      <div className={styles.grid}>
        {views.map((v) => {
          const pct = v.bankCount > 0 ? (v.mastered / v.bankCount) * 100 : 0;
          return (
            <Link
              key={v.id}
              to={`/docs/sections/${v.id}`}
              className={styles.cell}
              title={`${v.title} — ${v.mastered}/${v.bankCount} mastered (streak ≥2)`}>
              <span className={styles.cellNum}>{v.num}</span>
              <span className={styles.cellBar}>
                <span className={styles.cellFill} style={{width: `${pct}%`}} />
              </span>
              <span className={styles.cellPct}>
                {v.bankCount > 0 ? `${v.mastered}/${v.bankCount}` : '—'}
              </span>
            </Link>
          );
        })}
      </div>
      <div className={styles.legend}>
        mastered = answered with a correct streak of ≥2 · progress lives only in
        your browser
      </div>
    </div>
  );
}
