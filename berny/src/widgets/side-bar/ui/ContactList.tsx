import { useChannelInfoStore } from "@/src/features/chat/model/store";
import { useChannelsStore } from "@/src/entities/chat/model/store";
import { ChatBox } from "@/src/entities/chat/ui/ChatBox";
import { SearchContactForm } from "@/src/features";
import { Fetch } from "@/src/shared/api/http";
import { getAccessToken } from "@/src/shared/lib/storage/auth";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

const searchChannels = async (searchQuery: string) => {
    if (!searchQuery.trim()) return []
    const response = await Fetch(`/channels/search?search_query=${encodeURIComponent(searchQuery)}`)
    if (!response.ok) { throw new Error('SearchError') }
    return response.json()
}

interface ContactListProps {
    width: number
}

export function ContactList({width}: ContactListProps) {
    const userChannels = useChannelsStore((state) => state.channels)
    const fetchChannels = useChannelsStore((state) => state.fetchChannels)
    const setActiveChannelId = useChannelsStore((state) => state.setActiveChannelId)

    const setName = useChannelInfoStore((state) => state.setName)


    const [text, setText] = useState("")
    const [debouncedQuery, setDebouncedQuery] = useState("")

    const { data: searchResults = [], isLoading, error } = useQuery({
        queryKey: ['channelsSearch', debouncedQuery],
        queryFn: () => searchChannels(debouncedQuery),
        enabled: debouncedQuery.trim().length > 0,
    })

    useEffect(() => {
        fetchChannels()

    }, [fetchChannels])

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedQuery(text)
        }, 300)

        return () => clearTimeout(timer)
    }, [text])


    const handlePushSearchResult = async (target_user_search_query: string) => {
        let response = await Fetch(`/channels/direct/${target_user_search_query}`)

        if (response.status == 404) {
            response = await Fetch(`/channels/direct/${target_user_search_query}`)
            const result = await response.json()
            setActiveChannelId(result.channel_id)
            setName(result.name)
        }
        
        else {
            const result = await response.json()
            setActiveChannelId(result.channel_id)
            setName(result.name)
        }
    }

    return (
        <div className="shrink-0 flex-col h-screen bg-chat-list" style={{width: `${width}px` }}>
            <div className="flex flex-col flex-1 overflow-y-auto gap-5">
                
                <SearchContactForm
                    text={text}
                    onSearchChange={setText}
                />
                {text.trim().length > 0 ? (
                    searchResults.map((item: any) => (
                        <ChatBox
                            key={item.target_user_id}
                            name={item.title}
                            onClick={() => handlePushSearchResult(item.target_user_id)}
                        />
                    ))
                ) : (
                    userChannels.map((channel) => (
                        <ChatBox
                            key={channel.channel_id}
                            name={channel.name}
                            lastMessage={channel.last_message_text}
                            onClick={() => {
                                setActiveChannelId(channel.channel_id)
                                setName(channel.name)
                            }}
                        />
                    ))
                )}
            </div>
        </div>
    )

}