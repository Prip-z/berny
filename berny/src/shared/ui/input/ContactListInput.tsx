interface InputProps {
    value: string,
    onChange: (val:string) => void,
    onFocus: () => void,
    onBlur: () => void,
    placeholder?: string,
}

export function ContactListInput({value, onChange, placeholder, onFocus, onBlur}: InputProps) {
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
        onFocus={onFocus}
        onBlur={onBlur}
        placeholder="Поиск"
        />
    )
}