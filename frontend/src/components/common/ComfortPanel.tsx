import React from 'react';

interface ComfortPanelProps {
  comfortLevel: string;
}

export const ComfortPanel: React.FC<ComfortPanelProps> = ({ comfortLevel }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">體感舒適度</h3>
      <div className="text-center">
        <p className="text-xl font-medium text-gray-700">{comfortLevel}</p>
      </div>
    </div>
  );
};
