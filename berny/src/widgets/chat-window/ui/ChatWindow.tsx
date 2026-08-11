"use client";
import { Fragment, useEffect, useRef } from "react";
import { useChatStore } from "@/src/features/chat/send-message/model/store";
import MessageBubble, { MessageSchema, MessageType } from "@/src/entities/message";
import SendMessageForm from "@/src/features/chat/send-message/ui";
import { connectSocket, disconnectSocket, socketSubscribe } from "@/src/shared/api/socket";
import ConnectionBanner from "@/src/features/connection_status/ui";
import { UserPresence } from "@/src/entities/user";
import { TypingIndicator } from "@/src/features/chat/typing-indicator/ui";
import { useChannelsStore } from "@/src/entities/chat/model/store";
import { Fetch } from "@/src/shared/api/http";
import { UserProfileButton } from "@/src/features/user-profile/UserProfileButton";
import { useChannelInfoStore } from "@/src/_pages/home/model/store";

export function ChatWindow() {
  const messageArray = useChatStore((state) => state.messageArray);
  const receiveMessage = useChatStore((state) => state.receiveMessage);
  const activeChannelId = useChannelsStore((state) => state.activeChannelId);
  const setMessages = useChatStore((state) => state.setMessages);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

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
          .map((msg: any) => {
            const rawDate = String(msg.created_at);
            const utcDateString = rawDate.endsWith("Z") ? rawDate : `${rawDate}Z`;

            return {
              message_id: String(msg.message_id),
              sender_id: msg.sender_id,
              text: msg.text,
              created_at: utcDateString,
              status: "sent",
            };
          })
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
  }, [activeChannelId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messageArray]);

  const formatDateHelper = (isoString: string) => {
    const messageDate = new Date(isoString);
    if (isNaN(messageDate.getTime())) return "";

    const today = new Date();
    const targetDate = new Date(messageDate);

    targetDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    const diffDays = Math.round((today.getTime() - targetDate.getTime()) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Сегодня";
    if (diffDays === 1) return "Вчера";

    const options: Intl.DateTimeFormatOptions = { day: "numeric", month: "long" };
    if (targetDate.getFullYear() !== today.getFullYear()) {
      options.year = "numeric";
    }

    return targetDate.toLocaleDateString("ru-RU", options);
  };

  const getFormattedTime = (isoString: string) => {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return isoString;
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  return (
    <div className="flex flex-col h-screen w-full flex-1 min-w-0 min-h-0 overflow-hidden">
      <UserProfileButton/>
      <ConnectionBanner />
      <UserPresence />
      <TypingIndicator />
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-2">
        {messageArray.map((msg: MessageType, index: number) => {
          const currentParsed = new Date(msg.created_at);
          const currentDateStr = !isNaN(currentParsed.getTime())
            ? currentParsed.toDateString()
            : msg.created_at;

          const prevMsg = index > 0 ? messageArray[index - 1] : null;
          const prevParsed = prevMsg ? new Date(prevMsg.created_at) : null;
          const prevDateStr = prevParsed && !isNaN(prevParsed.getTime())
            ? prevParsed.toDateString()
            : null;

          const showDateDivider = index === 0 || currentDateStr !== prevDateStr;

          return (
            <Fragment key={msg.message_id}>
              {showDateDivider && (
                <div className="text-center my-2 text-xs text-gray-400 font-medium">
                  {formatDateHelper(msg.created_at)}
                </div>
              )}
              <MessageBubble
                {...msg}
                created_at={getFormattedTime(msg.created_at)}
              />
            </Fragment>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      <SendMessageForm />
    </div>
  );
}