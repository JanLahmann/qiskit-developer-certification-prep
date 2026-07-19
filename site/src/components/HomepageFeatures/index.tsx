import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  emoji: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Proven, not asserted',
    emoji: '🔬',
    description: (
      <>
        Every code-bearing question is executed at build time against a pinned
        Qiskit 2.x stack. Correct answers are <em>proven</em>, distractors are{' '}
        <em>disproven</em> — and the execution proof ships with the question.
      </>
    ),
  },
  {
    title: 'Guided by the official syllabus',
    emoji: '🧭',
    description: (
      <>
        The eight official exam sections, their weights, and IBM&apos;s own
        recommended resources drive everything: study path, drills, and a
        faithful 68-question / 90-minute mock exam with per-section remediation.
      </>
    ),
  },
  {
    title: 'Private by design',
    emoji: '🔒',
    description: (
      <>
        Fully static site — no accounts, no backend, no tracking. Your progress,
        mastery, and mock-exam history live in your browser and are yours to
        export. Works offline.
      </>
    ),
  },
];

function Feature({title, emoji, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <span className={styles.featureEmoji} role="img" aria-hidden="true">
          {emoji}
        </span>
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
