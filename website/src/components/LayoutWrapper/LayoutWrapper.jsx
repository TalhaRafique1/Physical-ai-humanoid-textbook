import React from 'react';
import Layout from '@theme/Layout';

function LayoutWrapper(props) {
  return (
    <Layout {...props}>
      {/* Render the original page content */}
      {props.children}
    </Layout>
  );
}

export default LayoutWrapper;