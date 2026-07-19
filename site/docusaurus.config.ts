import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'CertiQ',
  tagline:
    'Machine-verified prep for the IBM Qiskit v2.x Developer certification (C1000-179). Unofficial — not affiliated with IBM.',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://janlahmann.github.io',
  baseUrl: '/qiskit-developer-certification-prep/',
  trailingSlash: false,

  // GitHub pages deployment config.
  organizationName: 'JanLahmann',
  projectName: 'qiskit-developer-certification-prep',

  onBrokenLinks: 'throw',

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
        },
        blog: false,
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
      ],
      copyright: `Unofficial community project — not affiliated with, endorsed by, or sponsored by IBM. Qiskit is a trademark of IBM. Practice content is generated from public exam objectives and open documentation, never from actual exam content. Code Apache-2.0 · content CC BY-SA 4.0.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'json', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
