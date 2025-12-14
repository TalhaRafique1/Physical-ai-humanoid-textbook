import React from 'react';
import Layout from '@theme/Layout';
import ChatWidget from '../ChatWidget/ChatWidget';
import TranslationToggle from '../TranslationToggle/TranslationToggle';

function LayoutWrapper(props) {
  return (
    <Layout {...props}>
      {/* Add the AI Chat Widget */}
      <ChatWidget />

      {/* Add the Translation Toggle */}
      <div style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 1001 }}>
        <TranslationToggle />
      </div>

      {/* Render the original page content */}
      {props.children}
    </Layout>
  );
}

export default LayoutWrapper;