import { useChannelsStore } from "@/src/entities/chat/model/store";
import { ChatBox } from "@/src/entities/chat/ui/ChatBox";
import { SearchContactForm } from "@/src/features/channel-list/search-contact";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

const searchChannels = async (searchQuery: string) => {
    if (!searchQuery.trim()) return []
    const token = localStorage.getItem('accessToken')
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/channels/search?search_query=${encodeURIComponent(searchQuery)}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    if (!res.ok) { throw new Error('SearchError') }
    return res.json()
}


export function ContactList() {
    const userChannels = useChannelsStore((state) => state.channels)

    const fetchChannels = useChannelsStore((state) => state.fetchChannels)
    const setActiveChannelId = useChannelsStore((state) => state.setActiveChannelId)
    const [text, setText] = useState("")
    const [debouncedQuery, setDebouncedQuery] = useState("")
    const [showSearch, setShowSearch] = useState(false)

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

    const onFocus = () => {
        setShowSearch(true)
        console.log(showSearch)
    }

    const onBlur = () => {
        setShowSearch(false)
        console.log(showSearch)
    }

    const handlePushSearchResult = async (target_user_search_query: string) => {
        const token = localStorage.getItem('accessToken')
    
        try {
            let response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/channels/direct/${target_user_search_query}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })               
            if (response.status == 404) {
                response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/channels/direct/${target_user_search_query}`, {
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
        <div className="w-170 flex-col h-full border-r border-black bg-chat-list px-5 py-5">
            <div className="flex flex-col flex-1 overflow-y-auto">
                <SearchContactForm
                    text={text}
                    onSearchChange={setText}
                    onFocus={onFocus}
                    onBlur={onBlur}
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