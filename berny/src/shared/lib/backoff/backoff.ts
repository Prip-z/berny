
export function getBackoffTime(attempts: number):number {
    const baseDelay = Math.pow(2, attempts) * 1000
    const jitter = Math.random() * 1000
    return Math.min(baseDelay + jitter, 30000)
}
