import { cn } from "@/lib/utils";

interface MessageProps {
  text: string;
  sender: "user" | "bot";
}

export const Message = ({ text, sender }: MessageProps) => {
  return (
    <div
      className={cn(
        "flex w-full mb-4",
        sender === "user" ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[80%] px-4 py-3 rounded-2xl shadow-sm transition-all duration-300",
          sender === "user"
            ? "bg-message-user text-message-user-foreground ml-auto"
            : "bg-message-bot text-message-bot-foreground mr-auto border border-flight-card-border"
        )}
        style={{
          background: sender === "user" ? "var(--primary-gradient)" : undefined,
          boxShadow: "var(--shadow-soft)"
        }}
      >
        <p className="text-sm leading-relaxed whitespace-pre-line">{text}</p>
      </div>
    </div>
  );
};