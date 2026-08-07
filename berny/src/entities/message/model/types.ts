import {z} from 'zod';

export const MessageSchema = z.object({
    message_id: z.string(),
    text: z.string(),
    sender_id: z.string(),
    created_at: z.string(),
    status: z.enum(["sent", "departing", "read"]).default("sent")
})

export type MessageType = z.infer<typeof MessageSchema>