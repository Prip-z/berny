import { create } from "zustand";

interface SocketState {
  status: "offline" | "connecting" | "online",
  attempt: number,

  setStatus : (status: SocketState["status"]) => void,
  incrementAttempt: () => void,
  resetAttempt: () => void,
}

export const useSocketState = create<SocketState>((set) => ({
    status: "offline",
    attempt: 0,

    setStatus(newStatus) {
        set({status: newStatus})
    },

    incrementAttempt() {
        set((state) => ({attempt: state.attempt + 1}))
    },

    resetAttempt() {    
        set({attempt: 0})
    },

}))

