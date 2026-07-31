import { ChatBox } from "@/src/entities/chat/ui/ChatBox";
import { SearchContactForm } from "@/src/features/contack-list/search-contact";

export function ContactList() {
    


    return (
    <div className="w-170 flex-col h-full border-r border-black">
        <div className=" border-b border-black py-5 px-5">
            <SearchContactForm />
        </div>
        <div className="flex flex-1 overflow-y-auto">
            <ChatBox name="Имя" lastMessage="Ал1"/>
        </div>
    </div>
    )
    
}