import React from 'react';

interface HeaderProps {
  onToggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleSidebar }) => {
  return (
    <header className="mb-4 sm:mt-0 flex items-center">
      <button
        onClick={onToggleSidebar}
        className="sm:hidden p-2 rounded-lg hover:bg-gray-700 focus:outline-none"
      >
        <i className="fas fa-bars text-xl"></i>
      </button>
      <h1 className="text-2xl font-bold ml-4">運動中心 Dashboard</h1>
    </header>
  );
};
