import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

// 定義 GaugeProps 介面，包含三個屬性：title（標題）、maxCapacity（最大容量）和 value（當前值）。
interface GaugeProps {
	title: string;
	maxCapacity: number;
	value: number;
	type: 'gym' | 'pool';  // 新增 type 屬性來區分不同類型
	icon: string;  // 新增 icon 屬性來設置 Font Awesome 圖示
}

// 定義 Gauge 元件，使用 React.FC 並接收 GaugeProps 作為屬性。
export const Gauge: React.FC<GaugeProps> = ({ title, maxCapacity, value, type, icon }) => {
	// 使用 useRef 建立 chartRef 來存放圖表的 DOM 節點。
	const chartRef = useRef<HTMLDivElement>(null);
	// 使用 useRef 建立 chartInstance 來存放 ECharts 實例。
	const chartInstance = useRef<echarts.ECharts | null>(null);

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

		// 計算百分比值，用於顯示在儀表板上。
		const percentage = (value / maxCapacity) * 100;

		// 定義 ECharts 的配置選項。
		const option = {
			series: [{
				type: 'gauge',
				startAngle: 180,
				endAngle: 0,
				min: 0,
				max: 100,
				splitNumber: 10,
				radius: '100%',      // 使用最大可能的半徑
				center: ['50%', '60%'], // 將圖表中心點稍微下移
                // 軸線配置
				axisLine: {
					lineStyle: {
						width: 20, // 增加軸線寬度使其更明顯
						color: [
							[0.3, '#67e0e3'],
							[0.7, '#37a2da'],
							[1, '#fd666d']
						]
					}
				},
                // 指針配置
				pointer: {
					itemStyle: {
						color: 'inherit' // 指針顏色繼承。
					}
				},
                // 軸刻度配置
				axisTick: {
					distance: -20, // 軸刻度與軸線的距離。
					length: 8, // 軸刻度的長度。
					lineStyle: {
						color: '#fff', // 軸刻度顏色。
						width: 1 // 軸刻度寬度。
					}
				},
                // 軸刻度標籤配置
				splitLine: {
					distance: -12, // 分割線與軸線的距離。
					length: 12, // 分割線的長度。
					lineStyle: {
						color: '#fff', // 分割線顏色。
						width: 1 // 分割線寬度。
					}
				},
                // 軸刻度標籤配置
				axisLabel: {
					color: '#fff', // 標籤文字顏色。
					fontSize: 12, // 標籤文字大小。
					distance: -27, // 標籤與軸線的距離。
                    formatter: function(value: number) {
						return value + '%'; // 格式化標籤文字為百分比。
					}
				},
                // 標題和詳細信息配置
				title: {
					offsetCenter: [0, '-10%'], // 標題位置。
					fontSize: 16, // 標題文字大小。
					fontWeight: 'bold', // 標題文字加粗。
					color: '#fff', // 標題文字顏色。
					text: title // 標題文字內容。
				},
                // 詳細信息配置
				detail: {
					fontSize: 24, // 詳細文字大小。
					offsetCenter: [0, '40%'], // 詳細文字位置。
					valueAnimation: true, // 啟用值動畫。
					formatter: function(value: number) {
						return value + '%'; // 格式化詳細文字為百分比。
					},
					color: '#fff' // 詳細文字顏色繼承。
				},
				data: [{
					value: percentage // 儀表板顯示的數值。
				}]
			}]
		};

		// 更新 ECharts 的配置。
		chartInstance.current.setOption(option);
	}, [title, maxCapacity, value]);

	// 監聽窗口大小變化，並調整圖表大小。
	useEffect(() => {
		const handleResize = () => {
			if (chartInstance.current) {
				chartInstance.current.resize();
			}
		};

		window.addEventListener('resize', handleResize);
		return () => window.removeEventListener('resize', handleResize);
	}, []);

	// 返回渲染的 JSX 元素，包括圖表容器和文字描述。
	// 根據類型決定背景顏色
	const bgColor = type === 'gym'
		? 'from-green-400 to-green-600'
		: 'from-blue-400 to-blue-600';

	return (
		<div className={`bg-gradient-to-r ${bgColor} text-white p-4 rounded-lg shadow-lg`}>
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
					height: '250px',  // 增加高度
					width: '95%',    // 確保寬度填滿容器
					margin: '0 auto', // 水平置中
					position: 'relative',
					top: '25px'      // 往上移動一點，讓圖表更靠近標題
				}}
			/>
		</div>
	);
};
