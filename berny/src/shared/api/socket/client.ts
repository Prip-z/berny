"use client";

import { getBackoffTime } from "../../lib/backoff";
import { socketEmit } from "./emitter";
import { useSocketState } from "./store";

const WEBSOCKET_ADDRESS = 'ws://172.31.208.1:8000/ws/123'

let socket: WebSocket | null = null
let reconnectTimer: ReturnType<typeof setTimeout>

export function connectSocket() {
    const { setStatus, resetAttempt, incrementAttempt } = useSocketState.getState();
    setStatus("connecting")

    if ((socket?.readyState === WebSocket.OPEN) || (socket?.readyState === WebSocket.CONNECTING)) {
        return
    }
    else {
        socket = new WebSocket(WEBSOCKET_ADDRESS);
    }
    

    socket.onopen = () => {
        resetAttempt()
        setStatus("online")
    }
    socket.onerror = (error) => console.error("Ошибка сокета:", error);
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
        reconnectTimer = setTimeout(connectSocket, getBackoffTime(useSocketState.getState().attempt))
    }
}

export function disconnectSocket() {
    const { setStatus, resetAttempt, incrementAttempt } = useSocketState.getState();
    if (reconnectTimer != null) {
        clearTimeout(reconnectTimer)
    }
    if (socket) {
        socket.onclose = null;
        socket.close();
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