import { useChannelsStore } from "@/src/entities/chat/model/store";
import {ChatWindow} from "@/src/widgets/chat-window/ui";
import { ContactList } from "@/src/widgets/side-bar/ui";
import { ChatManagment } from "@/src/widgets/side-bar/ui/ChatManagment";

export default function HomePage() {
    const activeChannelId = useChannelsStore((state) => state.activeChannelId)
    const showChatWindow = () => {
        if (activeChannelId)
        {
            return <ChatWindow />
        }
        else {
            return (
                <div className="flex w-full justify-center px-75 py-120">
                    <div className="flex w-full h-full justify-center bg-chat-none font-bold text-xl rounded-2xl ">
                        <p>Выберите, кому хотите написать</p>
                    </div>
                    
                </div>
            )
        }
    }
    return <div className="flex flex-row items-center justify-center h-screen bg-neutral-900">
        <ChatManagment/>
        <ContactList/>
        {showChatWindow()}

    </div>
}