import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/ur/docs',
    component: ComponentCreator('/ur/docs', '4e8'),
    routes: [
      {
        path: '/ur/docs',
        component: ComponentCreator('/ur/docs', '468'),
        routes: [
          {
            path: '/ur/docs',
            component: ComponentCreator('/ur/docs', '5bb'),
            routes: [
              {
                path: '/ur/docs/applications/chapter-1-industrial-applications',
                component: ComponentCreator('/ur/docs/applications/chapter-1-industrial-applications', 'f21'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/applications/chapter-2-healthcare-applications',
                component: ComponentCreator('/ur/docs/applications/chapter-2-healthcare-applications', '8c4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/applications/chapter-3-domestic-applications',
                component: ComponentCreator('/ur/docs/applications/chapter-3-domestic-applications', 'ab8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/future-perspectives/chapter-1-technological-advances',
                component: ComponentCreator('/ur/docs/future-perspectives/chapter-1-technological-advances', '4ca'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/future-perspectives/chapter-2-societal-implications',
                component: ComponentCreator('/ur/docs/future-perspectives/chapter-2-societal-implications', '783'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/getting-started/introduction',
                component: ComponentCreator('/ur/docs/getting-started/introduction', 'bc9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/getting-started/setup',
                component: ComponentCreator('/ur/docs/getting-started/setup', 'e8e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/humanoid-robotics/chapter-1-introduction-to-humanoids',
                component: ComponentCreator('/ur/docs/humanoid-robotics/chapter-1-introduction-to-humanoids', '5f8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/humanoid-robotics/chapter-2-bipedal-locomotion',
                component: ComponentCreator('/ur/docs/humanoid-robotics/chapter-2-bipedal-locomotion', '8c9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/humanoid-robotics/chapter-3-humanoid-manipulation',
                component: ComponentCreator('/ur/docs/humanoid-robotics/chapter-3-humanoid-manipulation', '555'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/humanoid-robotics/chapter-4-humanoid-intelligence',
                component: ComponentCreator('/ur/docs/humanoid-robotics/chapter-4-humanoid-intelligence', '3d5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/intro',
                component: ComponentCreator('/ur/docs/intro', '7af'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/physical-ai/chapter-1-introduction',
                component: ComponentCreator('/ur/docs/physical-ai/chapter-1-introduction', 'e22'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/physical-ai/chapter-2-sensing-and-perception',
                component: ComponentCreator('/ur/docs/physical-ai/chapter-2-sensing-and-perception', '3d7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/physical-ai/chapter-3-motion-and-control',
                component: ComponentCreator('/ur/docs/physical-ai/chapter-3-motion-and-control', '7d5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/physical-ai/chapter-4-learning-and-adaptation',
                component: ComponentCreator('/ur/docs/physical-ai/chapter-4-learning-and-adaptation', '4fa'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/physical-ai/chapter-5-human-robot-interaction',
                component: ComponentCreator('/ur/docs/physical-ai/chapter-5-human-robot-interaction', 'f4d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/physical-ai/chapter-6-embodiment-and-cognition',
                component: ComponentCreator('/ur/docs/physical-ai/chapter-6-embodiment-and-cognition', 'dcc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/ur/docs/summary',
                component: ComponentCreator('/ur/docs/summary', 'e34'),
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
    path: '/ur/',
    component: ComponentCreator('/ur/', 'f66'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
