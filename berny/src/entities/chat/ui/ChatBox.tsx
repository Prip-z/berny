interface ChatBoxProps {
    name: string
    lastMessage?: string
    onClick?: () => void
}

export function ChatBox({ name, lastMessage, onClick }: ChatBoxProps) {
    
    return (
        <button type="button" onClick={onClick} className="flex flex-row px-7.5 py-5 gap-5 transition duration-100 hover:bg-chatbox-hover">
            <div className="w-12 h-12 rounded-full bg-blue-500"></div>
            <div className="flex flex-col flex-1">
                <p>{name}</p>
                <p>{lastMessage}</p>
            </div>
        </button>
    )
}