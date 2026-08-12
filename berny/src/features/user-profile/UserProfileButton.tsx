import { useChannelsStore } from "@/src/entities"
import { ChatBox } from "@/src/entities/chat/ui/ChatBox"
import { useChannelInfoStore } from "@/src/features/chat/model/store"
import { Fetch } from "@/src/shared/api/http"
import { Dialog } from "@/src/shared/ui/dialog/Dialog"
import { Lupa } from "@/src/shared/ui/icons/lupa"
import { useQuery } from "@tanstack/react-query"
import { UUID } from "crypto"
import { useEffect, useState } from "react"

const searchChannels = async (searchQuery: string) => {
    if (!searchQuery.trim()) return []
    const response = await Fetch(`/channels/search?search_query=${encodeURIComponent(searchQuery)}`)
    if (!response.ok) { throw new Error('SearchError') }
    return response.json()
}


export function UserProfileButton() {
    const username = useChannelInfoStore((state) => state.name)
    const activeChannelId = useChannelsStore((state) => state.activeChannelId)

    const [profileIsOpen, setProfileIsOpen] = useState(false)
    const [addMembersIsOpen, setAddMembersIsOpen] = useState(false)

    const [text, setText] = useState("")
    const [debouncedQuery, setDebouncedQuery] = useState("")

    const { data: searchResults = [], isLoading, error } = useQuery({
        queryKey: ['channelsSearch', debouncedQuery],
        queryFn: () => searchChannels(debouncedQuery),
        enabled: debouncedQuery.trim().length > 0,
    })

    const openAddMembersDialog = () => {
        setAddMembersIsOpen(true)
    }

    const addMembersHandler = async (target_user_id: string) => {
        const response = await Fetch(`/channels/${activeChannelId}/members`, {
            method: "POST",
            body: JSON.stringify({          
                "added_user_id": target_user_id,
                "role": "reader"
            })
        })
        const result = await response.json()
    }

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedQuery(text)
        }, 300)

        return () => clearTimeout(timer)
    }, [text])

    return (
        <>
            <button
                className="flex flex-row w-full h-13 bg-userprofile-button justify-start items-center gap-2 px-5 cursor-pointer"
                onClick={() => setProfileIsOpen(true)}
            >
                {username}
            </button>
            <Dialog
                isOpen={profileIsOpen}
                onClose={() => setProfileIsOpen(false)}
                className="w-100 h-400 bg-input-authorize fixed inset-0 m-auto rounded-2xl"
            >
                <div className="flex flex-col items-center justify-start p-2 gap-2 text-white">
                    <div className="w-12 h-12 rounded-full bg-blue-500"></div>
                    {username}
                    <button
                        className='hover:bg-neutral-700 transition p-2 w-full'
                        onClick={openAddMembersDialog}
                    >
                        Добавить участника
                    </button>
                </div>
            </Dialog>
            <Dialog className="w-100 h-400 bg-input-authorize fixed inset-0 m-auto rounded-2xl" isOpen={addMembersIsOpen} onClose={() => setAddMembersIsOpen(false)}>
                <h2 className="text-white pl-7 pt-3 text-xl">Добавить участников</h2>
                <div className="flex w-full border-b-2 border-white flex-row justify-center pt-5 pl-8 pr-3 gap-3 pb-3">
                    <Lupa/>
                    <input className=" text-white w-full focus:outline-none" value={text} onChange={(e) => setText(e.target.value)} placeholder="Поиск"/>
                </div>
                {text.trim().length > 0 ? (
                    searchResults.map((item: any) => (
                        <ChatBox
                            key={item.target_user_id}
                            name={item.title}
                            onClick={() => addMembersHandler(item.target_user_id)}
                        />
                    ))
                ) : null}
            </Dialog>
        </>
    )
}