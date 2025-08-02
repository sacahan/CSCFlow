import axios from "axios";

/**
 * 定義登入回應的資料結構。
 * 包含 access_token 和 token 的有效期限。
 */
interface LoginResponse {
  access_token: string; // 用於 API 驗證的存取令牌
  expires_in: number; // 存取令牌的有效期限（秒）
}

/**
 * AuthService 類別負責處理與身份驗證相關的操作。
 * 包括登入、確保身份驗證以及管理存取令牌。
 */
class AuthService {
  private static instance: AuthService; // 單例模式的實例
  private isRefreshing = false; // 標記是否正在刷新 token
  private subscribers: Array<(token: string) => void> = []; // 等待 token 刷新的請求隊列
  private readonly authAxios = axios.create(); // 創建獨立的 axios 實例

  private constructor() {
    // 初始化 authAxios headers
    const token = localStorage.getItem("access_token");
    if (token) {
      this.setupAuthHeaders(token);
    }

    // 配置 authAxios 攔截器
    this.authAxios.interceptors.response.use(
      (response) => response, // 成功回應直接返回
      async (error) => {
        const originalRequest = error.config;

        // 如果回應狀態為 401/403 且尚未重試，則嘗試刷新 token
        if (
          (error.response?.status === 401 || error.response?.status === 403) &&
          !originalRequest._retry
        ) {
          if (this.isRefreshing) {
            // 如果正在刷新 token，將請求加入等待隊列
            try {
              const token = await new Promise<string>((resolve) => {
                this.subscribers.push(resolve);
              });
              originalRequest.headers["Authorization"] = `Bearer ${token}`;
              return this.authAxios(originalRequest); // 使用新的 token 重試請求
            } catch (err) {
              return Promise.reject(err);
            }
          }

          originalRequest._retry = true; // 標記請求已重試
          this.isRefreshing = true; // 開始刷新 token

          try {
            const token = await this.login(); // 重新登入以獲取新的 token
            this.subscribers.forEach((callback) => callback(token)); // 通知所有等待的請求
            this.subscribers = []; // 清空等待隊列
            originalRequest.headers["Authorization"] = `Bearer ${token}`;
            return this.authAxios(originalRequest); // 使用新的 token 重試請求
          } catch (error) {
            return Promise.reject(error);
          } finally {
            this.isRefreshing = false; // 刷新完成
          }
        }
        return Promise.reject(error); // 其他錯誤直接返回
      },
    );
  }

  private setupAuthHeaders(token: string): void {
    this.authAxios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }

  /**
   * 獲取 AuthService 的單例實例。
   */
  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  /**
   * 執行登入操作並獲取存取令牌。
   */
  public async login(): Promise<string> {
    try {
      const response = await this.authAxios.post<LoginResponse>(
        "/api/v1/auth/login",
        {
          username: import.meta.env.VITE_API_USERNAME, // 從環境變數獲取使用者名稱
          password: import.meta.env.VITE_API_PASSWORD, // 從環境變數獲取密碼
        },
      );

      const { access_token } = response.data;
      localStorage.setItem("access_token", access_token); // 將存取令牌存入 localStorage
      this.setupAuthHeaders(access_token); // 設定 authAxios 的 Authorization 標頭

      return access_token; // 返回存取令牌
    } catch (error) {
      console.error("Login failed:", error); // 登入失敗時記錄錯誤
      throw error;
    }
  }

  /**
   * 確保使用者已驗證身份。
   * 如果沒有存取令牌，則執行登入操作。
   */
  public async ensureAuthenticated(): Promise<string> {
    const token = localStorage.getItem("access_token"); // 從 localStorage 獲取存取令牌
    if (!token) {
      return this.login(); // 如果沒有令牌，執行登入
    }
    this.setupAuthHeaders(token); // 設定 authAxios 的 Authorization 標頭
    return token; // 返回存取令牌
  }

  /**
   * 獲取目前的存取令牌。
   */
  public getToken(): string | null {
    return localStorage.getItem("access_token"); // 從 localStorage 獲取存取令牌
  }

  /**
   * 取得已配置的 axios 實例
   */
  public getAuthAxios() {
    return this.authAxios;
  }
}

// 匯出 AuthService 實例與配置好的 axios 實例
export const authService = AuthService.getInstance();
export const authAxios = authService.getAuthAxios();
