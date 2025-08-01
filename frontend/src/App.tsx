import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { Gauge } from './components/charts/Gauge';
import { TrendChart } from './components/charts/TrendChart';
import { WeatherPanel } from './components/common/WeatherPanel';
import { TemperaturePanel } from './components/common/TemperaturePanel';
import { ComfortPanel } from './components/common/ComfortPanel';
import { fetchWeatherData } from './services/weatherAPI';

// 模擬數據
const mockCenters = [
  { id: '1', name: '台北市立大安運動中心' },
  { id: '2', name: '台北市立信義運動中心' },
  { id: '3', name: '台北市立中山運動中心' },
  { id: '4', name: '台北市立南港運動中心' },
];

export const App: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [selectedCenter, setSelectedCenter] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  const [weatherData, setWeatherData] = useState<any>(null);

  // 模擬數據
  const mockData = {
    gym: { value: 45, maxCapacity: 80 },
    pool: { value: 30, maxCapacity: 300 },
    trend: Array.from({ length: 24 }, (_, i) => ({
      time: `${i}:00`,
      gym: Math.floor(Math.random() * 80),
      pool: Math.floor(Math.random() * 300)
    }))
  };

  useEffect(() => {
    const loadWeatherData = async () => {
      const data = await fetchWeatherData();
      setWeatherData(data);
    };
    loadWeatherData();
  }, []);

  return (
    <div className="flex bg-gray-100 min-h-screen">
      <Sidebar
        centers={mockCenters}
        onSelectCenter={(centerId) => setSelectedCenter(centerId)}
      />

      <div className={`flex-1 ${isSidebarOpen ? 'ml-64' : ''} transition-margin duration-300`}>
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
                  locationName={weatherData?.locationName}
                  weather={weatherData?.weather}
                  rainChance={weatherData?.rainChance}
                />
                <TemperaturePanel
                  minTemperature={weatherData?.minTemperature}
                  maxTemperature={weatherData?.maxTemperature}
                />
                <ComfortPanel
                  comfortLevel={weatherData?.comfortLevel}
                />
              </div>
            </div>

            {/* 累積人數趨勢圖 */}
            <TrendChart
              data={mockData.trend}
              timeRange={timeRange}
            />
          </main>
        </div>
      </div>
    </div>
  );
};
