// app/[locale]page.tsx
"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import api from "@/utils/axios";
import { backendUrl } from "@/constants/url";
import { useTranslations } from "next-intl";

import StoryContent from "./components/storyContent";
import LeftContent from "./components/leftContent";

export default function HomePage() {
  const router = useRouter();
  const [storyDotList, setStoryDotList] = useState([]); // 储存故事点
  const t = useTranslations("Index");

  const getStoryDots = () => {
    api.get(backendUrl.getUserStoryDotUrl).then((res) => {
      if (res.data.code === 200) {
        setStoryDotList(res.data.story_dot_list);
      } else if (res.data.code == 401) {
        // router.push("/login");
      } else {
        toast("发生错误 请稍后重试");
      }
    });
  };
  useEffect(() => {
    getStoryDots();
  }, []);

  return (
    // <h1>{t('title')}</h1>
    <div className="flex h-screen">
      <div className="w-1/5 bg-gray-200">
        <LeftContent />
      </div>
      <div className="w-3/5 bg-gray-300">
        <StoryContent />
      </div>
      <div className="w-1/5 bg-gray-200">Box 3</div>
    </div>
  );
}
