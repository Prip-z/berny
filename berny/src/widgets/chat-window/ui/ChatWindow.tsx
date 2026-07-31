"use client";
import { useEffect } from "react";
import { useChatStore } from "@/src/features/chat/send-message/model/store";
import MessageBubble, { MessageSchema, MessageType } from "@/src/entities/message";
import SendMessageForm from "@/src/features/chat/send-message/ui";
import { socketSubscribe } from "@/src/shared/api/socket";
import ConnectionBanner from "@/src/features/connection_status/ui";
import { UserPresence } from "@/src/entities/user";
import { TypingIndicator } from "@/src/features/chat/typing-indicator/ui";

export function ChatWindow() {
  const messageArray = useChatStore((state) => state.messageArray);
  const addMessage = useChatStore((state) => state.addMessage)

  useEffect(() => {

    
    const addMessageUnsubscribe = socketSubscribe("NEW_MESSAGE", (rawPayload: unknown) => {
      const parsed = MessageSchema.safeParse(rawPayload)
      if (!parsed.success) {
        console.error("Invalid TYPING payload:", parsed.error.format());
        return;
      }

      const payload = parsed.data; 

      addMessage(payload.text, payload.senderId);
    });

    return () => {
      addMessageUnsubscribe();
    };
  }, []);

  return (
    <div className="flex flex-col h-full w-full max-4xl mx-auto overflow-auto">
      <ConnectionBanner />
      <UserPresence />
      <TypingIndicator />
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-2">
        {messageArray.map((msg: MessageType) => (
          <MessageBubble
            key={msg.id}
            {...msg}
          />
        ))}
      </div>

      <SendMessageForm></SendMessageForm>
    </div>
  );
}

