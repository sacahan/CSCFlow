import axios from "axios";

const CWA_API_BASE = "https://opendata.cwa.gov.tw/api/v1/rest/datastore";
const WEATHER_ENDPOINT = "F-C0032-001";
const axiosInstance = axios.create(); // 創建獨立的 axios 實例

interface WeatherElement {
  elementName: string;
  time: Array<{
    startTime: string;
    endTime: string;
    parameter: {
      parameterName: string;
      parameterUnit?: string;
    };
  }>;
}

interface WeatherResponse {
  success: boolean;
  records: {
    location: Array<{
      locationName: string;
      weatherElement: WeatherElement[];
    }>;
  };
}

export interface WeatherData {
  locationName: string; // 地點名稱
  weather: string; // Wx
  rainChance: number; // PoP
  minTemperature: number; // MinT
  maxTemperature: number; // MaxT
  comfortLevel: string; // CI
}

export const fetchWeatherData = async (
  locationName: string = "新北市",
): Promise<WeatherData> => {
  try {
    const now = new Date();
    const timeTo = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate(),
      18,
      0,
      0,
    );

    const response = await axiosInstance.get<WeatherResponse>(
      `${CWA_API_BASE}/${WEATHER_ENDPOINT}`,
      {
        params: {
          Authorization: import.meta.env.VITE_CWA_API_KEY,
          locationName,
          limit: 1,
          sort: "time",
        },
      },
    );

    if (!response.data.success) {
      throw new Error("Weather API request failed");
    }

    const location = response.data.records.location[0];
    const elements = location.weatherElement;

    const getElementValue = (elementName: string): string => {
      const element = elements.find((el) => el.elementName === elementName);
      return element?.time[0].parameter.parameterName || "";
    };

    return {
      locationName: location.locationName,
      weather: getElementValue("Wx"),
      rainChance: Number(getElementValue("PoP")) || 0,
      minTemperature: Number(getElementValue("MinT")) || 0,
      maxTemperature: Number(getElementValue("MaxT")) || 0,
      comfortLevel: getElementValue("CI"),
    };
  } catch (error) {
    console.error("Error fetching weather data:", error);
    return {
      locationName: locationName,
      weather: "資料載入中",
      rainChance: 0,
      minTemperature: 0,
      maxTemperature: 0,
      comfortLevel: "資料載入中",
    };
  }
};
