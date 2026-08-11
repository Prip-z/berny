interface InputProps {
    value: string,
    onChange: (val:string) => void,

    placeholder?: string,
}

export function ContactListInput({value, onChange, placeholder}: InputProps) {
    return (
        <input 
        className=" 
            bg-input-search
            text-white
            px-4
            py-2
            rounded-lg
            outline-none
            w-full
        "
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Поиск"
        />
    )
}