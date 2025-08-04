import React, { useState, useEffect } from "react";
import { Sidebar } from "./components/layout/Sidebar";
import { Header } from "./components/layout/Header";
import { Gauge } from "./components/charts/Gauge";
import { TrendChart } from "./components/charts/TrendChart";
import { WeatherPanel } from "./components/common/WeatherPanel";
import { TemperaturePanel } from "./components/common/TemperaturePanel";
import { ComfortPanel } from "./components/common/ComfortPanel";
import { fetchWeatherData } from "./services/weatherAPI";
import { authService } from "./services/authAPI";
import { getLocationFromZipCode } from "./utils/zipCodeMapping";

interface Center {
  zipCode: string;
  name: string;
  address: string;
  websiteUrl: string;
}

export const App: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [selectedCenter, setSelectedCenter] = useState<Center | null>(null);
  const [isAuthLoading, setIsAuthLoading] = useState(true);
  const [weatherData, setWeatherData] = useState<any>(null);

  // 確保在應用程式啟動時已經驗證
  useEffect(() => {
    const initAuth = async () => {
      try {
        await authService.ensureAuthenticated();
      } catch (error) {
        console.error("Authentication failed:", error);
      } finally {
        setIsAuthLoading(false);
      }
    };

    initAuth();
  }, []);

  // Fetch weather data when selected center changes
  useEffect(() => {
    const loadWeatherData = async () => {
      if (!selectedCenter) {
        setWeatherData(null);
        return;
      }

      try {
        const locationName = getLocationFromZipCode(selectedCenter.zipCode);
        console.log(
          `Fetching weather data for ${locationName} (zip: ${selectedCenter.zipCode})`,
        );
        const data = await fetchWeatherData(locationName);
        setWeatherData(data);
      } catch (error) {
        console.error("Error loading weather data:", error);
        setWeatherData(null);
      }
    };

    loadWeatherData();
  }, [selectedCenter]);

  return (
    <div className="flex bg-gray-100 min-h-screen">
      <Sidebar
        isAuthLoading={isAuthLoading}
        onSelectCenter={(center) => setSelectedCenter(center)}
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
      />

      <div className="flex-1 sm:ml-64 transition-margin duration-300">
        <div className="p-4">
          <Header
            selectedCenter={selectedCenter}
            onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
          />

          <main>
            {selectedCenter ? (
              <>
                <div className="flex flex-col lg:flex-row gap-4 mb-4">
                  {/* 左側游泳池和健身房區域 */}
                  <div className="lg:w-2/3 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Gauge
                      title="健身房"
                      type="gym"
                      icon="fa-dumbbell"
                      zipCode={selectedCenter.zipCode}
                    />
                    <Gauge
                      title="游泳池"
                      type="pool"
                      icon="fa-swimmer"
                      zipCode={selectedCenter.zipCode}
                    />
                  </div>

                  {/* 右側天氣資訊區域 */}
                  <div className="lg:w-1/3 space-y-4">
                    <WeatherPanel
                      location={selectedCenter.name}
                      weather={weatherData?.weather}
                      rainChance={weatherData?.rainChance}
                    />
                    <TemperaturePanel
                      minTemperature={weatherData?.minTemperature}
                      maxTemperature={weatherData?.maxTemperature}
                    />
                    <ComfortPanel comfortLevel={weatherData?.comfortLevel} />
                  </div>
                </div>

                {/* 累積人數趨勢圖 */}
                <TrendChart zipCode={selectedCenter.zipCode} />
              </>
            ) : (
              <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
                <p className="text-gray-500 text-xl">
                  請從側邊欄選擇一個運動中心
                </p>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};
