import React, { useState } from "react";
import { isDefaultCenter, setDefaultCenterZipCode, clearDefaultCenterZipCode } from "../../utils/userPreferences";

interface Center {
  zipCode: string;
  name: string;
  address: string;
  websiteUrl: string;
}

interface CenterListProps {
  centers: Center[];
  onSelect: (center: Center) => void;
}

export const CenterList: React.FC<CenterListProps> = ({
  centers,
  onSelect,
}) => {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleSelect = (center: Center) => {
    setSelectedId(center.zipCode);
    onSelect(center);
  };

  const handleToggleDefault = (center: Center, event: React.MouseEvent) => {
    event.stopPropagation(); // Prevent triggering center selection
    
    if (isDefaultCenter(center.zipCode)) {
      clearDefaultCenterZipCode();
    } else {
      setDefaultCenterZipCode(center.zipCode);
    }
    
    // Force re-render by updating state
    setSelectedId(prev => prev); // Trigger re-render
  };

  return (
    <ul className="space-y-2">
      {centers.map((center) => (
        <li key={center.zipCode}>
          <div
            className={`w-full px-4 py-2 rounded-lg hover:bg-gray-700 focus-within:bg-gray-700 transition-colors ${
              selectedId === center.zipCode ? "bg-gray-700" : ""
            }`}
          >
            <div className="flex items-center justify-between">
              <button
                onClick={() => handleSelect(center)}
                className="flex-1 text-left focus:outline-none"
              >
                {center.name}
              </button>
              <button
                onClick={(e) => handleToggleDefault(center, e)}
                className={`ml-2 p-1 rounded hover:bg-gray-600 focus:outline-none transition-colors ${
                  isDefaultCenter(center.zipCode) 
                    ? "text-yellow-400" 
                    : "text-gray-400 hover:text-yellow-400"
                }`}
                title={isDefaultCenter(center.zipCode) ? "取消設為預設" : "設為預設顯示"}
              >
                {isDefaultCenter(center.zipCode) ? (
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
};
