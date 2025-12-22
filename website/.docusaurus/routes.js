import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '304'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '9de'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'd40'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', '3d8'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '4c2'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', 'e6b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '72f'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '344'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'b4a'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'c53'),
            routes: [
              {
                path: '/docs/applications/chapter-1-industrial-applications',
                component: ComponentCreator('/docs/applications/chapter-1-industrial-applications', 'a7d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/applications/chapter-2-healthcare-applications',
                component: ComponentCreator('/docs/applications/chapter-2-healthcare-applications', '88f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/applications/chapter-3-domestic-applications',
                component: ComponentCreator('/docs/applications/chapter-3-domestic-applications', '5c7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/future-perspectives/chapter-1-technological-advances',
                component: ComponentCreator('/docs/future-perspectives/chapter-1-technological-advances', '317'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/future-perspectives/chapter-2-societal-implications',
                component: ComponentCreator('/docs/future-perspectives/chapter-2-societal-implications', 'f9a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/getting-started/introduction',
                component: ComponentCreator('/docs/getting-started/introduction', 'd6c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/getting-started/setup',
                component: ComponentCreator('/docs/getting-started/setup', '754'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/humanoid-robotics/chapter-1-introduction-to-humanoids',
                component: ComponentCreator('/docs/humanoid-robotics/chapter-1-introduction-to-humanoids', '1c0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/humanoid-robotics/chapter-2-bipedal-locomotion',
                component: ComponentCreator('/docs/humanoid-robotics/chapter-2-bipedal-locomotion', '77d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/humanoid-robotics/chapter-3-humanoid-manipulation',
                component: ComponentCreator('/docs/humanoid-robotics/chapter-3-humanoid-manipulation', '2c1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/humanoid-robotics/chapter-4-humanoid-intelligence',
                component: ComponentCreator('/docs/humanoid-robotics/chapter-4-humanoid-intelligence', 'ed8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'aed'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/physical-ai/chapter-1-introduction',
                component: ComponentCreator('/docs/physical-ai/chapter-1-introduction', '2c6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/physical-ai/chapter-2-sensing-and-perception',
                component: ComponentCreator('/docs/physical-ai/chapter-2-sensing-and-perception', '0a5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/physical-ai/chapter-3-motion-and-control',
                component: ComponentCreator('/docs/physical-ai/chapter-3-motion-and-control', 'f1f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/physical-ai/chapter-4-learning-and-adaptation',
                component: ComponentCreator('/docs/physical-ai/chapter-4-learning-and-adaptation', 'dca'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/physical-ai/chapter-5-human-robot-interaction',
                component: ComponentCreator('/docs/physical-ai/chapter-5-human-robot-interaction', '443'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/physical-ai/chapter-6-embodiment-and-cognition',
                component: ComponentCreator('/docs/physical-ai/chapter-6-embodiment-and-cognition', '793'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/summary',
                component: ComponentCreator('/docs/summary', '07e'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'c36'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
