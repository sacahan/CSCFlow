import React, { useState, useCallback } from 'react';
import { debounce } from 'lodash';
import { SearchBar } from '../common/SearchBar';
import { CenterList } from './CenterList';

interface SidebarProps {
  centers: Array<{
    id: string;
    name: string;
  }>;
  onSelectCenter: (centerId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ centers, onSelectCenter }) => {
  const [isOpen, setIsOpen] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredCenters, setFilteredCenters] = useState(centers);

  const handleSearch = useCallback(
    debounce((term: string) => {
      const filtered = centers.filter(center =>
        center.name.toLowerCase().includes(term.toLowerCase())
      );
      setFilteredCenters(filtered);
    }, 300),
    [centers]
  );

  const handleSearchChange = (term: string) => {
    setSearchTerm(term);
    handleSearch(term);
  };

  return (
    <>
      <aside
        className={`w-64 h-screen bg-gray-800 text-white p-4 fixed left-0 overflow-y-auto transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } transition-transform duration-300 ease-in-out z-40`}
      >
        <div className="mb-6 mt-10 sm:mt-0">
          <h2 className="text-xl font-semibold mb-4">運動中心列表</h2>
          <SearchBar value={searchTerm} onSearch={handleSearchChange} />
        </div>

        <CenterList centers={filteredCenters} onSelect={onSelectCenter} />

        <footer className="mt-4 text-center text-gray-400 fixed bottom-0 w-full md:-ml-5 -ml-20 mb-4">
          <p>作者: Sacahan</p>
        </footer>
      </aside>

      {/* 手機版遮罩 */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 sm:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
};
