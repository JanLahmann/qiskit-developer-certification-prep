/**
 * Minimal inline-markdown renderer for question text.
 *
 * Generated stems/options/explanations are constrained to a small dialect:
 * `inline code`, **bold**, *italic*. Anything heavier belongs in the
 * question's dedicated `code` block (rendered with the site CodeBlock).
 * Deliberately not a full markdown engine — predictable output, no deps.
 */

import React, {type ReactNode} from 'react';

const TOKEN = /(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/g;

export function renderInline(text: string): ReactNode[] {
  const parts = text.split(TOKEN);
  return parts.map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`') && part.length > 2) {
      return <code key={i}>{part.slice(1, -1)}</code>;
    }
    if (part.startsWith('**') && part.endsWith('**') && part.length > 4) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('*') && part.endsWith('*') && part.length > 2) {
      return <em key={i}>{part.slice(1, -1)}</em>;
    }
    return <React.Fragment key={i}>{part}</React.Fragment>;
  });
}
