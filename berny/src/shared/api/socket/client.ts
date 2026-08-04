"use client";

import { useChannelsStore } from "@/src/entities/chat/model/store";
import { getBackoffTime } from "../../lib/backoff";
import { socketEmit } from "./emitter";
import { useSocketState } from "./store";

let socket: WebSocket | null = null;
let reconnectTimer: ReturnType<typeof setTimeout>

export function connectSocket() {
    const activeChannelId = useChannelsStore.getState().activeChannelId
    if (!activeChannelId) return
    if (socket) {
        socket.close()
    }
    const WEBSOCKET_ADDRESS = `ws://172.31.208.1:8000/ws/${activeChannelId}`
    const { setStatus, resetAttempt, incrementAttempt } = useSocketState.getState();
    setStatus("connecting")

    const token = localStorage.getItem('accessToken')
    const protocols = token ? [token] : []
    
    socket = new WebSocket(WEBSOCKET_ADDRESS, protocols)

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