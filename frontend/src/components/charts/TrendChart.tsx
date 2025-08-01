import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

interface TrendData {
  time: string;
  gym: number;
  pool: number;
}

interface TrendChartProps {
  data: TrendData[];
  timeRange: 'daily' | 'weekly' | 'monthly';
}

export const TrendChart: React.FC<TrendChartProps> = ({ data, timeRange }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

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

  useEffect(() => {
    if (!chartInstance.current) return;

    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: function(params: any) {
          const time = params[0].name;
          return \`\${time}<br/>\${params.map((param: any) =>
            \`\${param.seriesName}: \${param.value}人\`).join('<br/>')}\`;
        }
      },
      legend: {
        data: ['健身房', '游泳池'],
        textStyle: {
          color: '#ffffff'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: data.map(item => item.time),
        axisLabel: {
          color: '#ffffff'
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.5)'
          }
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          formatter: '{value}人',
          color: '#ffffff'
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.5)'
          }
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.2)'
          }
        }
      },
      series: [
        {
          name: '健身房',
          type: 'line',
          data: data.map(item => item.gym),
          smooth: true,
          areaStyle: {
            opacity: 0.3
          },
          emphasis: {
            focus: 'series'
          },
          lineStyle: {
            width: 3
          },
          itemStyle: {
            borderWidth: 2
          }
        },
        {
          name: '游泳池',
          type: 'line',
          data: data.map(item => item.pool),
          smooth: true,
          areaStyle: {
            opacity: 0.3
          },
          emphasis: {
            focus: 'series'
          },
          lineStyle: {
            width: 3
          },
          itemStyle: {
            borderWidth: 2
          }
        }
      ]
    };

    chartInstance.current.setOption(option);
  }, [data]);

  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="bg-gradient-to-r from-teal-500 to-teal-700 p-6 rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-white text-lg font-semibold">累積人數趨勢</h3>
        <div className="flex gap-2">
          <button
            className={`px-3 py-1 rounded ${
              timeRange === 'daily' ? 'bg-white text-teal-700' : 'bg-teal-600 text-white'
            }`}
          >
            每日
          </button>
          <button
            className={`px-3 py-1 rounded ${
              timeRange === 'weekly' ? 'bg-white text-teal-700' : 'bg-teal-600 text-white'
            }`}
          >
            每週
          </button>
          <button
            className={`px-3 py-1 rounded ${
              timeRange === 'monthly' ? 'bg-white text-teal-700' : 'bg-teal-600 text-white'
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
