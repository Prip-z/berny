"use client";

import {getCurrentUser, InputMessage} from "@/src/shared";
import { FormButton } from "@/src/shared";
import { useEffect, useState } from "react";
import { useChatStore } from "../model/store";
import { getAccessToken } from "@/src/shared/lib/storage/auth";

export function SendMessageForm() {
  const [text, setText] = useState("");
  const [currentUserId, setCurrentUserId] = useState(() => {
    return getCurrentUser()
})

  const addMessage = useChatStore((state) => state.addMessage);

  const handleSendMessage = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (text.trim() === "") return;
    addMessage(text, currentUserId);
    setText("");
  };

  return (
    <form className="flex flex-row w-full gap-2 p-2 bg-chat-list" onSubmit={handleSendMessage}>
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

