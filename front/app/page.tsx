// app/page.tsx
'use client';
export default function HomePage() {
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