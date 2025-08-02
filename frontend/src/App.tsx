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

export const App: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [selectedCenter, setSelectedCenter] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<"daily" | "weekly" | "monthly">(
    "daily",
  );
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

  // 使用 useEffect 來載入天氣數據，確保在組件渲染後執行
  useEffect(() => {
    const loadWeatherData = async () => {
      try {
        const data = await fetchWeatherData(); // 從 API 獲取天氣數據
        setWeatherData(data); // 將獲取的天氣數據存入狀態
      } catch (error) {
        console.error("Error loading weather data:", error);
      }
    };

    loadWeatherData(); // 確保執行數據載入函數
  }, []);

  // 模擬數據：定義健身房和游泳池的使用情況，以及一天內的累積人數趨勢
  const mockData = {
    gym: { value: 45, maxCapacity: 80 }, // 健身房目前使用人數及最大容量
    pool: { value: 30, maxCapacity: 300 }, // 游泳池目前使用人數及最大容量
    trend: Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`, // 時間點，格式為小時:分鐘
      gym: Math.floor(Math.random() * 80), // 隨機生成健身房使用人數
      pool: Math.floor(Math.random() * 300), // 隨機生成游泳池使用人數
    })),
  };

  return (
    <div className="flex bg-gray-100 min-h-screen">
      <Sidebar
        isAuthLoading={isAuthLoading}
        onSelectCenter={(centerId) => setSelectedCenter(centerId)}
      />

      <div
        className={`flex-1 ${
          isSidebarOpen ? "ml-64" : ""
        } transition-margin duration-300`}
      >
        <div className="p-4">
          <Header onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

          <main>
            <div className="flex flex-col lg:flex-row gap-4 mb-4">
              {/* 左側游泳池和健身房區域 */}
              <div className="lg:w-2/3 grid grid-cols-1 md:grid-cols-2 gap-4">
                <Gauge
                  title="健身房"
                  value={mockData.gym.value}
                  maxCapacity={mockData.gym.maxCapacity}
                  type="gym"
                  icon="fa-dumbbell"
                />
                <Gauge
                  title="游泳池"
                  value={mockData.pool.value}
                  maxCapacity={mockData.pool.maxCapacity}
                  type="pool"
                  icon="fa-swimmer"
                />
              </div>

              {/* 右側天氣資訊區域 */}
              <div className="lg:w-1/3 space-y-4">
                <WeatherPanel
                  location={weatherData?.locationName}
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
            <TrendChart data={mockData.trend} timeRange={timeRange} />
          </main>
        </div>
      </div>
    </div>
  );
};
