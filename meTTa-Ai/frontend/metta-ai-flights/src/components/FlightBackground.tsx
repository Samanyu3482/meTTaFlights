import { Plane } from "lucide-react";

export const FlightBackground = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {/* Flying planes */}
      <div className="absolute top-1/4 left-0 w-full h-px">
        <Plane className="w-6 h-6 text-primary/20 animate-fly-right" />
      </div>
      
      <div className="absolute top-1/2 right-0 w-full h-px">
        <Plane className="w-5 h-5 text-primary/15 animate-fly-left transform rotate-180" />
      </div>
      
      <div className="absolute top-3/4 left-0 w-full h-px">
        <Plane className="w-4 h-4 text-primary/10 animate-fly-right-slow" />
      </div>

      {/* Floating elements */}
      <div className="absolute top-1/3 right-1/4 w-2 h-2 bg-primary/10 rounded-full animate-float" />
      <div className="absolute top-2/3 left-1/3 w-3 h-3 bg-primary/5 rounded-full animate-float-delayed" />
      <div className="absolute top-1/2 right-1/3 w-1.5 h-1.5 bg-primary/15 rounded-full animate-float-slow" />
    </div>
  );
};