import { ContactListInput } from "@/src/shared/ui/input";
import { useState } from "react";
import {useQuery} from "@tanstack/react-query"
import { channel } from "diagnostics_channel";

interface SearchContactFormProps {
    text: string
    onSearchChange: (text: string) => void
}

export function SearchContactForm({text, onSearchChange}: SearchContactFormProps) {




    const handleSearchContact = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
    }



    return (
        <div>
            <form onSubmit={handleSearchContact}>
                <ContactListInput value={text} onChange={onSearchChange} placeholder="Поиск"/>
            </form>
        </div>
        
    )
}