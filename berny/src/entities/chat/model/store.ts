import { Fetch } from "@/src/shared/api/http"
import { connectSocket, disconnectSocket } from "@/src/shared/api/socket"
import { getAccessToken } from "@/src/shared/lib/storage/auth"
import { create } from "zustand"

interface ChannelsState {
    channels: any[]
    activeChannelId: string | null
    fetchChannels: () => Promise<void>
    setActiveChannelId: (id: string) => void
}

export const useChannelsStore = create<ChannelsState>((set) => ({
    channels: [],
    activeChannelId: null,
    fetchChannels: async () => {
        const token = getAccessToken()
        const response = await Fetch("/channels/", {
          headers: {
                Authorization: `Bearer ${token}`
            }
          })
        const data = await response.json()
        set({ channels: data })
    },
    setActiveChannelId: (id) => {
        set({ activeChannelId: id })
    }
}))