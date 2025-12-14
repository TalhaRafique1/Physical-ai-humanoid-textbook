import React, { useState, useEffect } from 'react';

interface ExportOption {
  id: string;
  name: string;
  extension: string;
  description: string;
  isDefault: boolean;
}

interface ExportOptionsProps {
  textbookId: string;
  onExport: (format: string) => void;
  availableFormats?: ExportOption[];
}

const ExportOptions: React.FC<ExportOptionsProps> = ({ textbookId, onExport, availableFormats }) => {
  const [formats, setFormats] = useState<ExportOption[]>(availableFormats || []);
  const [selectedFormat, setSelectedFormat] = useState<string>('PDF');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // In a real implementation, this would fetch available formats from the backend
  useEffect(() => {
    if (!availableFormats || availableFormats.length === 0) {
      // Default formats if not provided
      const defaultFormats: ExportOption[] = [
        { id: 'format_pdf', name: 'PDF', extension: '.pdf', description: 'Portable Document Format', isDefault: true },
        { id: 'format_docx', name: 'DOCX', extension: '.docx', description: 'Microsoft Word Document', isDefault: false },
        { id: 'format_epub', name: 'EPUB', extension: '.epub', description: 'Electronic Publication', isDefault: false },
        { id: 'format_html', name: 'HTML', extension: '.html', description: 'HyperText Markup Language', isDefault: false },
        { id: 'format_txt', name: 'TXT', extension: '.txt', description: 'Plain Text', isDefault: false }
      ];
      setFormats(defaultFormats);
      setSelectedFormat('PDF');
    } else {
      setFormats(availableFormats);
      if (availableFormats.length > 0) {
        const defaultFormat = availableFormats.find(f => f.isDefault) || availableFormats[0];
        setSelectedFormat(defaultFormat.name);
      }
    }
  }, [availableFormats]);

  const handleExport = async () => {
    if (!textbookId) {
      setError('No textbook selected for export');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // In a real implementation, this would call the backend export API
      // For now, we'll just call the onExport callback
      onExport(selectedFormat);
    } catch (err) {
      setError('Export failed. Please try again.');
      console.error('Export error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="export-options" role="region" aria-labelledby="export-options-title">
      <h3 id="export-options-title">Export Options</h3>

      {error && (
        <div className="error-message" role="alert" aria-live="polite">
          {error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="export-format">Select Format:</label>
        <select
          id="export-format"
          value={selectedFormat}
          onChange={(e) => setSelectedFormat(e.target.value)}
          aria-describedby="export-format-help"
        >
          {formats.map(format => (
            <option key={format.id} value={format.name}>
              {format.name} ({format.extension}) - {format.description}
            </option>
          ))}
        </select>
        <small id="export-format-help" className="form-help">Select the format for textbook export</small>
      </div>

      <div className="export-info">
        <p><strong>Selected Textbook:</strong> {textbookId}</p>
        <p>Select the format in which you want to export your textbook.</p>
      </div>

      <button
        onClick={handleExport}
        disabled={loading}
        className="export-button"
        aria-busy={loading}
        aria-describedby="export-button-help"
      >
        {loading ? 'Exporting...' : `Export as ${selectedFormat}`}
      </button>
      <small id="export-button-help" className="form-help">Click to export the textbook in selected format</small>

      <div className="export-notes" aria-label="Export format information">
        <h4>Format Information:</h4>
        <ul>
          <li><strong>PDF:</strong> Best for printing and universal compatibility</li>
          <li><strong>DOCX:</strong> Editable in Microsoft Word and similar applications</li>
          <li><strong>EPUB:</strong> Ideal for e-readers and mobile devices</li>
          <li><strong>HTML:</strong> Web-friendly format for online viewing</li>
          <li><strong>TXT:</strong> Simple text format, universally readable</li>
        </ul>
      </div>
    </div>
  );
};

export default ExportOptions;