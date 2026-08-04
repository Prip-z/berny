"use client";
import { useEffect } from "react";
import { useChatStore } from "@/src/features/chat/send-message/model/store";
import MessageBubble, { MessageSchema, MessageType } from "@/src/entities/message";
import SendMessageForm from "@/src/features/chat/send-message/ui";
import { socketSubscribe } from "@/src/shared/api/socket";
import ConnectionBanner from "@/src/features/connection_status/ui";
import { UserPresence } from "@/src/entities/user";
import { TypingIndicator } from "@/src/features/chat/typing-indicator/ui";
import { useChannelsStore } from "@/src/entities/chat/model/store";

export function ChatWindow() {
  const messageArray = useChatStore((state) => state.messageArray);
  const receiveMessage = useChatStore((state) => state.receiveMessage)
  const activeChannelId = useChannelsStore((state) => state.activeChannelId)
  const setMessages = useChatStore((state) => state.setMessages)
  useEffect(() => {
    const addMessageUnsubscribe = socketSubscribe("NEW_MESSAGE", (rawPayload: unknown) => {
      const parsed = MessageSchema.safeParse(rawPayload)
      if (!parsed.success) {
        console.error("Invalid TYPING payload:", parsed.error.format());
        return;
      }

      const payload = parsed.data; 

      receiveMessage(payload)
    });
    if (activeChannelId == null) {
      setMessages([])
    }
    else {
      async function loadData(){
        const token = localStorage.getItem('accessToken')
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/messaging/channels/${activeChannelId}/messages`, {
          headers: {
                Authorization: `Bearer ${token}`
            }
          })
        const rawData = await response.json()

        const formattedMessages = rawData.map((msg: any) => ({
            id: String(msg.message_id),
            senderId: msg.sender_id,
            text: msg.text, 
            timestamp: new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            status: "sent"
        }))
        setMessages(formattedMessages)
      }
      loadData()
    }
    return () => {
      addMessageUnsubscribe();
    };
    
  }, [activeChannelId]);

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

