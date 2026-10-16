import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Head from '@docusaurus/Head';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import ProgressOverview from '@site/src/components/Progress/ProgressOverview';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          Pass the Qiskit v2.x Developer certification
        </Heading>
        <p className="hero__subtitle">
          A guided, machine-verified prep platform for IBM exam C1000-179 —
          68 questions, 90 minutes, 47 to pass. Every practice question is
          executed and proven against a pinned Qiskit 2.x stack at build time.
        </p>
        <div className={styles.buttons}>
          <Link className="button button--secondary button--lg" to="/docs/intro">
            Start preparing →
          </Link>
        </div>
      </div>
    </header>
  );
}

// schema.org: lets search engines show CertiQ as a free learning resource for
// the certification. Facts only — no ratings, no claims of IBM affiliation.
const STRUCTURED_DATA = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'WebSite',
      name: 'CertiQ',
      url: 'https://certiq.dev/',
    },
    {
      '@type': 'LearningResource',
      name: 'CertiQ — Qiskit v2.x Developer certification prep',
      url: 'https://certiq.dev/',
      description:
        'Unofficial, free prep for IBM exam C1000-179: guided study path, machine-verified question bank, and a mock exam that follows the official section weights.',
      isAccessibleForFree: true,
      inLanguage: 'en',
      learningResourceType: ['Practice exam', 'Study guide', 'Flashcards'],
      educationalLevel: 'Professional',
      teaches: 'Qiskit SDK v2.x and Qiskit Runtime',
      about: {
        '@type': 'EducationalOccupationalCredential',
        name: 'IBM Certified Quantum Computation using Qiskit v2.X Developer - Associate (C1000-179)',
      },
    },
  ],
};

export default function Home(): ReactNode {
  return (
    <Layout
      title="Qiskit Developer Certification (C1000-179) Prep"
      description="Unofficial, machine-verified prep platform for the IBM Qiskit v2.x Developer certification (C1000-179): guided study path, verified question bank, faithful mock exam.">
      <Head>
        <script type="application/ld+json">{JSON.stringify(STRUCTURED_DATA)}</script>
      </Head>
      <HomepageHeader />
      <main>
        <div className="container">
          <ProgressOverview compact />
        </div>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
