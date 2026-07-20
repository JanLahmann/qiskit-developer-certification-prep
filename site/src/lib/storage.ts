/**
 * CertiQ localStorage layer — the ONLY place that touches window.localStorage.
 *
 * All persistent learner state lives under namespaced keys (qcs.*), is
 * versioned, JSON-serialized, and export/importable as one bundle. Every
 * accessor is SSR-safe (no-ops during static rendering).
 */

export type QuestionStat = {
  /** total attempts */
  a: number;
  /** total correct */
  c: number;
  /** current correct streak */
  s: number;
  /** last attempt unix ms */
  t: number;
  /** last attempt was correct */
  r: boolean;
  /** flagged for review */
  f?: boolean;
};

export type ProgressState = {
  questions: Record<string, QuestionStat>;
};

export type MockAttempt = {
  date: string; // ISO
  seed: number;
  score: number;
  total: number;
  passed: boolean;
  durationSec: number;
  perSection: Record<string, {correct: number; total: number}>;
};

export type MockState = {attempts: MockAttempt[]};

export type SettingsState = {
  /** opt-in doQumentation integration (links + experimental execution) */
  doqIntegration: boolean;
};

const KEYS = {
  progress: 'qcs.progress.v1',
  mock: 'qcs.mock.v1',
  settings: 'qcs.settings.v1',
} as const;

const hasWindow = (): boolean =>
  typeof window !== 'undefined' && !!window.localStorage;

function read<T>(key: string, fallback: T): T {
  if (!hasWindow()) {
    return fallback;
  }
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? {...fallback, ...(JSON.parse(raw) as T)} : fallback;
  } catch {
    return fallback;
  }
}

function write<T>(key: string, value: T): void {
  if (!hasWindow()) {
    return;
  }
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Storage full or blocked — degrade silently; the site must keep working.
  }
}

// ---- progress ----

export function getProgress(): ProgressState {
  return read<ProgressState>(KEYS.progress, {questions: {}});
}

export function recordAnswer(qid: string, correct: boolean): QuestionStat {
  const p = getProgress();
  const prev: QuestionStat = p.questions[qid] ?? {
    a: 0,
    c: 0,
    s: 0,
    t: 0,
    r: false,
  };
  const next: QuestionStat = {
    ...prev,
    a: prev.a + 1,
    c: prev.c + (correct ? 1 : 0),
    s: correct ? prev.s + 1 : 0,
    t: Date.now(),
    r: correct,
  };
  p.questions[qid] = next;
  write(KEYS.progress, p);
  return next;
}

export function toggleFlag(qid: string): boolean {
  const p = getProgress();
  const prev: QuestionStat = p.questions[qid] ?? {
    a: 0,
    c: 0,
    s: 0,
    t: 0,
    r: false,
  };
  prev.f = !prev.f;
  p.questions[qid] = prev;
  write(KEYS.progress, p);
  return !!prev.f;
}

// ---- mock exam ----

export function getMockState(): MockState {
  return read<MockState>(KEYS.mock, {attempts: []});
}

export function recordMockAttempt(attempt: MockAttempt): void {
  const m = getMockState();
  m.attempts.push(attempt);
  write(KEYS.mock, m);
}

// ---- settings ----

export function getSettings(): SettingsState {
  return read<SettingsState>(KEYS.settings, {doqIntegration: false});
}

export function setSettings(s: Partial<SettingsState>): SettingsState {
  const next = {...getSettings(), ...s};
  write(KEYS.settings, next);
  return next;
}

// ---- export / import / reset ----

export function exportAll(): string {
  return JSON.stringify(
    {
      exported: new Date().toISOString(),
      app: 'CertiQ',
      version: 1,
      data: {
        [KEYS.progress]: getProgress(),
        [KEYS.mock]: getMockState(),
        [KEYS.settings]: getSettings(),
      },
    },
    null,
    2,
  );
}

export function importAll(json: string): {ok: boolean; error?: string} {
  try {
    const parsed = JSON.parse(json) as {
      version?: number;
      data?: Record<string, unknown>;
    };
    if (!parsed.data) {
      return {ok: false, error: 'Not a CertiQ export file.'};
    }
    for (const key of Object.values(KEYS)) {
      if (parsed.data[key] !== undefined) {
        write(key, parsed.data[key]);
      }
    }
    return {ok: true};
  } catch (e) {
    return {ok: false, error: `Could not parse file: ${String(e)}`};
  }
}

export function resetAll(): void {
  if (!hasWindow()) {
    return;
  }
  for (const key of Object.values(KEYS)) {
    window.localStorage.removeItem(key);
  }
}
