import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { useUserAuthStore } from "../stores/userAuthStore";

const baseURL =
  process.env.NODE_ENV === 'production'
    ? "https://cassandra-o5ft.onrender.com" // Production base URL
    : "http://localhost:8000"; // Development base URL

export const defaultAxiosInstance = axios.create({
  baseURL,

});

export const axiosInstance = axios.create({
  baseURL,

});


// request interceptor
axiosInstance.interceptors.request.use(
  async (config) => {
    const userAuthStore = useUserAuthStore();
    const oldAuthTokens = userAuthStore.authTokens;

    if (oldAuthTokens && oldAuthTokens.access) {
      const currentTimestamp = Date.now() + 30000;
      let tokenExpTimestamp: any = jwtDecode(oldAuthTokens.access);

      if (tokenExpTimestamp && tokenExpTimestamp['exp']) {
        tokenExpTimestamp = tokenExpTimestamp.exp * 1000;
      }

      if (currentTimestamp >= tokenExpTimestamp) {
        await userAuthStore.UpdateToken()
        .then(Response =>{
          const newAuthTokens:any = userAuthStore.authTokens;
          config.headers.Authorization = `Bearer ${newAuthTokens.access}`;
        })
        .catch(e =>{
          return Promise.reject(e);
        })
        
      } else {
        config.headers.Authorization = `Bearer ${oldAuthTokens['access']}`;
      }
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
 

export default axiosInstance;
