import React from 'react';

interface WeatherPanelProps {
  weather: string;
  rainChance: number;
}

export const WeatherPanel: React.FC<WeatherPanelProps> = ({ weather, rainChance }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">目前天氣</h3>
          <p className="text-gray-600">{weather}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">降雨機率</p>
          <p className="text-lg font-medium text-gray-800">{rainChance}%</p>
        </div>
      </div>
    </div>
  );
};
