import React, { useState, useEffect } from "react";

interface WeatherPanelProps {
  location: string;
  weather?: string;
  rainChance?: number;
}

export const WeatherPanel: React.FC<WeatherPanelProps> = ({
  location,
  weather,
  rainChance,
}) => {
  const [isLoading, setIsLoading] = useState<boolean>(
    !weather || rainChance === undefined,
  );
  const [locationValue, setLocationValue] = useState<string>(location || "");
  const [weatherValue, setWeatherValue] = useState<string>(weather || "");
  const [rainChanceValue, setRainChanceValue] = useState<number | undefined>(
    rainChance,
  );

  useEffect(() => {
    console.log(
      `WeatherPanel: Loaded weather for ${location} - Weather: ${weather}, Rain Chance: ${rainChance}%`,
    );
    setLocationValue(location);
    setWeatherValue(weather);
    setRainChanceValue(rainChance);
    setIsLoading(
      location === "" || weather === undefined || rainChance === undefined,
    );
  }, [location, weather, rainChance]);

  return (
    <div className="bg-gradient-to-r from-yellow-400 to-red-500 text-white p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-2">
        <i className="fas fa-sun"></i> 天氣 ({locationValue})
      </h2>
      {isLoading ? (
        <p className="text-left">查詢中央氣象台資訊...</p>
      ) : (
        <p className="flex justify-between">
          <span className="font-bold">{weatherValue}</span>
          <span>
            降雨機率: <span className="font-bold">{rainChance}%</span>
          </span>
        </p>
      )}
    </div>
  );
};
