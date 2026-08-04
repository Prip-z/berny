import { connectSocket } from "@/src/shared/api/socket"
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
        const token = localStorage.getItem('accessToken')
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/channels/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        const data = await response.json()
        set({ channels: data })
    },
    setActiveChannelId: (id) => {
        set({ activeChannelId: id })
        connectSocket()
    }
}))