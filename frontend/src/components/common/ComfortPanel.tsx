import React from 'react';

interface ComfortPanelProps {
  comfortLevel: string;
}

export const ComfortPanel: React.FC<ComfortPanelProps> = ({ comfortLevel }) => {
  return (
    <div className="bg-gradient-to-r from-indigo-400 to-indigo-500 text-white p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-2">
        <i className="fas fa-tint"></i> 體感
      </h2>
      <p>
        <span className="font-bold">{comfortLevel}</span>
      </p>
    </div>
  );
};
