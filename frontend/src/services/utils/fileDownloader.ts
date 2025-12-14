/**
 * File Download Utilities
 *
 * This module provides utility functions for downloading files in the textbook generation system.
 */

/**
 * Downloads a file from a given URL with a specified filename
 * @param url - The URL of the file to download
 * @param filename - The name to save the file as
 */
export const downloadFileFromUrl = (url: string, filename: string): void => {
  // Create a temporary link element
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.target = '_blank'; // Open in new tab for better UX with large files

  // Append to the body, click, and remove
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Downloads a file from a Blob object with a specified filename
 * @param blob - The Blob object containing the file data
 * @param filename - The name to save the file as
 */
export const downloadFileFromBlob = (blob: Blob, filename: string): void => {
  // Create a URL for the blob
  const url = URL.createObjectURL(blob);

  // Use the URL to download the file
  downloadFileFromUrl(url, filename);

  // Clean up the URL to free memory
  URL.revokeObjectURL(url);
};

/**
 * Downloads a file from a base64 encoded string with a specified filename and content type
 * @param base64String - The base64 encoded file data
 * @param filename - The name to save the file as
 * @param contentType - The MIME type of the file
 */
export const downloadFileFromBase64 = (base64String: string, filename: string, contentType: string): void => {
  // Remove the data URL prefix if present
  const base64Data = base64String.replace(/^data:.*;base64,/, '');

  // Convert base64 to binary data
  const binaryString = atob(base64Data);
  const bytes = new Uint8Array(binaryString.length);

  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  // Create a Blob with the binary data
  const blob = new Blob([bytes], { type: contentType });

  // Download the blob
  downloadFileFromBlob(blob, filename);
};

/**
 * Downloads a text file with specified content and filename
 * @param content - The text content to save
 * @param filename - The name to save the file as
 * @param contentType - The MIME type of the file (default: text/plain)
 */
export const downloadTextFile = (content: string, filename: string, contentType: string = 'text/plain'): void => {
  // Create a Blob with the text content
  const blob = new Blob([content], { type: contentType });

  // Download the blob
  downloadFileFromBlob(blob, filename);
};

/**
 * Downloads a JSON file with specified data and filename
 * @param data - The JSON-serializable data to save
 * @param filename - The name to save the file as
 */
export const downloadJsonFile = (data: any, filename: string): void => {
  // Convert the data to a formatted JSON string
  const jsonString = JSON.stringify(data, null, 2);

  // Download as text file with JSON content type
  downloadTextFile(jsonString, filename, 'application/json');
};

/**
 * Downloads an array of data as a CSV file
 * @param data - Array of objects to convert to CSV
 * @param filename - The name to save the file as
 * @param headers - Optional array of column headers (if not provided, uses object keys from first row)
 */
export const downloadCsvFile = (data: any[], filename: string, headers?: string[]): void => {
  if (data.length === 0) {
    console.warn('Cannot create CSV from empty data array');
    return;
  }

  // Determine headers if not provided
  const csvHeaders = headers || Object.keys(data[0]);

  // Create CSV content
  let csvContent = csvHeaders.join(',') + '\n';

  for (const row of data) {
    const csvRow = csvHeaders.map(header => {
      const value = row[header] !== undefined ? row[header] : '';
      // Escape commas and quotes in values
      const escapedValue = String(value).replace(/"/g, '""');
      return `"${escapedValue}"`;
    }).join(',');

    csvContent += csvRow + '\n';
  }

  // Download as text file with CSV content type
  downloadTextFile(csvContent, filename, 'text/csv');
};

/**
 * Downloads a file with progress tracking
 * @param url - The URL of the file to download
 * @param filename - The name to save the file as
 * @param onProgress - Optional callback to track download progress (0-1)
 */
export const downloadFileWithProgress = async (
  url: string,
  filename: string,
  onProgress?: (progress: number) => void
): Promise<void> => {
  try {
    // Fetch the file with progress tracking
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const contentLength = response.headers.get('content-length');
    const total = parseInt(contentLength || '0', 10);
    let loaded = 0;

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Could not get response reader');
    }

    const chunks: Uint8Array[] = [];

    // Read the response in chunks to track progress
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      chunks.push(value);
      loaded += value.length;

      // Report progress if callback provided
      if (onProgress && total > 0) {
        onProgress(loaded / total);
      }
    }

    // Combine all chunks into a single Uint8Array
    const allChunks = new Uint8Array(loaded);
    let position = 0;

    for (const chunk of chunks) {
      allChunks.set(chunk, position);
      position += chunk.length;
    }

    // Create a blob from the combined chunks
    const blob = new Blob([allChunks]);

    // Download the blob
    downloadFileFromBlob(blob, filename);

    // Report completion
    if (onProgress) {
      onProgress(1);
    }
  } catch (error) {
    console.error('Error downloading file with progress:', error);
    throw error;
  }
};

/**
 * Checks if a file type is supported for download
 * @param filename - The name of the file to check
 * @returns True if the file type is supported, false otherwise
 */
export const isSupportedFileType = (filename: string): boolean => {
  const supportedTypes = [
    '.pdf', '.docx', '.epub', '.html', '.txt',
    '.json', '.csv', '.xml', '.md', '.rtf'
  ];

  const fileExtension = filename.toLowerCase().substring(filename.lastIndexOf('.'));
  return supportedTypes.includes(fileExtension);
};

/**
 * Gets the MIME type for a given file extension
 * @param filename - The name of the file
 * @returns The MIME type for the file
 */
export const getMimeTypeForFile = (filename: string): string => {
  const extension = filename.toLowerCase().substring(filename.lastIndexOf('.'));

  const mimeTypes: Record<string, string> = {
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.epub': 'application/epub+zip',
    '.html': 'text/html',
    '.txt': 'text/plain',
    '.json': 'application/json',
    '.csv': 'text/csv',
    '.xml': 'application/xml',
    '.md': 'text/markdown',
    '.rtf': 'application/rtf'
  };

  return mimeTypes[extension] || 'application/octet-stream';
};

/**
 * Generates a safe filename by removing potentially problematic characters
 * @param filename - The original filename
 * @returns A safe filename with problematic characters removed
 */
export const generateSafeFilename = (filename: string): string => {
  // Remove potentially problematic characters
  let safeFilename = filename.replace(/[<>:"/\\|?*]/g, '_');

  // Limit length to prevent issues with file systems
  if (safeFilename.length > 200) {
    const lastDotIndex = safeFilename.lastIndexOf('.');
    if (lastDotIndex !== -1) {
      const name = safeFilename.substring(0, lastDotIndex);
      const extension = safeFilename.substring(lastDotIndex);
      safeFilename = name.substring(0, 190) + extension;
    } else {
      safeFilename = safeFilename.substring(0, 200);
    }
  }

  return safeFilename;
};