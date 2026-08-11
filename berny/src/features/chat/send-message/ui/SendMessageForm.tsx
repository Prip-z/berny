"use client";

import {InputMessage} from "@/src/shared/ui/input";
import { FormButton } from "@/src/shared/ui/button";
import { useEffect, useState } from "react";
import { useChatStore } from "../model/store";
import { getAccessToken } from "@/src/shared/lib/storage/auth";

export default function SendMessageForm() {
  const [text, setText] = useState("");
  const [currentUserId, setCurrentUserId] = useState(() => {
    if (typeof window === "undefined") return ""
    const token = getAccessToken()
    if (!token) return ""
    try {
        const payloadBase64 = token.split('.')[1]
        const decodedPayload = JSON.parse(atob(payloadBase64))
        return decodedPayload.sub || ""
    } catch {
        return ""
    }
})

  const addMessage = useChatStore((state) => state.addMessage);

  const handleSendMessage = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (text.trim() === "") return;
    addMessage(text, currentUserId);
    setText("");
  };

  return (
    <form className="flex flex-row w-full gap-2 p-4" onSubmit={handleSendMessage}>
      <InputMessage
        value={text}
        onChange={setText}
        placeholder="Сообщение"
      />
      <FormButton 
        text="Отправить"
      />
    </form>
  )
}

