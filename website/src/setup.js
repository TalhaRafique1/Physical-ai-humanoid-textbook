// Setup file to polyfill browser globals that may be expected by libraries
// This addresses the "File is not defined" error during build

if (typeof global.File === 'undefined') {
  // Create a minimal File polyfill for Node.js environment
  global.File = class File extends Blob {
    constructor(fileBits, fileName, options = {}) {
      super(fileBits, options);
      this.name = fileName.replace(/\s+/g, '_');
      this.lastModified = options.lastModified || Date.now();
    }
  };
}

if (typeof global.Blob === 'undefined') {
  // Import Blob from node:buffer if not available
  const { Blob } = require('buffer');
  global.Blob = Blob;
}

if (typeof global.FileReader === 'undefined') {
  // Create a minimal FileReader polyfill
  global.FileReader = class FileReader {
    constructor() {
      this.result = null;
      this.readyState = 0; // EMPTY
      this.onload = null;
      this.onerror = null;
    }

    readAsArrayBuffer(blob) {
      this.result = blob.buffer || Buffer.from(blob);
      this.readyState = 2; // DONE
      if (this.onload) this.onload({ target: this });
    }

    readAsDataURL(blob) {
      this.result = `data:${blob.type};base64,${blob.toString('base64')}`;
      this.readyState = 2; // DONE
      if (this.onload) this.onload({ target: this });
    }
  };
}