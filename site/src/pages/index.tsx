import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
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

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Unofficial, machine-verified prep platform for the IBM Qiskit v2.x Developer certification (C1000-179): guided study path, verified question bank, faithful mock exam.">
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
