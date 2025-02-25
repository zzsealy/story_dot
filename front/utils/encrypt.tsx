import CryptoJS from "crypto-js";

const SECRET_KEY = `${process.env.ENCRYPTION_KEY}`; // 从环境变量中获取密钥

export function encryptData(data: any) {
  return CryptoJS.AES.encrypt(JSON.stringify(data), SECRET_KEY).toString();
}

