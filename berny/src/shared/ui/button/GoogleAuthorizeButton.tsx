import { GoogleIcon } from "../icons/GoogleIcon"

export function GoogleAuthorizeButton() {
    return (
        <button className="flex text-lg items-center justify-center gap-2 w-full py-3 px-4 bg-white text-black rounded-2xl hover:bg-gray-100 transition-colors">
            <GoogleIcon />
            <span>Войти через Google</span>
        </button>
    );
}