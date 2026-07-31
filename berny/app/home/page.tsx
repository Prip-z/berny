"use client"
import HomePage from "@/src/_pages/home";
import { SocketProvider } from "@/src/features/connection";

export default function Home() {
    return <div>
        <HomePage />
        <SocketProvider />
    </div>
}