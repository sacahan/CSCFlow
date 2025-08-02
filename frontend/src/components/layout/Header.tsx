import React from "react";

interface Center {
  zipCode: string;
  name: string;
  address: string;
  websiteUrl: string;
}

interface HeaderProps {
  selectedCenter: Center | null;
  onToggleSidebar: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  selectedCenter,
  onToggleSidebar,
}) => {
  return (
    <header className="mb-4 sm:mt-0 flex items-center w-full justify-between">
      <button
        onClick={onToggleSidebar}
        className="sm:hidden p-2 rounded-lg hover:bg-gray-700 focus:outline-none"
      >
        <i className="fas fa-bars text-xl"></i>
      </button>
      {selectedCenter ? (
        <div className="flex items-center flex-1 min-w-0">
          <h1 className="text-2xl font-bold ml-1">
            <a
              href={selectedCenter?.websiteUrl || "#"}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:underline"
            >
              {selectedCenter.name}
            </a>
          </h1>
          <span className="text-sm text-gray-500" style={{ marginLeft: "5px" }}>
            <a
              href={`https://www.google.com/maps/search/?api=1&query=${selectedCenter.address}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <i className="fas fa-map-marker-alt"></i> 地圖
            </a>
          </span>
        </div>
      ) : (
        <h1 className="text-2xl font-bold ml-1 flex-1">運動中心 Dashboard</h1>
      )}
      <img src="logo.png" width={150} alt="Logo" className="h-8 w-8" />
    </header>
  );
};
