import { getAccessToken } from "../storage/auth"

export function getCurrentUser() {
    const token = getAccessToken()
    if (!token) return ""
    try {
        const payloadBase64 = token.split('.')[1]
        const decodedPayload = JSON.parse(atob(payloadBase64))
        return decodedPayload.sub || ""
    } catch {
        return ""
    }
}