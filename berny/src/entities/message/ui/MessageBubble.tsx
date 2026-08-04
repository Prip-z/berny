import { MessageType } from "../model/types";

export default function MessageBubble({ text, senderId, timestamp, status }: MessageType) {
  const token = localStorage.getItem('accessToken')
  let userId = null
  if (token) {
      const payloadBase64 = token.split('.')[1]
      const decodedPayload = JSON.parse(atob(payloadBase64))
      userId = decodedPayload.user_id
  }
  const isMe = senderId === userId;
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

  return (
    <div className={`flex w-full ${isMe ? "justify-end" : "justify-start"}`}>
      
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
          {statusMessage()} {timestamp} 
        </span>
      </div>

    </div>
  );
}