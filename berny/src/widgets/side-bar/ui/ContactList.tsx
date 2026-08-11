import { useChannelsStore } from "@/src/entities/chat/model/store";
import { ChatBox } from "@/src/entities/chat/ui/ChatBox";
import { SearchContactForm } from "@/src/features/channel-list/search-contact";
import { Fetch } from "@/src/shared/api/http";
import { getAccessToken } from "@/src/shared/lib/storage/auth";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

const searchChannels = async (searchQuery: string) => {
    if (!searchQuery.trim()) return []
    const token = getAccessToken()
    const response = await Fetch(`/channels/search?search_query=${encodeURIComponent(searchQuery)}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    if (!response.ok) { throw new Error('SearchError') }
    return response.json()
}


export function ContactList() {
    const userChannels = useChannelsStore((state) => state.channels)

    const fetchChannels = useChannelsStore((state) => state.fetchChannels)
    const setActiveChannelId = useChannelsStore((state) => state.setActiveChannelId)
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
        const token = getAccessToken()

        try {
            let response = await Fetch(`/channels/direct/${target_user_search_query}`, {
            headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            if (response.status == 404) {
                response = await Fetch(`/channels/direct/${target_user_search_query}`, {
                method: "POST",
                headers: {
                        Authorization: `Bearer ${token}`
                    }
                })
                const result = await response.json()
                setActiveChannelId(result.channel_id)
            }
            else {
                const result = await response.json()
                setActiveChannelId(result.channel_id)
            }


        }
        catch {
            console.log("ПИЗДЕЦ")
        }


    }

    return (
        <div className="w-270 flex-col h-full border-r border-black bg-chat-list px-5 py-5">
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
                            onClick={() => setActiveChannelId(channel.channel_id)}
                        />
                    ))
                )}
            </div>
        </div>
    )

}