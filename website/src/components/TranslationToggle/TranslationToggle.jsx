import React, { useState, useEffect } from 'react';
import styles from './TranslationToggle.module.css';

const TranslationToggle = () => {
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [isExpanded, setIsExpanded] = useState(false);
  // Note: We're not using useColorMode here to avoid context issues during SSR
  // The CSS will handle light/dark mode automatically

  // Language options
  const languages = [
    { code: 'en', name: 'English', nativeName: 'English' },
    { code: 'ur', name: 'Urdu', nativeName: 'اردو' },
    { code: 'es', name: 'Spanish', nativeName: 'Español' },
    { code: 'fr', name: 'French', nativeName: 'Français' },
    { code: 'de', name: 'German', nativeName: 'Deutsch' },
  ];

  // Function to simulate translation (in a real implementation, this would call the backend)
  const handleLanguageChange = (languageCode) => {
    setSelectedLanguage(languageCode);
    setIsExpanded(false);

    // In a real implementation, this would trigger content translation
    // For now, we'll just log the change
    console.log(`Language changed to: ${languageCode}`);

    // Update UI to reflect language change
    document.documentElement.lang = languageCode;
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isExpanded && !event.target.closest(`.${styles.translationToggle}`)) {
        setIsExpanded(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isExpanded]);

  const currentLanguage = languages.find(lang => lang.code === selectedLanguage);

  return (
    <div className={styles.translationToggle}>
      <button
        className={`${styles.toggleButton} ${isExpanded ? styles.expanded : ''}`}
        onClick={() => setIsExpanded(!isExpanded)}
        aria-haspopup="true"
        aria-expanded={isExpanded}
        title={`Switch language (currently ${currentLanguage?.name})`}
      >
        <span className={styles.languageCode}>{selectedLanguage.toUpperCase()}</span>
        <span className={styles.arrow}>{isExpanded ? '▲' : '▼'}</span>
      </button>

      {isExpanded && (
        <div className={styles.dropdown}>
          <div className={styles.dropdownHeader}>
            <span>Select Language</span>
          </div>
          <ul className={styles.languageList}>
            {languages.map((language) => (
              <li key={language.code}>
                <button
                  className={`${styles.languageOption} ${
                    selectedLanguage === language.code ? styles.active : ''
                  }`}
                  onClick={() => handleLanguageChange(language.code)}
                  aria-current={selectedLanguage === language.code ? 'true' : 'false'}
                >
                  <span className={styles.languageName}>
                    {language.nativeName}
                    {language.code !== language.nativeName && (
                      <span className={styles.languageEnglishName}>
                        {' '}({language.name})
                      </span>
                    )}
                  </span>
                  {selectedLanguage === language.code && (
                    <span className={styles.checkmark}>✓</span>
                  )}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default TranslationToggle;