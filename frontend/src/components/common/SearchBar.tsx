import React from "react";

interface SearchBarProps {
  value: string;
  onSearch: (term: string) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ value, onSearch }) => {
  return (
    <div className="relative">
      <input
        type="text"
        value={value}
        onChange={(e) => onSearch(e.target.value)}
        placeholder="搜尋運動中心..."
        className="w-full px-4 py-2 bg-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <div className="absolute inset-y-0 right-0 flex items-center pr-3">
        <i className="fas fa-search text-gray-400" />
      </div>
    </div>
  );
};
