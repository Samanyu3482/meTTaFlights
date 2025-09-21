import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput = ({ onSend, disabled }: ChatInputProps) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t border-border bg-background">
      <div className="flex gap-3 items-end">
        <div className="flex-1 relative">
          <Input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about flights..."
            disabled={disabled}
            className={cn(
              "pr-12 py-3 bg-muted/50 border-border rounded-xl",
              "focus:ring-2 focus:ring-primary/20 focus:border-primary",
              "transition-all duration-300"
            )}
          />
        </div>
        <Button
          type="submit"
          disabled={!message.trim() || disabled}
          size="sm"
          className={cn(
            "px-4 py-3 rounded-xl transition-all duration-300",
            "disabled:opacity-50 disabled:cursor-not-allowed"
          )}
          style={{ background: "var(--primary-gradient)" }}
        >
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </form>
  );
};