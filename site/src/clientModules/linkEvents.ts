/**
 * Site-wide link events (one delegated listener, no per-link markup):
 * - "CertiQ: outbound click" {host, category} for links that leave certiq.dev
 * - "CertiQ: file download" {kind, file} for the Anki decks and the EPUB
 * Links that already carry data-umami-event (the family footer) are left to
 * Umami's own click tracking, so nothing is counted twice.
 */
import {track} from '@site/src/lib/analytics';

function category(url: URL): string {
  const host = url.hostname.replace(/^www\./, '');
  if (host === 'ibm.com' && url.pathname.startsWith('/training')) {
    return 'ibm-exam';
  }
  if (host === 'quantum.cloud.ibm.com' || host === 'openqasm.com') {
    return 'docs';
  }
  if (host === 'github.com' || host === 'raw.githubusercontent.com') {
    return 'github';
  }
  if (host === 'doqumentation.org') {
    return 'doqumentation';
  }
  if (/(^|\.)(ankiweb\.net|apple\.com|google\.com|amazon\.com)$/.test(host)) {
    return 'apps';
  }
  return 'other';
}

function onClick(e: MouseEvent): void {
  if (e.type === 'auxclick' && e.button !== 1) {
    return; // only a middle click opens a link; ignore right clicks
  }
  const a = (e.target as Element | null)?.closest?.('a[href]') as HTMLAnchorElement | null;
  if (!a || a.hasAttribute('data-umami-event')) {
    return;
  }
  let url: URL;
  try {
    url = new URL(a.href, location.href);
  } catch {
    return;
  }
  if (url.protocol !== 'http:' && url.protocol !== 'https:') {
    return;
  }
  if (url.host === location.host) {
    const m = url.pathname.match(/^\/downloads\/([\w.-]+\.(apkg|epub))$/);
    if (m) {
      track('file download', {kind: m[2] === 'apkg' ? 'anki' : 'epub', file: m[1]});
    }
    return;
  }
  track('outbound click', {host: url.hostname, category: category(url)});
}

if (typeof document !== 'undefined') {
  // Capture phase, so the event is queued before a same-tab navigation starts.
  document.addEventListener('click', onClick, true);
  document.addEventListener('auxclick', onClick, true);
}
