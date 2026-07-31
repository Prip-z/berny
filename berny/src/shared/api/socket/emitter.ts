type Listener = (payload: any) => void

const listeners: Record<string, Set<Listener>> = {}

export function socketSubscribe(eventType: string, callback: Listener) {
    if (!listeners[eventType]) {
        listeners[eventType] = new Set()
    }
    listeners[eventType].add(callback)

    return () => listeners[eventType].delete(callback) 
}

export function socketEmit(eventType: string, payload: any) {
    if (listeners[eventType]) {
        listeners[eventType].forEach((callback) => callback(payload))
    }
}