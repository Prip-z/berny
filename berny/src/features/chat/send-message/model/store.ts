import { create } from "zustand";
import { MessageType } from "@/src/entities";
import { sendSocketMessage } from "@/src/shared";

interface ChatState {
  messageArray: Array<MessageType>
  addMessage: (text: string, senderid: string) => void
  setMessages: (messages: MessageType[]) => void
  receiveMessage: (message: MessageType) => void
}

export const useChatStore = create<ChatState>((set) => ({
  messageArray: [],

  addMessage: (text: string, senderId: string) => {
    const messageUuid: string = crypto.randomUUID();
    const currentTime: string = new Date().toLocaleTimeString("ru-RU", {
      hour: "2-digit",
      minute: "2-digit",
    });
    const newStatus = "departing"

    const currentMessage: MessageType = {
      message_id: messageUuid,
      sender_id: senderId,
      text: text,
      created_at: currentTime,
      status: newStatus,
    };

    sendSocketMessage("NEW_MESSAGE", { text, senderId })
    set((state) => ({
      messageArray: [...state.messageArray, currentMessage],
    }));
  },

  setMessages: (messages) => {
      set({ messageArray: [...messages] })
  },

  receiveMessage: (message) => {
      set((state) => {
          const hasDeparting = state.messageArray.some(
              (m) => m.status === 'departing' && m.text === message.text
          )

          if (hasDeparting) {
              return {
                  messageArray: state.messageArray.map((m) =>
                      m.status === 'departing' && m.text === message.text
                          ? { ...message, status: 'sent' }
                          : m
                  ),
              }
          }

          return {
              messageArray: [...state.messageArray, message],
          }
      })
  }
}));
