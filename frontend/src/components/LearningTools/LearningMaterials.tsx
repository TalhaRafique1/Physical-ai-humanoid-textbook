import React, { useState, useEffect } from 'react';
import { Textbook } from '../../types/textbook';
import { learningToolsApi } from '../../services/api/learningToolsApi';

interface LearningMaterialsProps {
  textbook: Textbook;
}

interface QuizQuestion {
  id: string;
  question: string;
  type: string;
  options: string[];
  correct_answer: string;
  difficulty: string;
}

interface LearningBooster {
  id: string;
  type: string;
  title: string;
  content: string;
  tip: string;
  generated_at: string;
}

interface LearningMaterials {
  summary: any;
  quiz: {
    questions: QuizQuestion[];
    total_questions: number;
    recommended_time: number;
  };
  boosters: LearningBooster[];
}

const LearningMaterials: React.FC<LearningMaterialsProps> = ({ textbook }) => {
  const [materials, setMaterials] = useState<LearningMaterials | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'summary' | 'quiz' | 'boosters'>('summary');

  useEffect(() => {
    loadLearningMaterials();
  }, [textbook.id]);

  const loadLearningMaterials = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await learningToolsApi.generateLearningMaterials(textbook.id);
      setMaterials(response.materials);
    } catch (err) {
      console.error('Error loading learning materials:', err);
      setError('Failed to load learning materials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleStartQuiz = () => {
    setActiveTab('quiz');
  };

  if (loading) {
    return (
      <div className="learning-materials">
        <h3>Learning Materials</h3>
        <p>Loading learning materials...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="learning-materials">
        <h3>Learning Materials</h3>
        <div className="error-message">
          <p>Error: {error}</p>
          <button onClick={loadLearningMaterials}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="learning-materials">
      <h3>Learning Materials for {textbook.title}</h3>

      <div className="learning-tabs">
        <button
          className={`tab-button ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          Summary
        </button>
        <button
          className={`tab-button ${activeTab === 'quiz' ? 'active' : ''}`}
          onClick={() => setActiveTab('quiz')}
        >
          Quiz ({materials?.quiz.questions.length || 0})
        </button>
        <button
          className={`tab-button ${activeTab === 'boosters' ? 'active' : ''}`}
          onClick={() => setActiveTab('boosters')}
        >
          Boosters ({materials?.boosters.length || 0})
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'summary' && materials && (
          <div className="summary-content">
            <h4>Chapter Summary</h4>
            <div className="summary-text">
              {materials.summary.summary || 'No summary available.'}
            </div>
          </div>
        )}

        {activeTab === 'quiz' && materials && (
          <div className="quiz-content">
            <h4>Knowledge Check</h4>
            <p>Test your understanding with this {materials.quiz.total_questions}-question quiz.</p>
            <p>Estimated time: {materials.quiz.recommended_time} minutes</p>

            <div className="quiz-questions">
              {materials.quiz.questions.map((question, index) => (
                <div key={question.id} className="quiz-question">
                  <h5>Question {index + 1}</h5>
                  <p>{question.question}</p>

                  {question.type === 'multiple_choice' && question.options.length > 0 && (
                    <div className="mcq-options">
                      {question.options.map((option, optIndex) => (
                        <div key={optIndex} className="option">
                          <label>
                            <input type="radio" name={`q-${question.id}`} /> {option}
                          </label>
                        </div>
                      ))}
                    </div>
                  )}

                  {question.type === 'short_answer' && (
                    <textarea
                      placeholder="Type your answer here..."
                      rows={3}
                    ></textarea>
                  )}

                  <div className="question-meta">
                    Difficulty: <span className={`difficulty-${question.difficulty}`}>{question.difficulty}</span>
                  </div>
                </div>
              ))}
            </div>

            <button className="submit-quiz-btn">Submit Quiz</button>
          </div>
        )}

        {activeTab === 'boosters' && materials && (
          <div className="boosters-content">
            <h4>Learning Boosters</h4>
            <p>Enhance your learning with these tips and insights.</p>

            <div className="boosters-list">
              {materials.boosters.map((booster) => (
                <div key={booster.id} className="booster-card">
                  <h5>{booster.title}</h5>
                  <p>{booster.content}</p>
                  <div className="booster-tip">
                    <strong>Tip:</strong> {booster.tip}
                  </div>
                  <div className="booster-type">
                    Type: {booster.type.replace('_', ' ').toUpperCase()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LearningMaterials;