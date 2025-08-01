import React, { useEffect, useState } from 'react';
import { fetchWeatherData } from '../../services/weatherAPI';

interface ComfortPanelProps {
  comfortLevel?: string;
}

export const ComfortPanel: React.FC<ComfortPanelProps> = ({ comfortLevel: initialComfortLevel }) => {
  const [comfortLevel, setComfortLevel] = useState<string>(initialComfortLevel || '載入中');
  const [isLoading, setIsLoading] = useState<boolean>(!initialComfortLevel);

  useEffect(() => {
    const loadComfortData = async () => {
      try {
        setIsLoading(true);
        const data = await fetchWeatherData();
        setComfortLevel(data.comfortLevel);
      } catch (error) {
        console.error('Failed to load comfort level data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (!initialComfortLevel) {
      loadComfortData();
    }
  }, [initialComfortLevel]);

  return (
    <div className="bg-gradient-to-r from-indigo-400 to-indigo-500 text-white p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-2">
        <i className="fas fa-tint"></i> 體感
      </h2>
      {isLoading ? (
        <p className="text-center">載入中...</p>
      ) : (
        <p>
          <span className="font-bold">{comfortLevel}</span>
        </p>
      )}
    </div>
  );
};
