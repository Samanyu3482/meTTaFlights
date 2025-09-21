import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Plane, Clock, DollarSign, MapPin } from "lucide-react";
import { formatTime, formatDuration } from "@/lib/utils";

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

interface FlightCardProps {
  flight: Flight;
  onBook: (flight: Flight) => void;
}

export const FlightCard = ({ flight, onBook }: FlightCardProps) => {
  return (
    <Card 
      className="p-6 mb-4 bg-flight-card border-flight-card-border transition-all duration-300 hover:shadow-lg"
      style={{ boxShadow: "var(--shadow-soft)" }}
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-primary/10">
          <Plane className="h-5 w-5 text-primary" />
        </div>
        <h3 className="font-semibold text-lg text-foreground">
          {flight.airline || "Flight Details"}
        </h3>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm text-muted-foreground">Route:</span>
          <span className="font-medium">{flight.source} → {flight.destination}</span>
        </div>
        
        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm text-muted-foreground">Duration:</span>
          <span className="font-medium">{formatDuration(flight.duration_minutes)}</span>
        </div>
      </div>

      <div className="space-y-2 mb-4 text-sm">
        <p><span className="text-muted-foreground">Date:</span> <span className="font-medium">{flight.year}-{flight.month}-{flight.day}</span></p>
        <p><span className="text-muted-foreground">Departure:</span> <span className="font-medium">{formatTime(flight.departure)}</span></p>
        <p><span className="text-muted-foreground">Arrival:</span> <span className="font-medium">{formatTime(flight.arrival)}</span></p>
      </div>

      {flight.is_connecting && flight.segments && (
        <div className="mb-4 p-3 bg-secondary/50 rounded-lg">
          <h4 className="font-medium mb-2 text-sm">Flight Segments:</h4>
          <div className="space-y-2">
            {flight.segments.map((seg, i) => (
              <div key={i} className="text-xs text-muted-foreground pl-2 border-l-2 border-primary/20">
                <p><strong>{i + 1}.</strong> {seg.source} → {seg.destination} | {formatTime(seg.takeoff)} → {formatTime(seg.landing)}</p>
                <p className="ml-4">Airline: {seg.airline}, Cost: ${seg.cost}, Duration: {formatDuration(seg.duration)}</p>
              </div>
            ))}
            {flight.connection_airport && flight.layover_hours && (
              <p className="text-xs text-muted-foreground pl-2">
                Layover at {flight.connection_airport}: {flight.layover_hours} hrs
              </p>
            )}
          </div>
        </div>
      )}

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <DollarSign className="h-4 w-4 text-primary" />
          <span className="text-2xl font-bold text-primary">${flight.cost}</span>
        </div>
        
        <Button 
          onClick={() => onBook(flight)}
          className="bg-primary hover:bg-primary/90 transition-all duration-300"
          style={{ background: "var(--primary-gradient)" }}
        >
          Book This Flight
        </Button>
      </div>
    </Card>
  );
};