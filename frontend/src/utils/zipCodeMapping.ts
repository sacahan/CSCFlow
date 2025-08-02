/**
 * Mapping from Taiwan zip codes to county/city names for weather API
 * Based on Taiwan postal code system
 */

export interface ZipCodeMapping {
  [key: string]: string;
}

export const zipCodeToLocationMap: ZipCodeMapping = {
  // Taipei City (台北市) - 100-116
  '100': '台北市',
  '103': '台北市', 
  '104': '台北市',
  '105': '台北市',
  '106': '台北市',
  '108': '台北市',
  '110': '台北市',
  '111': '台北市',
  '112': '台北市',
  '114': '台北市',
  '115': '台北市',
  '116': '台北市',
  
  // New Taipei City (新北市) - 200-253
  '220': '新北市',
  '231': '新北市', 
  '235': '新北市',
  '236': '新北市',
  '237': '新北市',
  '238': '新北市',
  '239': '新北市',
  '241': '新北市',
  '242': '新北市',
  '244': '新北市',
  '247': '新北市',
  '248': '新北市',
  '251': '新北市',
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
    return '新北市';
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