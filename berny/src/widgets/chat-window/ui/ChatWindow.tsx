"use client";
import { useEffect, useRef } from "react";
import { useChatStore } from "@/src/features/chat/send-message/model/store";
import MessageBubble, { MessageSchema, MessageType } from "@/src/entities/message";
import SendMessageForm from "@/src/features/chat/send-message/ui";
import { connectSocket, disconnectSocket, socketSubscribe } from "@/src/shared/api/socket";
import ConnectionBanner from "@/src/features/connection_status/ui";
import { UserPresence } from "@/src/entities/user";
import { TypingIndicator } from "@/src/features/chat/typing-indicator/ui";
import { useChannelsStore } from "@/src/entities/chat/model/store";
import { getAccessToken } from "@/src/shared/lib/storage/auth";
import { Fetch } from "@/src/shared/api/http";
import { is } from "zod/v4/locales";

export function ChatWindow() {
  const messageArray = useChatStore((state) => state.messageArray);
  const receiveMessage = useChatStore((state) => state.receiveMessage)
  const activeChannelId = useChannelsStore((state) => state.activeChannelId)
  const setMessages = useChatStore((state) => state.setMessages)
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (!activeChannelId) {
      setMessages([]);
      return;
    }

    let isCurrent = true;

    connectSocket(activeChannelId);

    const addMessageUnsubscribe = socketSubscribe("NEW_MESSAGE", (rawPayload: unknown) => {
      const parsed = MessageSchema.safeParse(rawPayload);
      if (!parsed.success) {
        console.error("Invalid socket payload:", parsed.error.format());
        return;
      }
      receiveMessage(parsed.data);
    });

    async function loadData() {
      try {
        const response = await Fetch(`/messaging/channels/${activeChannelId}/messages`);
        if (!response.ok) return;

        const result = await response.json();

        if (!isCurrent) return;

        const formattedMessages = result
          .map((msg: any) => ({
            message_id: String(msg.message_id),
            sender_id: msg.sender_id,
            text: msg.text,
            created_at: new Date(msg.created_at).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            }),
            status: "sent",
          }))
          .reverse();

        setMessages(formattedMessages);
      } catch (error) {
        console.error("Failed to fetch messages:", error);
      }
    }

    loadData();
    return () => {
      isCurrent = false;
      addMessageUnsubscribe();
      disconnectSocket();
    };
  }, [activeChannelId, receiveMessage, setMessages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messageArray])

  return (
    <div className="flex flex-col h-full w-full flex-1 min-w-0 overflow-auto">
      <ConnectionBanner />
      <UserPresence />
      <TypingIndicator />
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-2">
        {messageArray.map((msg: MessageType) => (
          <MessageBubble
            key={msg.message_id}
            {...msg}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <SendMessageForm></SendMessageForm>
    </div>
  );
}

