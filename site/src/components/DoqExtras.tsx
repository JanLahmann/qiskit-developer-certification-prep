/**
 * DoqExtras — optional doQumentation integration (settings-gated, default OFF).
 *
 * When the learner has explicitly enabled the integration in Settings, this
 * renders companion deep links to doqumentation.org (which mirrors the
 * official docs with in-browser execution). Renders nothing otherwise —
 * including during SSR.
 */

import React, {useEffect, useState} from 'react';
import Link from '@docusaurus/Link';
import {getSettings} from '@site/src/lib/storage';

export default function DoqExtras({
  slugs,
}: {
  slugs: string[];
}): React.ReactElement | null {
  const [enabled, setEnabled] = useState(false);
  useEffect(() => {
    setEnabled(getSettings().doqIntegration);
  }, []);

  if (!enabled || slugs.length === 0) {
    return null;
  }
  return (
    <div className="alert alert--info" role="note" style={{marginTop: '0.75rem'}}>
      <strong>doQumentation companion</strong> (enabled in your{' '}
      <Link to="/settings">settings</Link>): read these guides with in-browser
      code execution on{' '}
      {slugs.map((slug, i) => (
        <React.Fragment key={slug}>
          {i > 0 ? ' · ' : ''}
          <a
            href={`https://doqumentation.org/guides/${slug}`}
            target="_blank"
            rel="noopener noreferrer">
            {slug} ↗
          </a>
        </React.Fragment>
      ))}
      <div style={{fontSize: '0.8rem', marginTop: '0.3rem'}}>
        Independent community mirror of the official docs; some pages may not be
        mirrored. Executing question code directly inside CertiQ is planned.
      </div>
    </div>
  );
}
