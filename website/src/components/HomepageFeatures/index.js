import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Physical AI Fundamentals',
    description: (
      <>
        Learn the core principles of Physical AI, including sensing, perception,
        motion control, and embodied cognition that differentiate it from traditional AI.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    description: (
      <>
        Explore the fascinating world of humanoid robots, from bipedal locomotion
        and manipulation to intelligence and social interaction.
      </>
    ),
  },
  {
    title: 'Interactive Learning',
    description: (
      <>
        Engage with AI-powered learning tools, including our integrated chatbot
        that provides personalized assistance throughout your learning journey.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}