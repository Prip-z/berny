import { create } from "zustand"

interface ChannelInfo {
    name: string
    setName: (username:string) => void
}

export const useChannelInfoStore = create<ChannelInfo>((set) => ({
    name: "",
    setName: (username: string) => {
        set({name: username})
    }
}))