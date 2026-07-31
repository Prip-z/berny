import {ChatWindow} from "@/src/widgets/chat-window/ui";
import { ContactList } from "@/src/widgets/side-bar/ui";

export default function HomePage() {
    return <div className="flex flex-row items-center justify-center h-screen bg-neutral-900">
        <ContactList/>
        <ChatWindow/>

    </div>
}