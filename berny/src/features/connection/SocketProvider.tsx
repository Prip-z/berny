import { connectSocket, disconnectSocket } from "@/src/shared/api/socket";
import { useEffect } from "react";

export function SocketProvider() {
    useEffect (() => {
        connectSocket()
        return () => {disconnectSocket();}
    }, [])
    return <></>
}