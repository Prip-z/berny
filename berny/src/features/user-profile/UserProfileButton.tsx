import { useChannelInfoStore } from "@/src/features/chat/model/store"

export function UserProfileButton() {
    const username = useChannelInfoStore((state) => state.name)
    return (
        <button 
        className="flex flex-row w-full h-13 bg-userprofile-button justify-start items-center gap-2 px-5"
        >
            {username}
        </button>
    )
}