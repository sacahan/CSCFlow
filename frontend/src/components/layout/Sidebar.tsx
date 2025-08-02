import React, { useState, useCallback, useEffect } from "react";
import { debounce } from "lodash";
import { SearchBar } from "../common/SearchBar";
import { CenterList } from "./CenterList";
import { fetchSportCenters } from "../../services/centerAPI";

interface Center {
  zipCode: string;
  name: string;
  address: string;
  websiteUrl: string;
}

interface SidebarProps {
  isAuthLoading: boolean;
  onSelectCenter: (center: Center) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isAuthLoading,
  onSelectCenter,
}) => {
  const [isOpen, setIsOpen] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [centers, setCenters] = useState<Center[]>([]);
  const [filteredCenters, setFilteredCenters] = useState<Center[]>([]);

  useEffect(() => {
    const loadCenters = async () => {
      try {
        const data = await fetchSportCenters();
        const formattedCenters = data.map((center) => ({
          zipCode: center.zip_code,
          name: center.name,
          address: center.address,
          websiteUrl: center.website_url,
        }));
        setCenters(formattedCenters);
        setFilteredCenters(formattedCenters);

        // 從data中選擇zipCode=235作為預設選擇
        const defaultCenter = formattedCenters.find(
          (center) => center.zipCode === "235",
        );
        if (defaultCenter) {
          onSelectCenter(defaultCenter);
        }
      } catch (err) {
        console.error("Error loading centers:", err);
      }
    };

    loadCenters();
  }, []);

  const handleSearch = useCallback(
    debounce((term: string) => {
      const filtered = centers.filter((center) =>
        center.name.toLowerCase().includes(term.toLowerCase()),
      );
      setFilteredCenters(filtered);
    }, 300),
    [centers],
  );

  const handleSearchChange = (term: string) => {
    setSearchTerm(term);
    handleSearch(term);
  };

  const handleClearSearch = () => {
    setSearchTerm("");
    setFilteredCenters(centers);
  };

  return (
    <>
      <aside
        className={`w-64 h-screen bg-gray-800 text-white p-4 fixed left-0 overflow-y-auto transform ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } transition-transform duration-300 ease-in-out z-40`}
      >
        <div className="mb-6 mt-10 sm:mt-0">
          <h2 className="text-xl font-semibold mb-4">運動中心列表</h2>
          <SearchBar
            value={searchTerm}
            onSearch={handleSearchChange}
            onClear={handleClearSearch}
          />
        </div>

        {isAuthLoading ? (
          <div className="text-center text-gray-400">載入中...</div>
        ) : (
          <CenterList centers={filteredCenters} onSelect={onSelectCenter} />
        )}

        {/* 手機版遮罩 */}
        {isOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-30 sm:hidden"
            onClick={() => setIsOpen(false)}
          />
        )}
      </aside>
    </>
  );
};
