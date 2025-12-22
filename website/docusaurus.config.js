// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI-Native Textbook for Physical AI & Humanoid Robotics',
  tagline: 'Interactive, intelligent textbook powered by AI by Talha Rafique',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-website-domain.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'ai-textbook-project', // Usually your GitHub org/user name.
  projectName: 'textbook', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/ai-textbook-project/textbook/tree/main/website/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  plugins: [
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/book-logo.png',
      navbar: {
        title: 'AI Textbook',
        logo: {
          alt: 'AI Textbook Logo',
          src: 'img/book-logo.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Textbook',
          },
          {
            href: 'https://github.com/ai-textbook-project/textbook',
            label: 'GitHub',
            position: 'right',
          },
          {
            type: 'localeDropdown',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook Sections',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Getting Started',
                to: '/docs/getting-started/introduction',
              },
              {
                label: 'Physical AI',
                to: '/docs/physical-ai/chapter-1-introduction',
              },
              {
                label: 'Humanoid Robotics',
                to: '/docs/humanoid-robotics/chapter-1-introduction-to-humanoids',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Documentation',
                to: '/docs/intro',
              },
              {
                label: 'Research Papers',
                href: 'https://scholar.google.com',
              },
              {
                label: 'Tutorials',
                to: '/docs/getting-started/introduction',
              },
              {
                label: 'API Reference',
                href: '#',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/ai-textbook-project/textbook',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Applications',
                to: '/docs/applications/chapter-1-industrial-applications',
              },
              {
                label: 'Future Perspectives',
                to: '/docs/future-perspectives/chapter-1-technological-advances',
              },
              {
                label: 'Contributing',
                href: 'https://github.com/ai-textbook-project/textbook/blob/main/CONTRIBUTING.md',
              },
              {
                label: 'GitHub Repository',
                href: 'https://github.com/ai-textbook-project/textbook',
              },
            ],
          },
        ],
        copyright: `<div style="display: flex; flex-direction: column; align-items: center;"><span>Copyright © ${new Date().getFullYear()} AI-Native Textbook for Physical AI & Humanoid Robotics. Built with Docusaurus.</span><div style="margin-top: 10px;">Made with ❤️ for the AI community by Talha Rafique</div></div>`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;