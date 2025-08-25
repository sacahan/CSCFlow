/**
 * User preferences management using localStorage
 */

const STORAGE_KEYS = {
  DEFAULT_CENTER_ZIP_CODE: "cscflow_default_center_zip_code",
} as const;

/**
 * Get the user's preferred default center zip code
 * @returns The zip code of the preferred center, or null if not set
 */
export const getDefaultCenterZipCode = (): string | null => {
  try {
    return localStorage.getItem(STORAGE_KEYS.DEFAULT_CENTER_ZIP_CODE);
  } catch (error) {
    console.warn(
      "Failed to read default center preference from localStorage:",
      error,
    );
    return null;
  }
};

/**
 * Set the user's preferred default center zip code
 * @param zipCode The zip code to set as default
 */
export const setDefaultCenterZipCode = (zipCode: string): void => {
  try {
    localStorage.setItem(STORAGE_KEYS.DEFAULT_CENTER_ZIP_CODE, zipCode);
  } catch (error) {
    console.warn(
      "Failed to save default center preference to localStorage:",
      error,
    );
  }
};

/**
 * Clear the user's preferred default center zip code
 */
export const clearDefaultCenterZipCode = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEYS.DEFAULT_CENTER_ZIP_CODE);
  } catch (error) {
    console.warn(
      "Failed to clear default center preference from localStorage:",
      error,
    );
  }
};

/**
 * Check if a center is set as the user's default
 * @param zipCode The zip code to check
 * @returns True if this center is set as default
 */
export const isDefaultCenter = (zipCode: string): boolean => {
  return getDefaultCenterZipCode() === zipCode;
};
