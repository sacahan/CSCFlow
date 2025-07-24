'use client';

import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function FlowChart({ dataSourceId }) {
  const [flowData, setFlowData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/flowdata/${dataSourceId}`);
        const data = await response.json();
        setFlowData(data);
      } catch (error) {
        console.error('Error fetching flow data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // 每分鐘更新一次
    return () => clearInterval(interval);
  }, [dataSourceId]);

  const data = {
    labels: flowData.map(d => new Date(d.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: '即時人數',
        data: flowData.map(d => d.currentCount),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '人流變化趨勢'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  return (
    <div className="p-4 bg-white rounded shadow-md mt-4">
      <Line
        data={data}
        options={options}
        className="max-w-full h-auto"
      />
    </div>
  );
}
