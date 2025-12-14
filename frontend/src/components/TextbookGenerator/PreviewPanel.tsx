import React, { useState, useEffect } from 'react';
import { TextbookPreview, ChapterPreview } from '../../types/textbook';
import { previewApi } from '../../services/api/previewApi';

interface PreviewPanelProps {
  textbookId?: string;
  initialPreview?: TextbookPreview;
}

const PreviewPanel: React.FC<PreviewPanelProps> = ({ textbookId, initialPreview }) => {
  const [preview, setPreview] = useState<TextbookPreview | null>(initialPreview || null);
  const [chapterPreviews, setChapterPreviews] = useState<ChapterPreview[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<number | null>(null);

  useEffect(() => {
    if (textbookId) {
      loadPreview();
    }
  }, [textbookId]);

  const loadPreview = async () => {
    if (!textbookId) return;

    try {
      setLoading(true);
      setError(null);

      // Load textbook preview
      const textbookPreview = await previewApi.getTextbookPreview(textbookId);
      setPreview(textbookPreview);

      // Load previews for first few chapters
      const chapterNumbers = Array.from({ length: Math.min(3, textbookPreview.totalChapters) }, (_, i) => i + 1);
      const chapterPreviewsData = await previewApi.getMultipleChapterPreviews(textbookId, chapterNumbers);
      setChapterPreviews(chapterPreviewsData);
    } catch (err) {
      console.error('Error loading preview:', err);
      setError('Failed to load preview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChapterSelect = async (chapterNumber: number) => {
    if (!textbookId) return;

    try {
      setLoading(true);
      setError(null);

      const chapterPreview = await previewApi.getChapterPreview(textbookId, chapterNumber);

      // Update the chapter previews list
      setChapterPreviews(prev => {
        const updated = [...prev];
        const index = updated.findIndex(c => c.chapterNumber === chapterNumber);
        if (index >= 0) {
          updated[index] = chapterPreview;
        } else {
          updated.push(chapterPreview);
        }
        return updated;
      });

      setSelectedChapter(chapterNumber);
    } catch (err) {
      console.error('Error loading chapter preview:', err);
      setError(`Failed to load chapter ${chapterNumber} preview. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !preview) {
    return (
      <div className="preview-panel">
        <h3>Content Preview</h3>
        <p>Loading preview...</p>
      </div>
    );
  }

  return (
    <div className="preview-panel" role="region" aria-labelledby="preview-panel-title">
      <h3 id="preview-panel-title">Content Preview</h3>

      {error && (
        <div className="error-message" role="alert" aria-live="polite">
          <p>Error: {error}</p>
          <button onClick={loadPreview} aria-label="Retry loading preview">Retry</button>
        </div>
      )}

      {preview && (
        <div className="preview-content">
          <div className="preview-header">
            <h4>Textbook: {preview.title}</h4>
            <p><strong>Status:</strong> {preview.status}</p>
            <p><strong>Chapters:</strong> {preview.totalChapters}</p>
            <p><strong>Audience:</strong> {preview.targetAudience}</p>
            <p><strong>Depth:</strong> {preview.contentDepth}</p>
          </div>

          <div className="preview-body">
            <h5>Preview Content:</h5>
            <div className="preview-text" aria-label={`Preview of textbook: ${preview.title}`}>
              {preview.preview}
              {!preview.fullContentAvailable && (
                <p className="preview-note" aria-label="Content availability note">
                  <em>Showing partial preview. Full content available after generation.</em>
                </p>
              )}
            </div>
          </div>

          {chapterPreviews.length > 0 && (
            <div className="chapter-previews" aria-labelledby="chapter-previews-title">
              <h5 id="chapter-previews-title">Chapter Previews:</h5>
              <div className="chapter-nav" role="tablist" aria-label="Chapter selection">
                {chapterPreviews.map((chapter) => (
                  <button
                    key={chapter.chapterNumber}
                    className={`chapter-nav-btn ${selectedChapter === chapter.chapterNumber ? 'active' : ''}`}
                    onClick={() => handleChapterSelect(chapter.chapterNumber)}
                    role="tab"
                    aria-selected={selectedChapter === chapter.chapterNumber}
                    aria-controls={`chapter-preview-${chapter.chapterNumber}`}
                    id={`chapter-tab-${chapter.chapterNumber}`}
                  >
                    Ch {chapter.chapterNumber}
                  </button>
                ))}
              </div>

              {selectedChapter !== null && (
                <div
                  className="selected-chapter-preview"
                  role="tabpanel"
                  id={`chapter-preview-${selectedChapter}`}
                  aria-labelledby={`chapter-tab-${selectedChapter}`}
                  aria-hidden={selectedChapter === null}
                >
                  <h6>Chapter {selectedChapter} Preview:</h6>
                  {chapterPreviews.find(c => c.chapterNumber === selectedChapter)?.preview || 'Loading...'}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {!preview && !loading && (
        <div className="no-preview" role="status" aria-label="No preview available">
          <p>No preview available. Generate a textbook to see content preview.</p>
        </div>
      )}
    </div>
  );
};

export default PreviewPanel;