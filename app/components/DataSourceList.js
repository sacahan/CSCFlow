'use client';

import { useState, useEffect } from 'react';
import DataSourceForm from './DataSourceForm';
import FlowChart from './FlowChart';

export default function DataSourceList() {
  const [dataSources, setDataSources] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchDataSources();
  }, []);

  const fetchDataSources = async () => {
    try {
      const response = await fetch('/api/datasources');
      const data = await response.json();
      setDataSources(data);
    } catch (error) {
      console.error('Error fetching data sources:', error);
    }
  };

  const filteredDataSources = dataSources.filter(source =>
    source.centerName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div className="flex justify-between mb-4">
        <input
          type="text"
          placeholder="搜尋運動中心..."
          className="px-4 py-2 border rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600"
          onClick={() => setIsFormOpen(true)}
        >
          新增資料來源
        </button>
      </div>

      {isFormOpen && (
        <DataSourceForm
          onClose={() => setIsFormOpen(false)}
          onSubmit={fetchDataSources}
        />
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredDataSources.map((source) => (
          <div key={source.id} className="border p-4 rounded">
            <h3 className="text-xl font-bold">{source.centerName}</h3>
            <p>最大容客數：{source.maxCapacity}</p>
            <p>狀態：{source.status}</p>
            <FlowChart dataSourceId={source.id} />
          </div>
        ))}
      </div>
    </div>
  );
}
