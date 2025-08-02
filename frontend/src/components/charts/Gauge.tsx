import React, { useEffect, useRef } from "react";
import * as echarts from "echarts";
import { authAxios } from "../../services/authAPI"; // 確保引入 authAxios 來獲取數據

// 定義 GaugeProps 介面，包含三個屬性：title（標題）、maxCapacity（最大容量）和 value（當前值）。
interface GaugeProps {
  title: string;
  type: "gym" | "pool"; // 新增 type 屬性來區分不同類型
  icon: string; // 新增 icon 屬性來設置 Font Awesome 圖示
  zipCode: string; // 新增 center 屬性
}

//定義currentFlow，基於{
interface CurrentFlow {
  available: boolean; // 是否可用
  currentCount: number; // 當前流量數據
  maxCapacity: number; // 最大容量
  lastUpdated: string; // 最後更新時間
}

// 定義 Gauge 元件，使用 React.FC 並接收 GaugeProps 作為屬性。
export const Gauge: React.FC<GaugeProps> = ({ title, type, icon, zipCode }) => {
  // 使用 useRef 建立 chartRef 來存放圖表的 DOM 節點。
  const chartRef = useRef<HTMLDivElement>(null);
  // 使用 useRef 建立 chartInstance 來存放 ECharts 實例。
  const chartInstance = useRef<echarts.ECharts | null>(null);
  const [currentFlow, setCurrentFlow] = React.useState<CurrentFlow | null>(
    null,
  );

  // 初始化 ECharts 實例，並在元件卸載時釋放資源。
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

  // 根據屬性更新圖表的配置。
  useEffect(() => {
    if (!chartInstance.current) return;

    // 定義 ECharts 的配置選項。
    const option = {
      series: [
        {
          type: "gauge",
          startAngle: 180,
          endAngle: 0,
          min: 0,
          max:
            currentFlow?.maxCapacity ?? (currentFlow?.currentCount ?? 0) + 50, // 使用 currentFlow 的 maxCapacity 作為最大值
          splitNumber: 10,
          radius: "100%", // 使用最大可能的半徑
          center: ["50%", "60%"], // 將圖表中心點稍微下移
          // 軸線配置
          axisLine: {
            lineStyle: {
              width: 20, // 增加軸線寬度使其更明顯
              color: [
                [0.3, "#67e0e3"],
                [0.7, "#37a2da"],
                [1, "#fd666d"],
              ],
            },
          },
          // 指針配置
          pointer: {
            itemStyle: {
              color: "inherit", // 指針顏色繼承。
            },
          },
          // 軸刻度配置
          axisTick: {
            distance: -20, // 軸刻度與軸線的距離。
            length: 8, // 軸刻度的長度。
            lineStyle: {
              color: "#fff", // 軸刻度顏色。
              width: 1, // 軸刻度寬度。
            },
          },
          // 分割線配置
          splitLine: {
            distance: -12, // 分割線與軸線的距離。
            length: 12, // 分割線的長度。
            lineStyle: {
              color: "#fff", // 分割線顏色。
              width: 1, // 分割線寬度。
            },
          },
          // 軸刻度標籤配置
          axisLabel: {
            color: "#fff", // 標籤文字顏色。
            fontSize: 12, // 標籤文字大小。
            distance: -27, // 標籤與軸線的距離。
            formatter: function (value: number) {
              return Math.round(value);
            },
          },
          // 標題和詳細信息配置
          title: {
            offsetCenter: [0, "-10%"], // 標題位置。
            fontSize: 16, // 標題文字大小。
            fontWeight: "bold", // 標題文字加粗。
            color: "#fff", // 標題文字顏色。
            text: title, // 標題文字內容。
          },
          // 詳細信息配置
          detail: {
            fontSize: 24, // 詳細文字大小。
            offsetCenter: [0, "40%"], // 詳細文字位置。
            valueAnimation: true, // 啟用值動畫。
            formatter: function (value: number) {
              if (currentFlow?.available) {
                return "{value|" + Math.round(value) + "}{unit|人}"; // 格式化顯示
              } else {
                return "{unit|無此設施}"; // 當不可用時
              }
            },
            color: "#fff", // 詳細文字顏色繼承。
            rich: {
              value: {
                fontSize: 30, // 值字體大小
                fontWeight: "bold", // 值字體加粗
                color: "rgba(255, 255, 255, 0.9)", // 值顏色
              },
              unit: {
                fontSize: 18, // 單位字體大小
                fontWeight: "normal", // 單位字體正常
                color: "rgba(255, 255, 255, 0.7)", // 單位顏色
                padding: [0, 0, 0, 4], // 單位內邊距
              },
            },
          },
          data: [
            {
              value: currentFlow?.currentCount || 0, // 儀表板顯示的初始數值。
            },
          ],
        },
      ],
    };

    // 更新 ECharts 的配置。
    chartInstance.current?.setOption(option);
  }, [currentFlow]);

  // 監聽窗口大小變化，並調整圖表大小。
  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // 每 30 秒更新一次儀表板數據
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await authAxios.get(`/api/v1/current_flows`, {
          params: { zip_code: zipCode },
        });
        const flow = response.data.center[type];

        // 更新當前流量數據
        setCurrentFlow({
          available: flow.available,
          currentCount: flow.current_count,
          maxCapacity: flow.max_capacity,
          lastUpdated: flow.last_updated,
        });
      } catch (error) {
        console.error("Error updating gauge data:", error);
      }
    };

    const interval = setInterval(fetchData, 30000); // 每 30 秒更新數據
    fetchData();

    return () => clearInterval(interval);
  }, [zipCode, type, title]);

  // 返回渲染的 JSX 元素，包括圖表容器和文字描述。
  // 根據類型決定背景顏色
  const bgColor =
    type === "gym"
      ? "from-green-400 to-green-600"
      : "from-blue-400 to-blue-600";

  return (
    <div
      className={`bg-gradient-to-r ${bgColor} text-white p-4 rounded-lg shadow-lg`}
    >
      <div className="flex items-center justify-center mb-4">
        <i className={`fas ${icon} text-2xl`} aria-hidden="true"></i>
        <h2 className="text-2xl font-semibold text-center flex-1 flex items-center justify-center -ml-7">
          {title}
        </h2>
      </div>
      <div
        ref={chartRef}
        className="gauge-container"
        style={{
          height: "250px", // 增加高度
          width: "95%", // 確保寬度填滿容器
          margin: "0 auto", // 水平置中
          position: "relative",
          top: "25px", // 往上移動一點，讓圖表更靠近標題
        }}
      />
      <p className="text-center mt-2 font-semibold ">
        最後更新:{" "}
        {currentFlow?.lastUpdated
          ? new Date(currentFlow.lastUpdated).toLocaleTimeString()
          : "---"}
      </p>
    </div>
  );
};
