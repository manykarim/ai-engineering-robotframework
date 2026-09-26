// The workshop site: the repository's own Markdown, rendered where it lives (spec: workshop/docs-site, design D6).
// One docs plugin rooted at the repository keeps every relative link between the rendered files resolvable.
const {themes} = require('prism-react-renderer');

const REPO = 'https://github.com/manykarim/ai-engineering-robotframework';

module.exports = {
  title: 'Agentic Engineering with Robot Framework',
  tagline: 'From a Markdown file to a self-healing pipeline',
  url: 'https://manykarim.github.io',
  baseUrl: '/ai-engineering-robotframework/',
  organizationName: 'manykarim',
  projectName: 'ai-engineering-robotframework',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',
  markdown: {
    // .md is CommonMark: ${VARIABLE} and HTML comments in prose stay as written.
    format: 'detect',
    hooks: {
      onBrokenMarkdownLinks: 'throw',
      onBrokenMarkdownImages: 'throw',
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: '..',
          routeBasePath: '/',
          include: [
            'README.md',
            'SETUP.md',
            'GLOSSARY.md',
            'labs/**/*.md',
            'docs/**/*.md',
            'transcripts/**/*.md',
          ],
          exclude: ['**/node_modules/**', 'website/**'],
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: `${REPO}/edit/main/`,
        },
        blog: false,
        theme: {customCss: require.resolve('./src/css/custom.css')},
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Agentic Engineering with Robot Framework',
      items: [
        {type: 'doc', docId: 'labs/README', label: 'Labs', position: 'left'},
        {type: 'doc', docId: 'SETUP', label: 'Setup', position: 'left'},
        {type: 'doc', docId: 'GLOSSARY', label: 'Glossary', position: 'left'},
        {href: REPO, label: 'GitHub', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      copyright: 'Built by the community, for the community. Fork it, break it, heal it.',
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['bash', 'toml', 'json', 'diff'],
    },
  },
};
