import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  getDefaultCenterZipCode,
  setDefaultCenterZipCode,
  clearDefaultCenterZipCode,
  isDefaultCenter,
} from '../src/utils/userPreferences';

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
global.localStorage = localStorageMock as any;

describe('userPreferences', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getDefaultCenterZipCode', () => {
    it('should return stored zip code from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('235');
      
      const result = getDefaultCenterZipCode();
      
      expect(result).toBe('235');
      expect(localStorageMock.getItem).toHaveBeenCalledWith('cscflow_default_center_zip_code');
    });

    it('should return null when nothing is stored', () => {
      localStorageMock.getItem.mockReturnValue(null);
      
      const result = getDefaultCenterZipCode();
      
      expect(result).toBeNull();
    });

    it('should return null and log warning when localStorage throws error', () => {
      const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
      localStorageMock.getItem.mockImplementation(() => {
        throw new Error('localStorage error');
      });
      
      const result = getDefaultCenterZipCode();
      
      expect(result).toBeNull();
      expect(consoleSpy).toHaveBeenCalledWith(
        'Failed to read default center preference from localStorage:',
        expect.any(Error)
      );
      
      consoleSpy.mockRestore();
    });
  });

  describe('setDefaultCenterZipCode', () => {
    it('should store zip code in localStorage', () => {
      setDefaultCenterZipCode('104');
      
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'cscflow_default_center_zip_code',
        '104'
      );
    });

    it('should log warning when localStorage throws error', () => {
      const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
      localStorageMock.setItem.mockImplementation(() => {
        throw new Error('localStorage error');
      });
      
      setDefaultCenterZipCode('104');
      
      expect(consoleSpy).toHaveBeenCalledWith(
        'Failed to save default center preference to localStorage:',
        expect.any(Error)
      );
      
      consoleSpy.mockRestore();
    });
  });

  describe('clearDefaultCenterZipCode', () => {
    it('should remove zip code from localStorage', () => {
      clearDefaultCenterZipCode();
      
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('cscflow_default_center_zip_code');
    });

    it('should log warning when localStorage throws error', () => {
      const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
      localStorageMock.removeItem.mockImplementation(() => {
        throw new Error('localStorage error');
      });
      
      clearDefaultCenterZipCode();
      
      expect(consoleSpy).toHaveBeenCalledWith(
        'Failed to clear default center preference from localStorage:',
        expect.any(Error)
      );
      
      consoleSpy.mockRestore();
    });
  });

  describe('isDefaultCenter', () => {
    it('should return true when zip code matches stored default', () => {
      localStorageMock.getItem.mockReturnValue('235');
      
      const result = isDefaultCenter('235');
      
      expect(result).toBe(true);
    });

    it('should return false when zip code does not match stored default', () => {
      localStorageMock.getItem.mockReturnValue('235');
      
      const result = isDefaultCenter('104');
      
      expect(result).toBe(false);
    });

    it('should return false when no default is stored', () => {
      localStorageMock.getItem.mockReturnValue(null);
      
      const result = isDefaultCenter('235');
      
      expect(result).toBe(false);
    });
  });
});