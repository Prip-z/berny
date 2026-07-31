"use client";

import { useSocketState } from "@/src/shared/api/socket/store";

export default function ConnectionBanner() {
  const status = useSocketState((state) => state.status);

  if (status === "connecting") {
    return (
      <div className="bg-yellow-500 py-1.5 text-center text-xs font-medium animate-pulse">
        ПОДКЛЮЧЕНИЕ
      </div>
    );
  }

  if (status === "offline") {
    return (
      <div className="bg-red-500 py-1.5 text-center text-xs font-medium text-white">
        ОФФЛАЙН
      </div>
    );
  }

  return null;
}