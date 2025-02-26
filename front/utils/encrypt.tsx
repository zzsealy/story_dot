import CryptoJS from "crypto-js";

const ENCRYPTION_KEY = `${process.env.NEXT_PUBLIC_ENCRYPTION_KEY}`; // 从环境变量中获取密钥

export function encryptData(data: any) {
  // 将 Base64 密钥转换为 WordArray（crypto-js 需要的格式）
  const key = CryptoJS.enc.Base64.parse(ENCRYPTION_KEY);
    const encrypted = CryptoJS.AES.encrypt(JSON.stringify(data), key, {
    mode: CryptoJS.mode.ECB, // 使用 ECB 模式
    padding: CryptoJS.pad.Pkcs7, // 使用 PKCS7 填充
  });
  return encrypted.toString();
}

