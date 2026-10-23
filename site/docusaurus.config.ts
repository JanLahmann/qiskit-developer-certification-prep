import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import {familyFooterColumn} from './family-footer';

// Prism github/dracula with token colors darkened/lightened to WCAG AA (4.5:1)
// against their code-block backgrounds; Lighthouse flagged the stock ones.
const AA_LIGHT: Record<string, string> = {
  '#999988': '#57606a', // comment
  '#e3116c': '#b3125a', // string
  '#36acaa': '#0f7b78', // number, boolean, constant, ...
  '#00a4db': '#006b9a', // atrule, attr-name
  '#d73a49': '#c02d3a', // function, tag
};
const lightCodeTheme = {
  ...prismThemes.github,
  styles: prismThemes.github.styles.map((s) => ({
    ...s,
    style: {...s.style, color: AA_LIGHT[s.style.color ?? ''] ?? s.style.color},
  })),
};
const darkCodeTheme = {
  ...prismThemes.dracula,
  styles: prismThemes.dracula.styles.map((s) => ({
    ...s,
    style: s.types.includes('comment') ? {...s.style, color: '#8b9bd0'} : s.style,
  })),
};

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'CertiQ',
  tagline:
    'Machine-verified prep for the IBM Qiskit v2.x Developer certification (C1000-179). Unofficial — not affiliated with IBM.',
  favicon: 'favicon.ico', // + apple-touch-icon.png; both from pipeline/make_icons.py

  future: {
    v4: true,
  },

  url: 'https://certiq.dev',
  baseUrl: '/',
  trailingSlash: false,

  // GitHub pages deployment config.
  organizationName: 'JanLahmann',
  projectName: 'qiskit-developer-certification-prep',

  onBrokenLinks: 'throw',

  // Umami analytics — shared Fun with Quantum family property (cookie-free, no consent banner).
  // data-domains keeps local and preview builds out of the numbers. The family-standard guard runs
  // first: it drops headless browsers and crawlers (data-before-send), and ?notrack / ?track turn
  // tracking off / on again for this browser (localStorage umami.disabled). Custom events:
  // src/lib/analytics.ts and src/clientModules/linkEvents.ts.
  headTags: [
    {tagName: 'link', attributes: {rel: 'apple-touch-icon', href: '/apple-touch-icon.png'}},
    {
      tagName: 'script',
      attributes: {},
      innerHTML:
        "(function(){try{var q=location.search;if(/[?&]notrack\\b/.test(q))localStorage.setItem('umami.disabled','1');if(/[?&]track\\b/.test(q))localStorage.removeItem('umami.disabled')}catch(e){}window.fwqUmamiBeforeSend=function(t,p){var n=navigator;return(n.webdriver||/HeadlessChrome|bot|crawl|spider|Lighthouse|PageSpeed/i.test(n.userAgent))?false:p}})();",
    },
    {
      tagName: 'script',
      attributes: {
        defer: true,
        src: 'https://cloud.umami.is/script.js',
        'data-website-id': '97f347ac-e7ba-4be3-b26f-ab4b328bdbf2',
        'data-domains': 'certiq.dev',
        'data-before-send': 'fwqUmamiBeforeSend',
      },
    },
  ],
  clientModules: ['./src/clientModules/linkEvents.ts'],

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/JanLahmann/qiskit-developer-certification-prep/tree/main/site/',
          // git last-commit dates; they also feed the sitemap's <lastmod> (needs full history in CI)
          showLastUpdateTime: true,
        },
        blog: false,
        sitemap: {
          lastmod: 'date',
          ignorePatterns: ['/settings'],
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'CertiQ',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'studySidebar',
          position: 'left',
          label: 'Study Guide',
        },
        {to: '/mock-exam', label: 'Mock Exam', position: 'left'},
        {
          href: 'https://github.com/JanLahmann/qiskit-developer-certification-prep',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Study',
          items: [
            {
              label: 'Start here',
              to: '/docs/intro',
            },
            {
              label: 'Guided path',
              to: '/docs/path',
            },
            {
              label: 'Mock exam',
              to: '/mock-exam',
            },
            {
              label: 'Settings & your data',
              to: '/settings',
            },
          ],
        },
        {
          title: 'Official IBM resources',
          items: [
            {
              label: 'Exam page (C1000-179)',
              href: 'https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400',
            },
            {
              label: 'IBM Quantum documentation',
              href: 'https://quantum.cloud.ibm.com/docs',
            },
            {
              label: 'IBM Quantum Learning',
              href: 'https://quantum.cloud.ibm.com/learning',
            },
          ],
        },
        {
          title: 'Project',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/JanLahmann/qiskit-developer-certification-prep',
            },
          ],
        },
        // + "Fun with Quantum family" column, appended by createConfig() below.
      ],
      copyright: `Unofficial community project — not affiliated with, endorsed by, or sponsored by IBM. Qiskit is a trademark of IBM. Practice content is generated from public exam objectives and open documentation, never from actual exam content. Code Apache-2.0 · content CC BY-SA 4.0.`,
    },
    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
      additionalLanguages: ['python', 'json', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

// Async config: the family footer column comes from the shared manifest at build time.
export default async function createConfig(): Promise<Config> {
  const themeConfig = config.themeConfig as {footer: {links: unknown[]}};
  themeConfig.footer.links.push(await familyFooterColumn('certiq'));
  return config;
}
