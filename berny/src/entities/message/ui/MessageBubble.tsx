"use client"
import { getAccessToken } from "@/src/shared/lib/storage/auth";
import { MessageType } from "../model/types";

export default function MessageBubble({ text, sender_id, created_at, status }: MessageType) {
  const token = getAccessToken()
  let user_id = null
  if (token) {
      const payloadBase64 = token.split('.')[1]
      const decodedPayload = JSON.parse(atob(payloadBase64))
      user_id = decodedPayload.sub
  }
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
  let timeOnMessage
  const timePattern = /^\d{2}:\d{2}$/;
  if (timePattern.test(created_at)) {
    timeOnMessage = created_at
  }
  else {
    const dateInstance = new Date(created_at)
    const timeOnly = dateInstance.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    timeOnMessage = timeOnly
  }

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