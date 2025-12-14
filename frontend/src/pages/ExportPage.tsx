import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import ExportOptions from '../components/TextbookGenerator/ExportOptions';
import { exportApi } from '../services/api/exportApi';
import { Textbook, ExportFormat, ExportStatus, ExportTextbookResponse } from '../types/textbook';

const ExportPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [textbookId, setTextbookId] = useState<string>('');
  const [textbook, setTextbook] = useState<Textbook | null>(null);
  const [availableFormats, setAvailableFormats] = useState<ExportFormat[]>([]);
  const [exportStatus, setExportStatus] = useState<ExportStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [exportResult, setExportResult] = useState<ExportTextbookResponse | null>(null);

  useEffect(() => {
    // Get textbook ID from URL params
    const id = searchParams.get('textbookId') || '';
    if (id) {
      setTextbookId(id);
      loadTextbookAndFormats(id);
    } else {
      setError('No textbook ID provided. Please go to the generation page first.');
      setLoading(false);
    }
  }, [searchParams]);

  const loadTextbookAndFormats = async (id: string) => {
    try {
      setLoading(true);
      setError(null);

      // Fetch textbook details
      const textbookData = await exportApi.getTextbook(id);
      setTextbook(textbookData);

      // Fetch available export formats
      const formats = await exportApi.getSupportedFormats();
      setAvailableFormats(formats);

      // Fetch export status
      const status = await exportApi.getExportStatus(id);
      setExportStatus(status);
    } catch (err) {
      console.error('Error loading textbook and formats:', err);
      setError('Failed to load textbook information. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (formatName: string) => {
    if (!textbookId) {
      setError('No textbook selected for export');
      return;
    }

    try {
      setError(null);
      const result = await exportApi.exportTextbook(textbookId, formatName);
      setExportResult(result);

      if (result.success) {
        // Refresh export status
        const status = await exportApi.getExportStatus(textbookId);
        setExportStatus(status);
      } else {
        setError(result.message || 'Export failed');
      }
    } catch (err) {
      console.error('Export error:', err);
      setError('Export failed. Please try again.');
    }
  };

  const handleDownload = (formatName: string) => {
    // In a real implementation, this would trigger the download
    // For now, we'll just log the action
    console.log(`Downloading textbook ${textbookId} in ${formatName} format`);

    // Construct download URL
    const downloadUrl = `http://localhost:8000/api/export/download/${textbookId}/${formatName}`;
    window.open(downloadUrl, '_blank');
  };

  if (loading) {
    return (
      <div className="export-page">
        <h2>Export Textbook</h2>
        <p>Loading textbook information...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="export-page">
        <h2>Export Textbook</h2>
        <div className="error-message">
          <p>Error: {error}</p>
          <button onClick={() => window.history.back()}>Go Back</button>
        </div>
      </div>
    );
  }

  return (
    <div className="export-page">
      <h2>Export Textbook</h2>

      {textbook && (
        <div className="textbook-info">
          <h3>Textbook: {textbook.title}</h3>
          <p><strong>Description:</strong> {textbook.description}</p>
          <p><strong>Status:</strong> {textbook.status}</p>
          <p><strong>Chapters:</strong> {textbook.totalChapters}</p>
          <p><strong>Audience:</strong> {textbook.targetAudience}</p>
        </div>
      )}

      {exportResult && exportResult.success && (
        <div className="export-success">
          <h3>Export Successful!</h3>
          <p>Textbook exported as {exportResult.format} format.</p>
          <p>File saved to: {exportResult.outputPath}</p>
          <button onClick={() => handleDownload(exportResult.format)}>
            Download {exportResult.format} File
          </button>
        </div>
      )}

      {exportResult && !exportResult.success && (
        <div className="export-error">
          <h3>Export Failed</h3>
          <p>Error: {exportResult.message}</p>
        </div>
      )}

      <ExportOptions
        textbookId={textbookId}
        onExport={handleExport}
        availableFormats={availableFormats}
      />

      {exportStatus && exportStatus.exportFormats.length > 0 && (
        <div className="previous-exports">
          <h3>Previously Exported Formats</h3>
          <ul>
            {exportStatus.exportFormats.map((format, index) => (
              <li key={index} className="export-format">
                <span>{format}</span>
                <button onClick={() => handleDownload(format)}>
                  Download {format}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="export-actions">
        <button onClick={() => window.location.href = '/'}>
          Back to Home
        </button>
        <button onClick={() => window.location.href = `/generate?textbookId=${textbookId}`}>
          Back to Textbook
        </button>
      </div>
    </div>
  );
};

export default ExportPage;