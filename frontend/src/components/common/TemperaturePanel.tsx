import React, { useEffect, useState } from 'react';
import { fetchWeatherData } from '../../services/weatherAPI';

interface TemperaturePanelProps {
  minTemperature?: number;
  maxTemperature?: number;
  unit?: 'C' | 'F';
}

export const TemperaturePanel: React.FC<TemperaturePanelProps> = ({
  minTemperature: initialMinTemp,
  maxTemperature: initialMaxTemp,
  unit = 'C'
}) => {
  const [minTemperature, setMinTemperature] = useState<number>(initialMinTemp || 0);
  const [maxTemperature, setMaxTemperature] = useState<number>(initialMaxTemp || 0);
  const [isLoading, setIsLoading] = useState<boolean>(!initialMinTemp || !initialMaxTemp);

  useEffect(() => {
    const loadTemperatureData = async () => {
      try {
        setIsLoading(true);
        const data = await fetchWeatherData();
        setMinTemperature(data.minTemperature);
        setMaxTemperature(data.maxTemperature);
      } catch (error) {
        console.error('Failed to load temperature data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (!initialMinTemp || !initialMaxTemp) {
      loadTemperatureData();
    }
  }, [initialMinTemp, initialMaxTemp]);

  return (
    <div className="bg-gradient-to-r from-red-400 to-pink-500 text-white p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-2">
        <i className="fas fa-thermometer-half"></i> 溫度
      </h2>
      {isLoading ? (
        <p className="text-center">載入中...</p>
      ) : (
        <p>
          <span className="font-bold">{minTemperature}°{unit}</span>
          {' '} ~ {' '}
          <span className="font-bold">{maxTemperature}°{unit}</span>
        </p>
      )}
    </div>
  );
};
