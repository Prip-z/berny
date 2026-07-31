
export function getBackoffTime(attempts: number):number {
        return (Math.pow(2, attempts) * 1000 * Math.random()) % 30000
}
