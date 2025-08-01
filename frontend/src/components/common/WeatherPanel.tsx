import React from 'react';

interface WeatherPanelProps {
  weather: string;
  rainChance: number;
}

export const WeatherPanel: React.FC<WeatherPanelProps> = ({ weather, rainChance }) => {
  return (
    <div className="bg-gradient-to-r from-yellow-400 to-red-500 text-white p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-2">
        <i className="fas fa-sun"></i> 天氣
      </h2>
      <p className="flex justify-between">
        <span className="font-bold">{weather}</span>
        <span>降雨機率: <span className="font-bold">{rainChance}%</span></span>
      </p>
    </div>
  );
};
