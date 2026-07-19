import React, {useEffect, useRef, useState} from 'react';
import Layout from '@theme/Layout';
import {
  exportAll,
  getMockState,
  getProgress,
  getSettings,
  importAll,
  resetAll,
  setSettings,
} from '@site/src/lib/storage';

function Row({children}: {children: React.ReactNode}) {
  return <div style={{margin: '1.25rem 0'}}>{children}</div>;
}

export default function SettingsPage(): React.ReactElement {
  const [doq, setDoq] = useState(false);
  const [stats, setStats] = useState({answered: 0, mocks: 0});
  const [msg, setMsg] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const refresh = () => {
    setDoq(getSettings().doqIntegration);
    setStats({
      answered: Object.keys(getProgress().questions).length,
      mocks: getMockState().attempts.length,
    });
  };
  useEffect(refresh, []);

  return (
    <Layout title="Settings" description="CertiQ settings: data export/import and optional integrations.">
      <main className="container margin-vert--lg" style={{maxWidth: 760}}>
        <h1>Settings</h1>
        <p>
          CertiQ stores everything locally in your browser — there is no
          account and no server. These controls manage that local data and
          optional integrations.
        </p>

        <h2>Optional integration: doQumentation</h2>
        <Row>
          <label style={{display: 'flex', gap: '0.6rem', alignItems: 'flex-start', cursor: 'pointer'}}>
            <input
              type="checkbox"
              checked={doq}
              onChange={(e) => {
                setSettings({doqIntegration: e.target.checked});
                setDoq(e.target.checked);
              }}
              style={{marginTop: '0.25rem'}}
            />
            <span>
              <strong>Enable doQumentation companion links</strong> (off by
              default). Section pages will additionally link to{' '}
              <a href="https://doqumentation.org" target="_blank" rel="noopener noreferrer">
                doqumentation.org
              </a>{' '}
              — an independent community mirror of the official Qiskit docs
              with in-browser code execution (RasQberry project). Nothing is
              sent anywhere by enabling this; it only adds links.{' '}
              <em>Experimental: executing question code inside CertiQ via the
              same public infrastructure is planned.</em>
            </span>
          </label>
        </Row>

        <h2>Your data</h2>
        <Row>
          <p>
            {stats.answered} question(s) attempted · {stats.mocks} mock exam(s)
            recorded — all in <code>localStorage</code>.
          </p>
          <div style={{display: 'flex', gap: '0.75rem', flexWrap: 'wrap'}}>
            <button
              type="button"
              className="button button--primary"
              onClick={() => {
                const blob = new Blob([exportAll()], {type: 'application/json'});
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = `certiq-progress-${new Date().toISOString().slice(0, 10)}.json`;
                a.click();
                URL.revokeObjectURL(a.href);
              }}>
              Export progress (JSON)
            </button>
            <button
              type="button"
              className="button button--secondary"
              onClick={() => fileRef.current?.click()}>
              Import progress
            </button>
            <input
              ref={fileRef}
              type="file"
              accept="application/json"
              style={{display: 'none'}}
              onChange={async (e) => {
                const f = e.target.files?.[0];
                if (!f) {
                  return;
                }
                const res = importAll(await f.text());
                setMsg(res.ok ? 'Import successful.' : `Import failed: ${res.error}`);
                refresh();
                e.target.value = '';
              }}
            />
            <button
              type="button"
              className="button button--danger"
              onClick={() => {
                // eslint-disable-next-line no-alert
                if (window.confirm('Delete ALL local CertiQ data (progress, mock history, settings)?')) {
                  resetAll();
                  setMsg('All local data deleted.');
                  refresh();
                }
              }}>
              Reset everything
            </button>
          </div>
          {msg ? <p style={{marginTop: '0.75rem'}}>{msg}</p> : null}
        </Row>

        <h2>About the content</h2>
        <p>
          Questions are AI-generated at build time from the public exam
          objectives and official documentation, execution-verified against a
          pinned Qiskit 2.x stack, and adversarially reviewed. Found something
          off?{' '}
          <a
            href="https://github.com/JanLahmann/qiskit-developer-certification-prep/issues/new"
            target="_blank"
            rel="noopener noreferrer">
            Open an issue
          </a>{' '}
          — human feedback is very welcome.
        </p>
      </main>
    </Layout>
  );
}
