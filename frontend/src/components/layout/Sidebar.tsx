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
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isAuthLoading,
  onSelectCenter,
  isOpen,
  onClose,
}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [centers, setCenters] = useState<Center[]>([]);
  const [filteredCenters, setFilteredCenters] = useState<Center[]>([]);

  useEffect(() => {
    const loadCenters = async () => {
      try {
        const data = await fetchSportCenters();
        if (data.length > 0) {
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
          return;
        }
      } catch (err) {
        console.error("Error loading centers:", err);
      }

      // Fallback mock data for testing when API is not available
      const mockCenters = [
        {
          zipCode: "235",
          name: "新北市中和國民運動中心",
          address: "新北市中和區錦和路350-1、2號",
          websiteUrl: "https://www.zhsc.com.tw/",
        },
        {
          zipCode: "104",
          name: "台北市中山運動中心",
          address: "台北市中山區中山北路二段44巷2號",
          websiteUrl: "https://cssc.cyc.org.tw/",
        },
        {
          zipCode: "100",
          name: "台北市中正運動中心",
          address: "台北市中正區信義路一段1號",
          websiteUrl: "https://wsjjsc.com.tw/",
        },
        {
          zipCode: "251",
          name: "新北市淡水國民運動中心",
          address: "新北市淡水區中山北路二段381巷2號",
          websiteUrl: "http://www.tssc.tw/",
        },
      ];
      
      setCenters(mockCenters);
      setFilteredCenters(mockCenters);
      
      // Select default center (zip code 235)
      const defaultCenter = mockCenters.find(center => center.zipCode === "235");
      if (defaultCenter) {
        onSelectCenter(defaultCenter);
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

  const handleSelectCenter = (center: Center) => {
    onSelectCenter(center);
    if (window.innerWidth <= 640) {
      // 判斷是否為手機螢幕
      onClose();
    }
  };

  return (
    <>
      <aside
        className={`w-64 h-screen bg-gray-800 text-white p-4 fixed left-0 overflow-y-auto transform ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } sm:translate-x-0 transition-transform duration-300 ease-in-out z-40`}
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
          <CenterList centers={filteredCenters} onSelect={handleSelectCenter} />
        )}
      </aside>

      {/* 手機版遮罩 */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 sm:hidden"
          onClick={onClose}
        />
      )}
    </>
  );
};
