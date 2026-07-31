interface FormButtonProps {
    text: string,
    disabled?: boolean,
}

export function FormButton({text, disabled}: FormButtonProps) {
    return (
        <button 
            className="bg-blue-600 
                        hover:bg-blue-700 
                        text-white 
                        font-medium 
                        py-2 
                        px-4 
                        rounded-lg 
                        transition-colors
                        ml-auto
                        " 
            disabled={disabled}
            type="submit"
        >
            {text}
        </button>
    );
}