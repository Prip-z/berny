import { socketSubscribe } from "@/src/shared";
import { useEffect, useState } from "react";
import { z } from "zod";

const typingPayloadSchema = z.object({
  userId: z.string(),
  username: z.string().optional(),
});

export function TypingIndicator() {
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    let timer: ReturnType<typeof setTimeout> | null = null;

    const unsubscribe = socketSubscribe("TYPING", (rawPayload: unknown) => {
      const parsed = typingPayloadSchema.safeParse(rawPayload);

      if (!parsed.success) {
        console.error("Invalid TYPING payload:", parsed.error.format());
        return;
      }

      const payload = parsed.data; 

      setIsTyping(true);

      if (timer) {
        clearTimeout(timer);
      }

      timer = setTimeout(() => setIsTyping(false), 3000);
    });

    return () => {
      unsubscribe();
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, []);

  if (!isTyping) return null;

  return (
    <div className="py-1.5 text-center text-xs font-medium animate-pulse">
      ...Печатает
    </div>
  );
}