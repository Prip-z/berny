"use client";

import { useSocketState } from "@/src/shared/api/socket/store";

export function ConnectionBanner() {
  const status = useSocketState((state) => state.status);

  if (status === "connecting") {
    return (
      // <div className="bg-yellow-500 py-1.5 text-center text-xs font-medium animate-pulse">
      //   ПОДКЛЮЧЕНИЕ
      // </div>
      null
    );
  }

  if (status === "offline") {
    return (
      // <div className="bg-red-500 py-1.5 text-center text-xs font-medium text-white">
      //   ОФФЛАЙН
      // </div>
      null
    );
  }

  return null;
}