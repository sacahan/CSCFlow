/**
 * Mapping from Taiwan zip codes to county/city names for weather API
 * Based on Taiwan postal code system
 */

export interface ZipCodeMapping {
  [key: string]: string;
}

export const zipCodeToLocationMap: ZipCodeMapping = {
  // Taipei City (臺北市) - 100-116
  "100": "臺北市",
  "103": "臺北市",
  "104": "臺北市",
  "105": "臺北市",
  "106": "臺北市",
  "108": "臺北市",
  "110": "臺北市",
  "111": "臺北市",
  "112": "臺北市",
  "114": "臺北市",
  "115": "臺北市",
  "116": "臺北市",

  // New Taipei City (新北市) - 200-253
  "220": "新北市",
  "231": "新北市",
  "235": "新北市",
  "236": "新北市",
  "237": "新北市",
  "238": "新北市",
  "239": "新北市",
  "241": "新北市",
  "242": "新北市",
  "244": "新北市",
  "247": "新北市",
  "248": "新北市",
  "251": "新北市",
};

/**
 * Convert zip code to location name for weather API
 * @param zipCode - Taiwan postal code
 * @returns Location name compatible with CWA weather API
 */
export const getLocationFromZipCode = (zipCode: string): string => {
  const location = zipCodeToLocationMap[zipCode];

  if (!location) {
    console.warn(`Unknown zip code: ${zipCode}, defaulting to 新北市`);
    return "新北市";
  }

  return location;
};

/**
 * Get all supported zip codes
 * @returns Array of supported zip codes
 */
export const getSupportedZipCodes = (): string[] => {
  return Object.keys(zipCodeToLocationMap);
};
