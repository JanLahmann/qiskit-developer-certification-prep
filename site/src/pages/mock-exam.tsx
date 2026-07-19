import React from 'react';
import Layout from '@theme/Layout';
import MockExam from '@site/src/components/Exam/MockExam';

export default function MockExamPage(): React.ReactElement {
  return (
    <Layout
      title="Mock exam"
      description="Faithful C1000-179 simulator: 68 questions, 90 minutes, pass at 47 — sampled by official section weights from the verified question bank.">
      <MockExam />
    </Layout>
  );
}
