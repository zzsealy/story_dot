// components/LocaleSwitcher.tsx
"use client"; // 标记为客户端组件

import React from "react";
import { useRouter, usePathname } from "next/navigation"; // 路由相关的 Hook
import { useLocale, useTranslations } from "next-intl"; // next-intl 提供的 Hook

export default function LocaleSwitcher() {
  const router = useRouter();
  const pathname = usePathname(); // 获取当前路径 (不含语言前缀)
  const currentLocale = useLocale(); // 获取当前的语言环境
  const t = useTranslations("LocaleSwitcher"); // 获取语言切换器相关的翻译

  const onLocaleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newLocale = event.target.value;
    // 构建新的 URL，替换掉路径中的语言部分
    // next-intl 会自动处理好 pathnames
    // 比如当前是 /zh-CN/about, pathname 是 /about
    // 切换到 en, 传入 { locale: 'en' }
    router.replace(pathname, { locale: newLocale });
  };

  return (
    <span>
      <label>{t("label")}: </label>
      {/* 使用 select 元素作为示例切换器 */}
      <select value={currentLocale} onChange={onLocaleChange}>
        {/* 遍历支持的语言列表并创建选项 */}
        {/* 注意：这里写死了语言列表，更好的做法是从某个配置或 state 中获取 */}
        {["zh-CN", "en", "fr"].map((locale) => (
          <option key={locale} value={locale}>
            {/* 使用翻译来显示语言的名称，例如 "简体中文", "English" */}
            {t("locale", { locale })}
          </option>
        ))}
      </select>
    </span>
  );
}
