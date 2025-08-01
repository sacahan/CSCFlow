import React, { useState, useEffect } from 'react';

interface ComfortPanelProps {
  initialComfortLevel?: string;
}

export const ComfortPanel: React.FC<ComfortPanelProps> = ({ comfortLevel }) => {
  const [comfortLevelValue, setCurrentComfortLevel] = useState(comfortLevel || '');
  const [isLoading, setIsLoading] = useState<boolean>(!comfortLevel);

  useEffect(() => {
    console.log(`ComfortPanel: Loaded comfort level - ${comfortLevel}`);
    setCurrentComfortLevel(comfortLevel);
    setIsLoading(!comfortLevel);
  }, [comfortLevel]);

  return (
    <div className="bg-gradient-to-r from-indigo-400 to-indigo-500 text-white p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-2">
        <i className="fas fa-tint"></i> 體感
      </h2>
      {isLoading ? (
        <p className="text-left">查詢中央氣象台資訊...</p>
      ) : (
        <p>
          <span className="font-bold">{comfortLevelValue}</span>
        </p>
      )}
    </div>
  );
};
