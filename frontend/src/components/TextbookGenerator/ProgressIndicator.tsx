import React, { useState, useEffect } from 'react';

interface ProgressIndicatorProps {
  progress: number; // 0 to 1
  status: string;
  textbookId?: string;
}

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ progress, status, textbookId }) => {
  const [isVisible, setIsVisible] = useState(progress > 0);

  useEffect(() => {
    // Show the progress indicator when progress > 0
    setIsVisible(progress > 0);
  }, [progress]);

  if (!isVisible) {
    return null;
  }

  const progressPercentage = Math.round(progress * 100);

  return (
    <div
      className="progress-container"
      role="progressbar"
      aria-valuenow={progressPercentage}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={`Textbook generation progress: ${progressPercentage}% - ${status}`}
    >
      <div className="progress-header">
        <h3>Textbook Generation Progress</h3>
        {textbookId && <p>Textbook ID: {textbookId}</p>}
      </div>

      <div className="progress-bar-container" aria-hidden="true">
        <div
          className="progress-bar"
          style={{ width: `${progressPercentage}%` }}
        >
          {progressPercentage}%
        </div>
      </div>

      <div className="progress-status">
        <p>Status: {status}</p>
        <p>Progress: {progressPercentage}%</p>
      </div>
    </div>
  );
};

export default ProgressIndicator;