import { AuthorizationWindow, RegistrationWindow } from "@/src/widgets";
import { useState } from "react";



export function Authorization() {
    const [mode, setMode] = useState<"login" | "register">("login");
    return (
        <div className="bg-main flex flex-1 flex-row">
            <div className="flex-2 bg-cover bg-center"     style={{ backgroundImage: "url('windows-blue-gradient-1920x1080-v0-rzyccf9ixmrd1.png')" }}>

            </div>
            <div className="flex flex-col bg-card flex-1 px-10 py-30">
                {mode === "login" ? (
                    <AuthorizationWindow onSwitchToRegister={() => setMode("register")} />
                ) : (
                    <RegistrationWindow onSwitchToLogin={() => setMode("login")} />
                )}
            </div>

        </div>
    )
}