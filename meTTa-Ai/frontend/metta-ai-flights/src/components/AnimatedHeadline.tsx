import { useState, useEffect } from "react";

const headlines = [
  "MeTTa-AI: Transforming Flight Booking",
  "Smart Flights, Smarter Future – MeTTa-AI",
  "Flying Smarter, Booking Faster – MeTTa-AI",
  "Your AI Co-Pilot for Best Flight Routes"
];

export const AnimatedHeadline = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    const currentHeadline = headlines[currentIndex];
    
    if (isTyping) {
      // Typing effect
      if (displayText.length < currentHeadline.length) {
        const timeout = setTimeout(() => {
          setDisplayText(currentHeadline.slice(0, displayText.length + 1));
        }, 50);
        return () => clearTimeout(timeout);
      } else {
        // Pause at full text
        const timeout = setTimeout(() => {
          setIsTyping(false);
        }, 2000);
        return () => clearTimeout(timeout);
      }
    } else {
      // Erasing effect
      if (displayText.length > 0) {
        const timeout = setTimeout(() => {
          setDisplayText(displayText.slice(0, -1));
        }, 30);
        return () => clearTimeout(timeout);
      } else {
        // Move to next headline
        const timeout = setTimeout(() => {
          setCurrentIndex((prev) => (prev + 1) % headlines.length);
          setIsTyping(true);
        }, 500);
        return () => clearTimeout(timeout);
      }
    }
  }, [displayText, isTyping, currentIndex]);

  return (
    <div className="text-center mb-8">
      <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-primary via-purple-500 to-primary bg-clip-text text-transparent min-h-[2.5rem] flex items-center justify-center">
        {displayText}
        <span className="ml-1 w-0.5 h-6 bg-primary animate-pulse" />
      </h1>
    </div>
  );
};