import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

interface GaugeProps {
  title: string;
  maxCapacity: number;
  value: number;
}

export const Gauge: React.FC<GaugeProps> = ({ title, maxCapacity, value }) => {
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

    const percentage = (value / maxCapacity) * 100;

    const option = {
      series: [{
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        min: 0,
        max: 100,
        splitNumber: 10,
        axisLine: {
          lineStyle: {
            width: 20,
            color: [
              [0.3, '#67e0e3'],
              [0.7, '#37a2da'],
              [1, '#fd666d']
            ]
          }
        },
        pointer: {
          itemStyle: {
            color: 'inherit'
          }
        },
        axisTick: {
          distance: -30,
          length: 8,
          lineStyle: {
            color: '#fff',
            width: 2
          }
        },
        splitLine: {
          distance: -30,
          length: 30,
          lineStyle: {
            color: '#fff',
            width: 2
          }
        },
        axisLabel: {
          color: '#464646',
          fontSize: 14,
          distance: -60,
          formatter: function(value: number) {
            return value + '%';
          }
        },
        title: {
          offsetCenter: [0, '-20%'],
          fontSize: 16,
          fontWeight: 'bold',
          color: '#464646',
          text: title
        },
        detail: {
          fontSize: 24,
          offsetCenter: [0, '20%'],
          valueAnimation: true,
          formatter: function(value: number) {
            return value + '%';
          },
          color: 'inherit'
        },
        data: [{
          value: percentage
        }]
      }]
    };

    chartInstance.current.setOption(option);
  }, [title, maxCapacity, value]);

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
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <div ref={chartRef} className="w-full h-[250px]" />
      <div className="text-center mt-2">
        <p className="text-gray-600">當前人數：{value}</p>
        <p className="text-gray-600">總容量：{maxCapacity}</p>
      </div>
    </div>
  );
};
