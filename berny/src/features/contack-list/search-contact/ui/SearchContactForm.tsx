import { ContactListInput } from "@/src/shared/ui/input";
import { useState } from "react";


export function SearchContactForm() {
    const [text, setText] = useState("");

    const handleSearchContact = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (text.trim() === "") return;

        setText("")
    }

    return (
        <ContactListInput value={text} onChange={setText} placeholder="Поиск"/>
    )
}