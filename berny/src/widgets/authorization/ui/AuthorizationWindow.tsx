"use client";

import { Fetch } from "@/src/shared/api/http";
import { setTokens } from "@/src/shared/lib/storage/auth";
import { FormButton, GoogleAuthorizeButton } from "@/src/shared";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

interface AuthorizationWindowProps {
    onSwitchToRegister: () => void;
}


export function AuthorizationWindow({onSwitchToRegister}: AuthorizationWindowProps) {
    const [textEmail, setEmail] = useState("");
    const [textPassword, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("")
    const router = useRouter();

    const handleAuthorize = async (e: React.FormEvent<HTMLFormElement>) => {
        setErrorMessage("")
        e.preventDefault()
        if ((textEmail.trim() === "") || (textPassword.trim() === "") ) return;
        try {
            const response = await Fetch(`/identify/api/v1/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: textEmail,
                    password: textPassword,
                }),
            })

            if (response.status == 404) {
                setErrorMessage("Введен неверный логин или пароль")
                return
            }
            
            const data = await response.json()
            
            setTokens(data)

            router.push("/home");

            setEmail("");
            setPassword("")
        }
        catch (error){
            console.error("Network or execution error:", error)
        }
        
    };

    return (
        <div className="flex flex-col flex-1 gap-7 px-16.25 pt-12.5">
            <div className="flex items-center justify-center">
                <h1 className="font-bold text-4xl">Вход в Berny</h1>
            </div>
            <div className="flex items-center justify-center">
                <GoogleAuthorizeButton />
            </div>
            <div className="flex items-center justify-center">
                ------------------ или ------------------
            </div>

            <div>
                {errorMessage ? <span>{errorMessage}</span> : null}
            </div>
            <form className="flex flex-col gap-10" onSubmit={handleAuthorize}>
                <div className="flex flex-col items-left justify-center gap-3">
                    <span>Email</span>
                    <input className="bg-input-authorize rounded-lg w-full px-4 h-12" 
                            value={textEmail}
                            onChange={(e) => setEmail(e.target.value)}>

                    </input>
                </div>
                <div className="flex flex-col items-left justify-center gap-3">
                    <span>Password</span>
                    <input className="bg-input-authorize rounded-lg  w-full px-4 h-12"
                            value={textPassword}
                            type="password"
                            onChange={(e) => setPassword(e.target.value)}>

                    </input>
                </div>
                
                <div className="flex items-center justify-center w-full">
                    <FormButton text="Войти"/>
                </div>
            </form>

            <div className="flex flex-row items-center justify-center">
                <span>Нет аккаунта?&nbsp;</span>
                <button 
                    type="button" 
                    onClick={onSwitchToRegister} 
                    className="text-blue-500 hover:underline cursor-pointer"
                >
                    Зарегистрироваться
                </button>
            </div>

        </div>
    )
}