import axios from 'axios'

import { encryptData } from './encrypt';

// 创建一个axios实例
const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    timeout: 5000,
});

//请求拦截器
api.interceptors.request.use(
  (config) => {
  const allowedMethods = ['post', 'put', 'delete', 'patch'];
  if (config.method && allowedMethods.includes(config.method) && config.data) {
    // 对请求数据进行加密
    config.data = { data: encryptData(config.data) };
  }
  const token = typeof window !== "undefined" ? window.localStorage.getItem('story_dot_token') : null;
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
  },
  (error) => {
  return Promise.reject(error);
  }
)

export default api