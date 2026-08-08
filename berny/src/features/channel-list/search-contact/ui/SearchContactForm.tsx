import { ContactListInput } from "@/src/shared/ui/input";
import { useState } from "react";
import {useQuery} from "@tanstack/react-query"
import { channel } from "diagnostics_channel";

interface SearchContactFormProps {
    onFocus: () => void
    onBlur:() => void
    text: string
    onSearchChange: (text: string) => void
}

export function SearchContactForm({onFocus, onBlur, text, onSearchChange}: SearchContactFormProps) {




    const handleSearchContact = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
    }



    return (
        <div>
            <form onSubmit={handleSearchContact}>
                <ContactListInput value={text} onChange={onSearchChange} placeholder="Поиск" onFocus={onFocus} onBlur={onBlur} />
            </form>
        </div>
        
    )
}