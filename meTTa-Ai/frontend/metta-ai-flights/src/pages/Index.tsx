import { useState, useRef, useEffect } from "react";
import { Message } from "@/components/Message";
import { FlightCard } from "@/components/FlightCard";
import { ChatInput } from "@/components/ChatInput";
import { AnimatedHeadline } from "@/components/AnimatedHeadline";
import { FlightBackground } from "@/components/FlightBackground";
import { LoadingAnimation } from "@/components/LoadingAnimation";
import { FrequentlyAskedQuestions } from "@/components/FrequentlyAskedQuestions";
import { Card } from "@/components/ui/card";
import { Bot, Sparkles, RotateCcw } from "lucide-react";
import { toast } from "@/hooks/use-toast";
import { Link } from "react-router-dom";

interface FlightSegment {
  source: string;
  destination: string;
  takeoff: string;
  landing: string;
  airline: string;
  cost: number;
  duration: number;
}

interface Flight {
  airline?: string;
  source: string;
  destination: string;
  year: number;
  month: number;
  day: number;
  departure: string;
  arrival: string;
  duration_minutes: number;
  cost: number;
  is_connecting?: boolean;
  segments?: FlightSegment[];
  connection_airport?: string;
  layover_hours?: number;
}

interface ChatMessage {
  id: string;
  text?: string;
  sender: "user" | "bot";
  flights?: Flight[];
}

const Index = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (text: string) => {
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text,
      sender: "user"
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender: "user", message: text })
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      data.forEach((msg: any) => {
        const botMessage: ChatMessage = {
          id: Date.now().toString() + Math.random(),
          sender: "bot"
        };

        if (msg.text) {
          botMessage.text = msg.text;
        }

        if (msg.custom && msg.custom.flights) {
          botMessage.flights = msg.custom.flights;
        }

        setMessages(prev => [...prev, botMessage]);
      });
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        text: "⚠️ Server error, could not reach Rasa.",
        sender: "bot"
      };
      setMessages(prev => [...prev, errorMessage]);
      toast({
        title: "Connection Error",
        description: "Could not connect to the flight booking service.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const resetChat = () => {
    setMessages([]);
    toast({
      title: "Chat Reset",
      description: "Starting a new conversation.",
    });
  };

  const bookFlight = async (flight: Flight) => {
    const bookingMessage: ChatMessage = {
      id: Date.now().toString(),
      text: `✈️ Booking flight: ${flight.source} → ${flight.destination}`,
      sender: "user"
    };

    setMessages(prev => [...prev, bookingMessage]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sender: "user",
          message: "/request_booking",
          metadata: {
            flight_info: flight
          }
        })
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      
      data.forEach((msg: any) => {
        if (msg.text) {
          const botMessage: ChatMessage = {
            id: Date.now().toString(),
            text: msg.text,
            sender: "bot"
          };
          setMessages(prev => [...prev, botMessage]);
        }
      });

      toast({
        title: "Booking Initiated",
        description: "Your flight booking request has been processed.",
      });
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        text: "⚠️ Server error while booking.",
        sender: "bot"
      };
      setMessages(prev => [...prev, errorMessage]);
      toast({
        title: "Booking Error",
        description: "There was an error processing your booking request.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/30 flex flex-col relative">
      <FlightBackground />
      
      {/* Header */}
      <div className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-10 relative">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-primary/10">
                <Bot className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground flex items-center gap-2">
                  meTTa-AI
                  <Sparkles className="h-4 w-4 text-primary" />
                </h1>
                <p className="text-sm text-muted-foreground">Your intelligent flight booking assistant</p>
              </div>
            </div>
            
            {/* Navigation */}
            <nav className="flex items-center gap-6">
              <Link 
                to="/bookings" 
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors duration-200 hover:scale-105 transform"
              >
                Bookings
              </Link>
            </nav>
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 max-w-4xl mx-auto w-full px-6 py-6 overflow-hidden relative z-10">
        <Card 
          className="h-full flex flex-col bg-background/60 backdrop-blur-sm border-border"
          style={{ boxShadow: "var(--shadow-elevation)" }}
        >
          <div className="flex-1 overflow-y-auto p-6 space-y-1">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="p-4 rounded-2xl bg-primary/5 inline-block mb-6">
                  <Bot className="h-12 w-12 text-primary mx-auto" />
                </div>
                <AnimatedHeadline />
                <p className="text-muted-foreground max-w-md mx-auto">
                  I'm your intelligent flight booking assistant. Ask me about flights, destinations, 
                  or help with booking your next trip!
                </p>
              </div>
            )}

            {messages.map((message) => (
              <div key={message.id}>
                {message.text && (
                  <Message text={message.text} sender={message.sender} />
                )}
                {message.flights && (
                  <div className="mb-4">
                    {message.flights.map((flight, index) => (
                      <FlightCard
                        key={index}
                        flight={flight}
                        onBook={bookFlight}
                      />
                    ))}
                  </div>
                )}
              </div>
            ))}

            {isLoading && <LoadingAnimation />}

            <div ref={messagesEndRef} />
          </div>

          <div className="border-t border-border p-4 space-y-4">
            <FrequentlyAskedQuestions 
              onQuestionClick={sendMessage}
              disabled={isLoading}
            />
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <ChatInput onSend={sendMessage} disabled={isLoading} />
              </div>
              <button
                onClick={resetChat}
                className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary/50 transition-all duration-200 hover:scale-105 transform"
                title="Reset Chat"
              >
                <RotateCcw className="h-5 w-5" />
              </button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Index;