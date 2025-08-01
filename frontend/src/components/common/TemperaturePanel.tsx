import React from 'react';

interface TemperaturePanelProps {
  minTemperature: number;
  maxTemperature: number;
  unit?: 'C' | 'F';
}

export const TemperaturePanel: React.FC<TemperaturePanelProps> = ({
  minTemperature,
  maxTemperature,
  unit = 'C'
}) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">溫度範圍</h3>
      <div className="flex justify-between items-center">
        <div>
          <p className="text-sm text-gray-500">最低溫度</p>
          <p className="text-lg font-medium text-blue-600">
            {minTemperature}°{unit}
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">最高溫度</p>
          <p className="text-lg font-medium text-red-600">
            {maxTemperature}°{unit}
          </p>
        </div>
      </div>
    </div>
  );
};
