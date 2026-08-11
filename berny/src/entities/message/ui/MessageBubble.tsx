"use client"
import { getAccessToken } from "@/src/shared/lib/storage/auth";
import { MessageType } from "../model/types";
import { getCurrentUser, getTimeOnMessage } from "@/src/shared";

export function MessageBubble({ text, sender_id, created_at, status }: MessageType) {
  let user_id = getCurrentUser()
  
  const isMe = sender_id === user_id;

  const statusMessage = () => {
    if (status == "departing") {
      return (
        <span >
          ✓
        </span>
      )
    }
    else if (status == "read") {
      return (
        <span className="text-gray-100">
          ✓✓
        </span>
      )
    }
    else if (status == "sent") {
      return (
        <span>
          ✓✓
        </span>
      )
    }
  }
  
  const timeOnMessage = getTimeOnMessage(created_at)

  return (
    <div className={`flex w-full animate-bubble-appear ${isMe ? "justify-end" : "justify-start"}`}>
      
      <div
        className={`max-w-[70%] rounded-2xl px-4 py-2 flex flex-col gap-1 text-sm shadow-sm
          ${isMe 
            ? "bg-blue-600 text-white rounded-tr-none" 
            : "bg-gray-100 text-gray-900 rounded-tl-none" 
          }`}
      >
        <p className="break-all text-[20px]">
          {text} 
        </p>
        <span 
          className={`text-[15px] self-end 
            ${isMe ? "text-blue-200" : "text-gray-400"}`} 
        >
          {statusMessage()} {timeOnMessage} 
        </span>
      </div>

    </div>
  );
}