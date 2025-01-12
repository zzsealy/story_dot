// app/about/layout.tsx
import React from 'react';

// 这个布局会继承根布局，并且可以覆盖或增加内容
export default function AboutLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      {/* 额外的布局或修改 */}
      <div className="bg-green-500 text-white p-4">
        <h2>关于页面专有布局</h2>
      </div>

      {children}
      {/* 渲染父布局内容（即根布局的内容） */}
    </div>
  );
}