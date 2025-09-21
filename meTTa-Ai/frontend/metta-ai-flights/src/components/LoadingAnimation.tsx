import { Plane } from "lucide-react";

export const LoadingAnimation = () => {
  return (
    <div className="flex justify-start mb-4">
      <div className="bg-message-bot border border-flight-card-border rounded-2xl px-6 py-4 max-w-[80%]">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Plane className="w-6 h-6 text-primary animate-plane-loading" />
            <div className="absolute -right-8 top-1/2 transform -translate-y-1/2">
              <div className="flex space-x-1">
                <div className="w-1 h-1 bg-primary/60 rounded-full animate-bounce"></div>
                <div className="w-1 h-1 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                <div className="w-1 h-1 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
              </div>
            </div>
          </div>
          <span className="text-sm text-muted-foreground ml-4">meTTa-AI is searching for flights...</span>
        </div>
      </div>
    </div>
  );
};