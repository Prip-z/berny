"use client";


import { getBackoffTime } from "../../";
import { getAccessToken } from "../../lib/storage/auth";
import { socketEmit } from "./emitter";
import { useSocketState } from "./store";

let socket: WebSocket | null = null;
let reconnectTimer: number | undefined;

export function connectSocket(activeChannelId: string) {
    if (!activeChannelId) return
    if (socket) {
        socket.close()
    }
    const WEBSOCKET_ADDRESS = `${process.env.NEXT_PUBLIC_WEBSOCKET_URL}/ws/${activeChannelId}`
    const { setStatus, resetAttempt, incrementAttempt } = useSocketState.getState();
    setStatus("connecting")

    const token = getAccessToken()
    const protocols = token ? [token] : []
    
    socket = new WebSocket(WEBSOCKET_ADDRESS, protocols)

    socket.onopen = () => {
        resetAttempt()
        setStatus("online")
    }
    socket.onerror = (error) => {
    console.error("Ошибка сокета:", error, "ReadyState:", socket?.readyState);
    };
    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data)
            if (data.type && data.payload) {
                socketEmit(data.type, data.payload)
            }
        }
        catch (error){
            console.log("WebSocket Error: Failed to parse", error)
        }
    }

    socket.onclose = () => {
        if (reconnectTimer != null) {
            clearTimeout(reconnectTimer)
        }
        setStatus("offline")
        incrementAttempt()
        reconnectTimer = window.setTimeout(connectSocket, getBackoffTime(useSocketState.getState().attempt))
    }
}

export function disconnectSocket() {
    const { setStatus, resetAttempt, incrementAttempt } = useSocketState.getState();
    if (reconnectTimer != null) {
        clearTimeout(reconnectTimer)
    }
    if (socket) {
        socket.onclose = null;
        socket.onerror = null
        if (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING) {
            socket.close();
            }
        socket = null
    } 
    setStatus("offline")
}

export function sendSocketMessage(type: any, payload: any) {
    if (socket?.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type,
            payload
        }))
    }
    else {
        console.log("СОКЕТ НЕ ГОТОВ")
    }
}