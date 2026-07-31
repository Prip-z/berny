"use client";

import {InputMessage} from "@/src/shared/ui/input";
import { FormButton } from "@/src/shared/ui/button";
import { useState } from "react";
import { useChatStore } from "../model/store";

export default function SendMessageForm() {
  const [text, setText] = useState("");
  //МОК
  const currentUserId = "user_123";
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

