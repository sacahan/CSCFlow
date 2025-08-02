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
  const [isLoading, setIsLoading] = useState<boolean>(
    !minTemperature || !maxTemperature,
  );

  useEffect(() => {
    console.log(
      `TemperaturePanel: Loaded temperatures - Min: ${minTemperature}°${unit}, Max: ${maxTemperature}°${unit}`,
    );
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
            {minTemperature}°{unit}
          </span>{" "}
          ~{" "}
          <span className="font-bold">
            {maxTemperature}°{unit}
          </span>
        </p>
      )}
    </div>
  );
};
