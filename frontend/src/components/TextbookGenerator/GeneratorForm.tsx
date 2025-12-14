import React, { useState } from 'react';
import { GenerationParams } from '../../types/textbook';

interface GeneratorFormProps {
  onSubmit: (params: GenerationParams) => void;
}

const GeneratorForm: React.FC<GeneratorFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<GenerationParams>({
    topic: '',
    targetAudience: 'undergraduate',
    numChapters: 5,
    contentDepth: 'medium',
    writingStyle: 'academic',
    sectionsPerChapter: 3,
    includeExamples: true,
    includeExercises: false,
    requiredSources: [],
    excludedTopics: [],
    customInstructions: ''
  });

  const [customSource, setCustomSource] = useState('');
  const [customExcludedTopic, setCustomExcludedTopic] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const val = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;

    setFormData(prev => ({
      ...prev,
      [name]: name === 'numChapters' || name === 'sectionsPerChapter' ? parseInt(value) : val
    }));
  };

  const handleAddSource = () => {
    if (customSource.trim() && !formData.requiredSources.includes(customSource.trim())) {
      setFormData(prev => ({
        ...prev,
        requiredSources: [...prev.requiredSources, customSource.trim()]
      }));
      setCustomSource('');
    }
  };

  const handleRemoveSource = (source: string) => {
    setFormData(prev => ({
      ...prev,
      requiredSources: prev.requiredSources.filter(s => s !== source)
    }));
  };

  const handleAddExcludedTopic = () => {
    if (customExcludedTopic.trim() && !formData.excludedTopics.includes(customExcludedTopic.trim())) {
      setFormData(prev => ({
        ...prev,
        excludedTopics: [...prev.excludedTopics, customExcludedTopic.trim()]
      }));
      setCustomExcludedTopic('');
    }
  };

  const handleRemoveExcludedTopic = (topic: string) => {
    setFormData(prev => ({
      ...prev,
      excludedTopics: prev.excludedTopics.filter(t => t !== topic)
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="generator-form" role="form" aria-label="Textbook Generation Form">
      <div className="form-group">
        <label htmlFor="topic">Topic:</label>
        <input
          type="text"
          id="topic"
          name="topic"
          value={formData.topic}
          onChange={handleChange}
          placeholder="Enter the main topic for your textbook"
          required
          aria-required="true"
          aria-describedby="topic-help"
        />
        <small id="topic-help" className="form-help">Enter the main subject for your textbook</small>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="targetAudience">Target Audience:</label>
          <select
            id="targetAudience"
            name="targetAudience"
            value={formData.targetAudience}
            onChange={handleChange}
            aria-describedby="targetAudience-help"
          >
            <option value="elementary">Elementary</option>
            <option value="middle_school">Middle School</option>
            <option value="high_school">High School</option>
            <option value="undergraduate">Undergraduate</option>
            <option value="graduate">Graduate</option>
            <option value="professional">Professional</option>
            <option value="general">General</option>
          </select>
          <small id="targetAudience-help" className="form-help">Select the intended audience level</small>
        </div>

        <div className="form-group">
          <label htmlFor="contentDepth">Content Depth:</label>
          <select
            id="contentDepth"
            name="contentDepth"
            value={formData.contentDepth}
            onChange={handleChange}
            aria-describedby="contentDepth-help"
          >
            <option value="shallow">Shallow</option>
            <option value="medium">Medium</option>
            <option value="deep">Deep</option>
          </select>
          <small id="contentDepth-help" className="form-help">Select the depth level of content</small>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="numChapters">Number of Chapters:</label>
          <input
            type="number"
            id="numChapters"
            name="numChapters"
            min="1"
            max="100"
            value={formData.numChapters}
            onChange={handleChange}
            aria-describedby="numChapters-help"
          />
          <small id="numChapters-help" className="form-help">Enter number of chapters (1-100)</small>
        </div>

        <div className="form-group">
          <label htmlFor="sectionsPerChapter">Sections per Chapter:</label>
          <input
            type="number"
            id="sectionsPerChapter"
            name="sectionsPerChapter"
            min="1"
            max="20"
            value={formData.sectionsPerChapter}
            onChange={handleChange}
            aria-describedby="sectionsPerChapter-help"
          />
          <small id="sectionsPerChapter-help" className="form-help">Enter number of sections per chapter (1-20)</small>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="writingStyle">Writing Style:</label>
          <select
            id="writingStyle"
            name="writingStyle"
            value={formData.writingStyle}
            onChange={handleChange}
            aria-describedby="writingStyle-help"
          >
            <option value="formal">Formal</option>
            <option value="conversational">Conversational</option>
            <option value="technical">Technical</option>
            <option value="academic">Academic</option>
            <option value="casual">Casual</option>
          </select>
          <small id="writingStyle-help" className="form-help">Select the writing style preference</small>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="includeExamples">
          <input
            type="checkbox"
            id="includeExamples"
            name="includeExamples"
            checked={formData.includeExamples}
            onChange={handleChange}
          />
          Include Examples
        </label>
      </div>

      <div className="form-group">
        <label htmlFor="includeExercises">
          <input
            type="checkbox"
            id="includeExercises"
            name="includeExercises"
            checked={formData.includeExercises}
            onChange={handleChange}
          />
          Include Exercises
        </label>
      </div>

      <div className="form-group">
        <label htmlFor="addSource">Required Sources:</label>
        <div className="input-with-button">
          <input
            type="text"
            id="addSource"
            value={customSource}
            onChange={(e) => setCustomSource(e.target.value)}
            placeholder="Add a source (e.g., Wikipedia, arXiv)"
            aria-describedby="addSource-help"
          />
          <button
            type="button"
            onClick={handleAddSource}
            aria-label="Add source"
          >
            Add
          </button>
        </div>
        <small id="addSource-help" className="form-help">Add sources to reference in content generation</small>
        <div className="tags-container" aria-label="List of required sources">
          {formData.requiredSources.map((source, index) => (
            <span key={index} className="tag" aria-label={`Source: ${source}`}>
              {source}
              <button
                type="button"
                onClick={() => handleRemoveSource(source)}
                aria-label={`Remove source: ${source}`}
                className="remove-tag-btn"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="addExcludedTopic">Excluded Topics:</label>
        <div className="input-with-button">
          <input
            type="text"
            id="addExcludedTopic"
            value={customExcludedTopic}
            onChange={(e) => setCustomExcludedTopic(e.target.value)}
            placeholder="Add a topic to exclude"
            aria-describedby="addExcludedTopic-help"
          />
          <button
            type="button"
            onClick={handleAddExcludedTopic}
            aria-label="Add excluded topic"
          >
            Add
          </button>
        </div>
        <small id="addExcludedTopic-help" className="form-help">Add topics to avoid in content generation</small>
        <div className="tags-container" aria-label="List of excluded topics">
          {formData.excludedTopics.map((topic, index) => (
            <span key={index} className="tag" aria-label={`Excluded topic: ${topic}`}>
              {topic}
              <button
                type="button"
                onClick={() => handleRemoveExcludedTopic(topic)}
                aria-label={`Remove excluded topic: ${topic}`}
                className="remove-tag-btn"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="customInstructions">Custom Instructions:</label>
        <textarea
          id="customInstructions"
          name="customInstructions"
          value={formData.customInstructions}
          onChange={handleChange}
          placeholder="Any special instructions for the textbook generation..."
          rows={3}
          aria-describedby="customInstructions-help"
        />
        <small id="customInstructions-help" className="form-help">Add any special requirements for content generation</small>
      </div>

      <button
        type="submit"
        className="generate-button"
        aria-label="Generate textbook with current parameters"
      >
        Generate Textbook
      </button>
    </form>
  );
};

export default GeneratorForm;