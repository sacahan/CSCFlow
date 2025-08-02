import React, { useEffect, useState } from "react";
import { fetchWeatherData } from "../../services/weatherAPI";

interface TemperaturePanelProps {
  minTemperature?: number;
  maxTemperature?: number;
  unit?: "C" | "F";
}

export const TemperaturePanel: React.FC<TemperaturePanelProps> = ({
  minTemperature,
  maxTemperature,
  unit = "C",
}) => {
  const [minTempValue, setMinTempValue] = useState<number>(0);
  const [maxTempValue, setMaxTempValue] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(
    !minTemperature || !maxTemperature,
  );

  useEffect(() => {
    console.log(
      `TemperaturePanel: Loaded temperatures - Min: ${minTemperature}°${unit}, Max: ${maxTemperature}°${unit}`,
    );
    setMinTempValue(minTemperature);
    setMaxTempValue(maxTemperature);
    setIsLoading(!minTemperature || !maxTemperature);
  }, [minTemperature, maxTemperature]);

  return (
    <div className="bg-gradient-to-r from-red-400 to-pink-500 text-white p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-2">
        <i className="fas fa-thermometer-half"></i> 溫度
      </h2>
      {isLoading ? (
        <p className="text-left">查詢中央氣象台資訊...</p>
      ) : (
        <p>
          <span className="font-bold">
            {minTempValue}°{unit}
          </span>{" "}
          ~{" "}
          <span className="font-bold">
            {maxTempValue}°{unit}
          </span>
        </p>
      )}
    </div>
  );
};
