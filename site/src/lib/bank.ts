/**
 * Question-bank types and loaders.
 *
 * The bank is compiled by pipeline/build_site_data.py into per-section JSON
 * files under src/data/bank/ (proof scripts stripped; proof evidence from
 * the verifier's artifacts embedded). Sections are lazy-loaded so a drill
 * page only pays for its own section.
 */

export type QuestionType = 'mcq' | 'multi' | 'predict-output' | 'spot-bug';

export type BankOption = {key: string; text: string};

export type BankProof = {
  status: 'executed' | 'conceptual';
  /** per-option observed evidence strings (executed only) */
  evidence?: Record<string, string>;
  /** exact library versions the proof ran against */
  versions?: Record<string, string>;
  verifiedOn?: string;
  wallSeconds?: number;
};

export type BankQuestion = {
  id: string;
  section: SectionId;
  objectives: string[];
  type: QuestionType;
  difficulty: 1 | 2 | 3;
  stem: string;
  code: string | null;
  options: BankOption[];
  answer: string[];
  explanation: {
    correct: string;
    distractors: Record<string, string>;
    citations: string[];
  };
  proof: BankProof;
  provenance: {generated: string; model: string; adversarialRounds: number};
};

export type SectionId = 's1' | 's2' | 's3' | 's4' | 's5' | 's6' | 's7' | 's8';

export type SectionMeta = {
  id: SectionId;
  num: number;
  title: string;
  weightPct: number;
  objectives: {id: string; text: string}[];
};

export type SectionBank = {
  section: SectionMeta;
  questions: BankQuestion[];
};

export const SECTION_IDS: SectionId[] = [
  's1',
  's2',
  's3',
  's4',
  's5',
  's6',
  's7',
  's8',
];

export async function loadSection(id: SectionId): Promise<SectionBank> {
  // Webpack turns this into a lazy context over src/data/bank/*.json.
  const mod = await import(`@site/src/data/bank/${id}.json`);
  return (mod.default ?? mod) as SectionBank;
}

export async function loadAllSections(): Promise<SectionBank[]> {
  return Promise.all(SECTION_IDS.map(loadSection));
}

/** Mulberry32 — tiny seedable PRNG for reproducible exam sampling. */
export function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function seededShuffle<T>(items: T[], rand: () => number): T[] {
  const arr = items.slice();
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
