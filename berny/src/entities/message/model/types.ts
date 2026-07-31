import {z} from 'zod';

export const MessageSchema = z.object({
    id: z.string(),
    text: z.string(),
    senderId: z.string(),
    timestamp: z.string(),
    status: z.enum(["sent", "departing", "read"])
})

export type MessageType = z.infer<typeof MessageSchema>