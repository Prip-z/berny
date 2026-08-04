import { useChannelsStore } from "@/src/entities/chat/model/store";
import { ChatBox } from "@/src/entities/chat/ui/ChatBox";
import { SearchContactForm } from "@/src/features/channel-list/search-contact";
import { useEffect } from "react";

export function ContactList() {
    const channels = useChannelsStore((state) => state.channels)
    const fetchChannels = useChannelsStore((state) => state.fetchChannels)
    const setActiveChannelId = useChannelsStore((state) => state.setActiveChannelId)
    
    useEffect(() => {
        fetchChannels()
    }, [fetchChannels])

    return (
    <div className="w-170 flex-col h-full border-r border-black">
        <div className=" border-b border-black py-5 px-5">
            <SearchContactForm />
        </div>
        <div className="flex flex-col flex-1 overflow-y-auto">
            {
                channels.map((channel) => (
                    <ChatBox 
                        key={channel.channel_id}
                        name={channel.name}
                        lastMessage={channel.last_message_text}
                        onClick={() => setActiveChannelId(channel.channel_id)}
                    />
                ))
            }
        </div>
    </div>
    )
    
}