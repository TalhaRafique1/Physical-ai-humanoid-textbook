import React, { useState } from 'react';
import { Textbook } from '../../types/textbook';
import { translationApi } from '../../services/api/translationApi';

interface TranslationToggleProps {
  textbook: Textbook;
  onTranslate: (translatedTextbook: Textbook) => void;
}

const TranslationToggle: React.FC<TranslationToggleProps> = ({ textbook, onTranslate }) => {
  const [isTranslating, setIsTranslating] = useState<boolean>(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('ur');
  const [error, setError] = useState<string | null>(null);
  const [languages, setLanguages] = useState<Array<{code: string, name: string, native_name: string}>>([
    { code: 'ur', name: 'Urdu', native_name: 'اردو' },
    { code: 'en', name: 'English', native_name: 'English' }
  ]);

  const handleTranslate = async () => {
    if (!textbook.id) {
      setError('Textbook ID is required for translation');
      return;
    }

    try {
      setIsTranslating(true);
      setError(null);

      const result = await translationApi.translateTextbook(textbook.id, selectedLanguage);

      // For now, we'll just pass the original textbook with a note
      // In a real implementation, this would be the translated textbook
      const translatedTextbook = {
        ...textbook,
        title: `${textbook.title} (${selectedLanguage.toUpperCase()})`,
        description: `Translated version of "${textbook.title}" in ${selectedLanguage.toUpperCase()}`
      };

      onTranslate(translatedTextbook);
    } catch (err) {
      console.error('Translation error:', err);
      setError('Translation failed. Please try again.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className="translation-toggle">
      <h4>Translate Textbook</h4>

      <div className="translation-controls">
        <label htmlFor="language-select">Select Language:</label>
        <select
          id="language-select"
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
        >
          {languages.map(lang => (
            <option key={lang.code} value={lang.code}>
              {lang.name} ({lang.native_name})
            </option>
          ))}
        </select>

        <button
          onClick={handleTranslate}
          disabled={isTranslating}
          className="translate-btn"
        >
          {isTranslating ? 'Translating...' : `Translate to ${selectedLanguage.toUpperCase()}`}
        </button>
      </div>

      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
        </div>
      )}

      <div className="translation-info">
        <p>One-click translation to Urdu and other languages.</p>
        <p>Current support: Urdu (اردو)</p>
      </div>
    </div>
  );
};

export default TranslationToggle;