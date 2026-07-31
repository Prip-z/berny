import { socketSubscribe } from "@/src/shared/api/socket";
import { useEffect, useState } from "react";
import { z } from "zod";

const UserPresencePayloadSchema = z.object({
    userId: z.string(),
    username: z.string().optional(),
});


export function UserPresence() {
    const [isOnline, setIsOnline] = useState(false);
    useEffect(() => {
        let timer: ReturnType<typeof setTimeout> | null = null
        const unsubscribe = socketSubscribe("USER_PRESENCE", (rawPayload: unknown) => {
            const parsed = UserPresencePayloadSchema.safeParse(rawPayload);

            if (!parsed.success) {
                console.error("Invalid USER_PRESENCE payload:", parsed.error.format());
                return;
            }

            const payload = parsed.data;
            setIsOnline(true)
            if (timer) {
                clearTimeout(timer)
            }
            timer = setTimeout(() => setIsOnline(false), 3000)
        })


        return () => {
            unsubscribe();
            if (timer) {
                clearTimeout(timer);
            }
        };
    }, [])

    if (!isOnline) return null

    return (
        <div className="py-1.5 text-center text-xs font-medium">
            🟢Онлайн
        </div>
    )
}