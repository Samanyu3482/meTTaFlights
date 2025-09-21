import { Button } from "@/components/ui/button";
import { useState } from "react";

interface FAQProps {
  onQuestionClick: (question: string) => void;
  disabled?: boolean;
}

const frequentQuestions = [
  "Tell me about New York",
  "Should I visit Los Angeles?",
  "Seattle places to visit",
  "Best time for Chicago"
];

export const FrequentlyAskedQuestions = ({ onQuestionClick, disabled }: FAQProps) => {
  const [clickedButtons, setClickedButtons] = useState<Set<number>>(new Set());

  const handleClick = (question: string, index: number) => {
    setClickedButtons(prev => new Set(prev).add(index));
    onQuestionClick(question);
    
    // Reset the clicked state after animation
    setTimeout(() => {
      setClickedButtons(prev => {
        const newSet = new Set(prev);
        newSet.delete(index);
        return newSet;
      });
    }, 2000);
  };

  return (
    <div className="flex flex-wrap gap-2 animate-fade-in">
      {frequentQuestions.map((question, index) => (
        <Button
          key={index}
          variant="outline"
          size="sm"
          onClick={() => handleClick(question, index)}
          disabled={disabled}
          className={`text-xs h-8 px-3 rounded-full transition-all duration-300 hover-scale animate-scale-in ${
            clickedButtons.has(index)
              ? "bg-green-500/20 border-green-500/50 text-green-700 dark:text-green-300"
              : "bg-pink-500/20 border-pink-500/50 text-pink-700 dark:text-pink-300 pulse hover:bg-pink-500/30"
          }`}
          style={{
            animationDelay: `${index * 0.1}s`
          }}
        >
          {question}
        </Button>
      ))}
    </div>
  );
};