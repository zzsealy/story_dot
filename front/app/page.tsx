// app/page.tsx
'use client';
import { useState, useEffect } from "react";
import { useRouter } from 'next/navigation'
import { toast } from 'sonner';
import api from "@/utils/axios";
import { backendUrl } from "@/constants/url";

export default function HomePage() {
  const router = useRouter()
  const [storyDotList, setStoryDotList] = useState([]); // 储存故事点

  const getStoryDots = () => {
      api.get(backendUrl.getUserStoryDotUrl)
      .then((res) => {
        if(res.data.status_code === 200){
          setStoryDotList(res.data.story_dot_list)
        } else if(res.data.status_code == 401){
          router.push('/login')
        } else {
          toast('发生错误 请稍后重试')
        }
      })
  }
  useEffect(() => {
    getStoryDots();
    },[]);

  return (
    <div className="flex h-screen">
      <div className="w-1/5 bg-gray-200">
        Box 1
      </div>
      <div className="w-3/5 bg-gray-300">
        Box 2
      </div>
      <div className="w-1/5 bg-gray-200">
        Box 3
      </div>
    </div>
  );
}