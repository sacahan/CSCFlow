import React, { useEffect, useState } from 'react';
import { fetchWeatherData } from '../../services/weatherAPI';

interface WeatherPanelProps {
    locationName?: string;
    weather?: string;
    rainChance?: number;
}

export const WeatherPanel: React.FC<WeatherPanelProps> = ({ locationName: initialLocationName, weather: initialWeather, rainChance: initialRainChance }) => {
    const [locationName, setLocationName] = useState<string>(initialLocationName || '載入中');
    const [weather, setWeather] = useState<string>(initialWeather || '載入中');
    const [rainChance, setRainChance] = useState<number>(initialRainChance || 0);
    const [isLoading, setIsLoading] = useState<boolean>(!initialWeather || !initialRainChance);

    useEffect(() => {
        const loadWeatherData = async () => {
            try {
                setIsLoading(true);
                const data = await fetchWeatherData();
                setWeather(data.weather);
                setRainChance(data.rainChance);
            } catch (error) {
                console.error('Failed to load weather data:', error);
            } finally {
                setIsLoading(false);
            }
        };

        if (!initialWeather || !initialRainChance) {
            loadWeatherData();
        }
    }, [initialWeather, initialRainChance]);

    return (
        <div className="bg-gradient-to-r from-yellow-400 to-red-500 text-white p-4 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-2">
                <i className="fas fa-sun"></i> 天氣 ({locationName})
            </h2>
            {isLoading ? (
                <p className="text-center">載入中...</p>
            ) : (
                <p className="flex justify-between">
                    <span className="font-bold">{weather}</span>
                    <span>降雨機率: <span className="font-bold">{rainChance}%</span></span>
                </p>
            )}
        </div>
    );
};
