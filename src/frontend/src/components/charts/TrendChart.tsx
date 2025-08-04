// 引入必要的 React 和 echarts 庫
import React, { useEffect, useRef, useState } from "react";
import * as echarts from "echarts";
import { authAxios } from "../../services/authAPI"; // 調整這個路徑以符合你的專案結構

// 定義組件屬性的介面，包含數據陣列和時間範圍選項
interface TrendChartProps {
  zipCode: string; // Ensure center is passed
}

// 修正 TrendStats 的定義
interface TrendStats {
  date_time: string;
  avg_count: number;
  max_count: number;
  min_count: number;
}

export const TrendChart: React.FC<TrendChartProps> = ({ zipCode }) => {
  const [timeRange, setTimeRange] = useState<"daily" | "weekly" | "monthly">(
    "daily",
  );
  // 建立圖表容器和實例的參考
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);
  const [xAxisSeries, setXAxisSeries] = useState<string[]>([]);
  const [gymData, setGymData] = useState<TrendStats[]>([]);
  const [poolData, setPoolData] = useState<TrendStats[]>([]);

  // 初始化圖表實例
  useEffect(() => {
    if (chartRef.current) {
      chartInstance.current = echarts.init(chartRef.current);
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.dispose();
      }
    };
  }, []);

  // 設定圖表配置並更新數據
  useEffect(() => {
    if (!chartInstance.current) return;

    const option = {
      // 配置提示框
      tooltip: {
        trigger: "axis",
        formatter: function (params: any) {
          return params
            .map((param: any) => `${param.seriesName}: ${param.value}人`)
            .join("<br/>");
        },
      },
      // 配置圖例，設定顏色樣式
      legend: {
        data: poolData.length > 0 ? ["健身房", "游泳池"] : ["健身房"],
        textStyle: {
          color: "#ffffff",
        },
        top: 0, // 將圖例放置在頂部
        left: "center", // 水平置中
      },
      // 配置網格佈局
      grid: {
        left: "2%",
        right: "3%",
        bottom: "5%",
        top: "15%", // 為上方圖例留出空間
        containLabel: true,
      },
      // 配置 X 軸，設定為時間類別
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: xAxisSeries,
        axisLabel: {
          color: "#ffffff",
          fontSize: 12,
        },
        axisLine: {
          lineStyle: {
            color: "rgba(255, 255, 255, 0.5)",
          },
        },
      },
      // 配置 Y 軸，設定為數值類型
      yAxis: {
        type: "value",
        axisLabel: {
          formatter: "{value}人",
          color: "#ffffff",
        },
        axisLine: {
          lineStyle: {
            color: "rgba(255, 255, 255, 0.5)",
          },
        },
        splitLine: {
          lineStyle: {
            color: "rgba(255, 255, 255, 0.2)",
          },
        },
      },
      // 配置數據系列
      series: [
        {
          name: "健身房",
          type: "line",
          data: gymData.map((stat) => stat.avg_count),
          smooth: true,
          areaStyle: {
            opacity: 0.3,
          },
          emphasis: {
            focus: "series",
          },
          lineStyle: {
            width: 3,
          },
          itemStyle: {
            borderWidth: 2,
          },
        },
        {
          name: "游泳池",
          type: "line",
          data: poolData.map((stat) => stat.avg_count),
          smooth: true,
          areaStyle: {
            opacity: 0.3,
          },
          emphasis: {
            focus: "series",
          },
          lineStyle: {
            width: 3,
          },
          itemStyle: {
            borderWidth: 2,
          },
        },
      ],
    };

    chartInstance.current.setOption(option);
  }, [zipCode, xAxisSeries, gymData, poolData]);

  // 監聽視窗大小變化，適配圖表尺寸
  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // 根據選擇的場館和時間範圍獲取並更新趨勢圖表數據
  useEffect(() => {
    if (zipCode) {
      const fetchData = async () => {
        try {
          const response = await authAxios.get(`/api/v1/trend_stats`, {
            params: {
              zip_code: zipCode,
              // area_type: "gym",
              time_range: timeRange,
            },
          });
          const gymStats = response.data.gym;
          const poolStats = response.data.pool;

          // 更新 X 軸數據
          setXAxisSeries(
            gymStats.length > 0
              ? gymStats.map(
                  (stat: TrendStats) =>
                    timeRange === "daily"
                      ? stat.date_time.slice(11, 16) // 取 HH:mm 格式化顯示
                      : stat.date_time.slice(5, 10), // 取 MM-DD 格式化顯示
                )
              : poolStats.map(
                  (stat: TrendStats) =>
                    timeRange === "daily"
                      ? stat.date_time.slice(11, 16) // 取 HH:mm 格式化顯示
                      : stat.date_time.slice(5, 10), // 取 MM-DD 格式化顯示
                ),
          );
          // 更新健身房和游泳池的數據
          setGymData(gymStats);
          setPoolData(poolStats);
        } catch (error) {
          console.error("Error updating trend chart data:", error);
        }
      };

      fetchData();
    }
  }, [zipCode, timeRange]);

  // 渲染圖表容器和控制按鈕
  return (
    <div className="bg-gradient-to-r from-teal-500 to-teal-700 p-4 rounded-lg shadow-lg">
      <div className="flex items-center justify-between">
        <h3 className="text-white text-lg font-semibold">人數趨勢統計</h3>
        <div className="flex gap-2">
          <button
            onClick={() => setTimeRange("daily")}
            className={`px-3 py-1 rounded ${
              timeRange === "daily"
                ? "bg-white text-teal-700"
                : "bg-teal-600 text-white"
            }`}
          >
            每日
          </button>
          <button
            onClick={() => setTimeRange("weekly")}
            className={`px-3 py-1 rounded ${
              timeRange === "weekly"
                ? "bg-white text-teal-700"
                : "bg-teal-600 text-white"
            }`}
          >
            每週
          </button>
          <button
            onClick={() => setTimeRange("monthly")}
            className={`px-3 py-1 rounded ${
              timeRange === "monthly"
                ? "bg-white text-teal-700"
                : "bg-teal-600 text-white"
            }`}
          >
            每月
          </button>
        </div>
      </div>
      <div ref={chartRef} className="w-full h-[300px]" />
    </div>
  );
};
