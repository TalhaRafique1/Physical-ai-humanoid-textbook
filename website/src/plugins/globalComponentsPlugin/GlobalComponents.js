import React from 'react';
import ChatWidget from '../../components/ChatWidget/ChatWidget';
import TranslationToggle from '../../components/TranslationToggle/TranslationToggle';

function GlobalComponents() {
  return (
    <>
      {/* AI Chat Widget - appears on all pages */}
      <ChatWidget />

      {/* Translation Toggle - appears on all pages */}
      <div style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 1001 }}>
        <TranslationToggle />
      </div>
    </>
  );
}

export default GlobalComponents;