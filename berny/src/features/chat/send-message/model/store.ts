import { create } from "zustand";
import { MessageType } from "@/src/entities/message";
import { sendSocketMessage } from "@/src/shared/api/socket";

interface ChatState {
  messageArray: Array<MessageType>;
  addMessage: (text: string, senderid: string) => void;
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
      id: messageUuid,
      senderId: senderId,
      text: text,
      timestamp: currentTime,
      status: newStatus,
    };

    sendSocketMessage("NEW_MESSAGE", { text, senderId })
    set((state) => ({
      messageArray: [...state.messageArray, currentMessage],
    }));
  },
}));
