// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: ['getting-started/introduction', 'getting-started/setup'],
    },
    {
      type: 'category',
      label: 'Physical AI',
      items: [
        'physical-ai/chapter-1-introduction',
        'physical-ai/chapter-2-sensing-and-perception',
        'physical-ai/chapter-3-motion-and-control',
        'physical-ai/chapter-4-learning-and-adaptation',
        'physical-ai/chapter-5-human-robot-interaction',
        'physical-ai/chapter-6-embodiment-and-cognition',
      ],
    },
    {
      type: 'category',
      label: 'Humanoid Robotics',
      items: [
        'humanoid-robotics/chapter-1-introduction-to-humanoids',
        'humanoid-robotics/chapter-2-bipedal-locomotion',
        'humanoid-robotics/chapter-3-humanoid-manipulation',
        'humanoid-robotics/chapter-4-humanoid-intelligence',
      ],
    },
    {
      type: 'category',
      label: 'Applications',
      items: [
        'applications/chapter-1-industrial-applications',
        'applications/chapter-2-healthcare-applications',
        'applications/chapter-3-domestic-applications',
      ],
    },
    {
      type: 'category',
      label: 'Future Perspectives',
      items: [
        'future-perspectives/chapter-1-technological-advances',
        'future-perspectives/chapter-2-societal-implications',
      ],
    },
    {
      type: 'category',
      label: 'Summary',
      items: [
        'summary',
      ],
    },
  ],
};

export default sidebars;