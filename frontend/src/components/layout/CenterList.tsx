import React, { useState } from "react";

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

  return (
    <ul className="space-y-2">
      {centers.map((center) => (
        <li key={center.zipCode}>
          <button
            onClick={() => handleSelect(center)}
            className={`w-full px-4 py-2 text-left rounded-lg hover:bg-gray-700 focus:outline-none transition-colors ${
              selectedId === center.zipCode ? "bg-gray-700" : ""
            }`}
          >
            {center.name}
          </button>
        </li>
      ))}
    </ul>
  );
};
