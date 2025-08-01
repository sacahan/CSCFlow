// 引入必要的 React 和 echarts 庫
import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

// 定義趨勢數據的介面，包含時間和各場地的使用人數
interface TrendData {
    time: string;
    gym: number;
    pool: number;
}

// 定義組件屬性的介面，包含數據陣列和時間範圍選項
interface TrendChartProps {
    data: TrendData[];
    timeRange: 'daily' | 'weekly' | 'monthly';
}

export const TrendChart: React.FC<TrendChartProps> = ({ data, timeRange }) => {
    // 建立圖表容器和實例的參考
    const chartRef = useRef<HTMLDivElement>(null);
    const chartInstance = useRef<echarts.ECharts | null>(null);

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
                trigger: 'axis',
                formatter: function (params: any) {
                    const time = params[0].name;
                    return `${time}<br/>${params.map((param: any) => param).join('')}`;
                }
            },
            // 配置圖例，設定顏色樣式
            legend: {
                data: ['健身房', '游泳池'],
                textStyle: {
                    color: '#ffffff'
                },
                top: 0,  // 將圖例放置在頂部
                left: 'center'  // 水平置中
            },
            // 配置網格佈局
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                top: '10%',  // 為上方圖例留出空間
                containLabel: true
            },
            // 配置 X 軸，設定為時間類別
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
            // 配置 Y 軸，設定為數值類型
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
            // 配置數據系列
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

    // 監聽視窗大小變化，適配圖表尺寸
    useEffect(() => {
        const handleResize = () => {
            if (chartInstance.current) {
                chartInstance.current.resize();
            }
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    // 渲染圖表容器和控制按鈕
    return (
        <div className="bg-gradient-to-r from-teal-500 to-teal-700 p-6 rounded-lg shadow-lg">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-white text-lg font-semibold">累積人數趨勢</h3>
                <div className="flex gap-2">
                    <button
                        className={`px-3 py-1 rounded ${timeRange === 'daily' ? 'bg-white text-teal-700' : 'bg-teal-600 text-white'
                            }`}
                    >
                        每日
                    </button>
                    <button
                        className={`px-3 py-1 rounded ${timeRange === 'weekly' ? 'bg-white text-teal-700' : 'bg-teal-600 text-white'
                            }`}
                    >
                        每週
                    </button>
                    <button
                        className={`px-3 py-1 rounded ${timeRange === 'monthly' ? 'bg-white text-teal-700' : 'bg-teal-600 text-white'
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
