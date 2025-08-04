import { describe, it, expect } from "vitest";
import {
  getLocationFromZipCode,
  getSupportedZipCodes,
  zipCodeToLocationMap,
} from "../src/utils/zipCodeMapping";

describe("zipCodeMapping", () => {
  describe("getLocationFromZipCode", () => {
    it("should return correct location for Taipei City zip codes", () => {
      expect(getLocationFromZipCode("100")).toBe("台北市");
      expect(getLocationFromZipCode("104")).toBe("台北市");
      expect(getLocationFromZipCode("116")).toBe("台北市");
    });

    it("should return correct location for New Taipei City zip codes", () => {
      expect(getLocationFromZipCode("235")).toBe("新北市");
      expect(getLocationFromZipCode("220")).toBe("新北市");
      expect(getLocationFromZipCode("251")).toBe("新北市");
    });

    it("should return default location for unknown zip codes", () => {
      expect(getLocationFromZipCode("999")).toBe("新北市");
      expect(getLocationFromZipCode("")).toBe("新北市");
    });
  });

  describe("getSupportedZipCodes", () => {
    it("should return array of all supported zip codes", () => {
      const supportedCodes = getSupportedZipCodes();
      expect(supportedCodes).toBeInstanceOf(Array);
      expect(supportedCodes.length).toBeGreaterThan(0);
      expect(supportedCodes).toContain("235");
      expect(supportedCodes).toContain("100");
    });
  });

  describe("zipCodeToLocationMap", () => {
    it("should contain expected sport center zip codes", () => {
      // Test some specific zip codes from the sport center list
      expect(zipCodeToLocationMap["235"]).toBe("新北市"); // 中和國民運動中心
      expect(zipCodeToLocationMap["104"]).toBe("台北市"); // 中山運動中心
      expect(zipCodeToLocationMap["100"]).toBe("台北市"); // 中正運動中心
    });
  });
});
