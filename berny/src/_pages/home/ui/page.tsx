import { useChannelsStore } from "@/src/entities/chat/model/store";
import { useResizible } from "@/src/shared/lib/resizeHandler/resizeHandler";
import {ChatWindow} from "@/src/widgets";
import { ContactList } from "@/src/widgets";
import { ChatManagment } from "@/src/widgets";
import { useEffect, useState } from "react";

export default function HomePage() {
    const {sidebarWidth, onMouseDownHandler} = useResizible()

    const activeChannelId = useChannelsStore((state) => state.activeChannelId)

    const showChatWindow = () => {
        if (activeChannelId)
        {
            return <ChatWindow />
        }
        else {
            return (
                <div className="flex w-full justify-center flex-1">
                    <div className="flex px-2 py-1 justify-center bg-chat-none font-bold text-l rounded-2xl ">
                        <p>Выберите, кому хотите написать</p>
                    </div>
                    
                </div>
            )
        }
    }

    return <div className="flex flex-1 flex-row items-center justify-center h-screen w-screen overflow-hidden bg-neutral-900">
        <ChatManagment/>
        <ContactList width={sidebarWidth}/>
        <div className="w-0.5 h-screen cursor-col-resize select-none transition duration-100 hover:bg-gray-800" onMouseDown={onMouseDownHandler} >

        </div>
        {showChatWindow()}

    </div>
}