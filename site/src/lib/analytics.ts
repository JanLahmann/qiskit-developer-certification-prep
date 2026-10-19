/**
 * Umami custom events, v2 family taxonomy ("CertiQ: <what happened>", see
 * family/EVENTS.md in JanLahmann/Fun-with-Quantum). Properties are fixed
 * vocabularies only: section ids, objective ids, buckets, hosts. Never free
 * text or anything personal.
 *
 * A no-op during SSR, when the tracker is absent or blocked, and when the
 * before-send guard in docusaurus.config.ts drops the event (bots, ?notrack).
 */

export type EventProps = Record<string, string | number>;

declare global {
  interface Window {
    umami?: {track: (event: string, data?: EventProps) => void};
  }
}

export function track(what: string, props?: EventProps): void {
  if (typeof window === 'undefined') {
    return;
  }
  try {
    window.umami?.track(`CertiQ: ${what}`, props);
  } catch {
    // analytics must never break the page
  }
}

/** Coarse score bucket, so no event carries an exact result. */
export function scoreBucket(correct: number, total: number): string {
  const pct = total > 0 ? (correct / total) * 100 : 0;
  if (pct >= 90) {
    return '90-100';
  }
  if (pct >= 70) {
    return '70-89';
  }
  if (pct >= 50) {
    return '50-69';
  }
  return '0-49';
}
