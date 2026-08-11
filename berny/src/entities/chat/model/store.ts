import { Fetch } from "@/src/shared/api/http"
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
        const response = await Fetch("/channels/")
        const data = await response.json()
        set({ channels: data })
    },
    setActiveChannelId: (id) => {
        set({ activeChannelId: id })
    }
}))