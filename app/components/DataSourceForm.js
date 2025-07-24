'use client';

import { useState } from 'react';

export default function DataSourceForm({ onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    centerName: '',
    apiUrl: '',
    maxCapacity: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/datasources', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        onSubmit();
        onClose();
      } else {
        const error = await response.json();
        alert(error.message);
      }
    } catch (error) {
      console.error('Error creating data source:', error);
      alert('建立資料來源時發生錯誤');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">新增資料來源</h2>

        <div className="mb-4">
          <label className="block mb-2">運動中心名稱</label>
          <input
            type="text"
            name="centerName"
            value={formData.centerName}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">API URL</label>
          <input
            type="url"
            name="apiUrl"
            value={formData.apiUrl}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">最大容客數</label>
          <input
            type="number"
            name="maxCapacity"
            value={formData.maxCapacity}
            onChange={handleChange}
            required
            min="1"
            className="w-full px-3 py-2 border rounded"
          />
        </div>

        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border rounded"
          >
            取消
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded"
          >
            提交
          </button>
        </div>
      </form>
    </div>
  );
}
