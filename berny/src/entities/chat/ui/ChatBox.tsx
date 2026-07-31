interface ChatBoxProps {
    name: string,
    lastMessage?: string,
}

export function ChatBox({name, lastMessage}: ChatBoxProps) {
    return (
        <button className="flex flex-row px-7.5 py-5 gap-5 ">
            <div className="w-12 h-12 rounded-full bg-blue-500"></div>
            <div className="flex flex-col flex-1">
                <p>{name}</p>
                <p>{lastMessage}</p>
            </div>
        </button>
    )
}