import axios from "axios";

// let baseURL;

// // If running in the browser → use localhost (your backend exposed to host machine)
// if (typeof window !== "undefined") {
//   baseURL = "http://localhost:8000";
// } else {
//   // If running inside Docker/Next.js server → use backend service name
//   baseURL = "http://backend:8000";
// }
const baseURL = process.env.NEXT_PUBLIC_API_URL;

const api = axios.create({ baseURL });

// Attach JWT from localStorage automatically (browser only)
api.interceptors.request.use(
  (config) => {
    try {
      const token = localStorage.getItem("jwt");
      
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch(err){
        console.warn(
      "⚠️ JWT token not available: make sure to call this in a browser ('use client')."
    );
    }
    return config;
  });

export default api;
