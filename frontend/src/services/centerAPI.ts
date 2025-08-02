import { authAxios } from "./authAPI";

interface SportCenter {
  name: string;
  zip_code: string;
  address: string;
  website_url: string;
  facility_info: {
    gym: {
      available: number;
      max_capacity: number;
    };
    pool: {
      available: number;
      max_capacity: number;
    };
  };
  status?: string;
}

export const fetchSportCenters = async (): Promise<SportCenter[]> => {
  try {
    const response = await authAxios.get("/api/v1/centers/");

    return response.data;
  } catch (error) {
    console.error("Error fetching sport centers:", error);
    return [];
  }
};
