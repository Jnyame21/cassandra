import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useUserAuthStore } from "../stores/userAuthStore";

const baseURL = process.env.NODE_ENV === 'production'
  ? "https://cassandra-o5ft.onrender.com" // Production base URL
  : "http://localhost:8000"; // Development base URL

export const defaultAxiosInstance = axios.create({
  baseURL,
  withCredentials: true,
});

export const axiosInstance = axios.create({
  baseURL,
  withCredentials: true,
});


// request interceptor
axiosInstance.interceptors.request.use(
  async (config) => {
    const userAuthStore = useUserAuthStore();
    const accessToken = userAuthStore.accessToken;

    if (accessToken) {
      const bufferTime = 120000
      const currentTimestamp = Date.now()
      let tokenExpTimestamp = jwtDecode(accessToken).exp || 0
      tokenExpTimestamp = tokenExpTimestamp * 1000;

      if ((currentTimestamp + bufferTime) >= tokenExpTimestamp) {
        
        try {
          await userAuthStore.UpdateToken()
          config.headers.Authorization = `Bearer ${userAuthStore.accessToken}`;
        }
        catch (e) {
          return Promise.reject(e);
        }
      } 
      else {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


export default axiosInstance;
