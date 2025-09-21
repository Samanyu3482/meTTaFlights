import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Plane, Clock, Calendar, MapPin, DollarSign } from "lucide-react";
import { Link } from "react-router-dom";
import { formatTime, formatDuration } from "@/lib/utils";

interface BookedFlight {
  id: string;
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
  bookingDate: string;
  status: "confirmed" | "pending" | "cancelled";
}

// Mock data - replace with actual API call
const mockBookings: BookedFlight[] = [
  {
    id: "BK001",
    airline: "Air India",
    source: "DEL",
    destination: "BOM",
    year: 2024,
    month: 12,
    day: 25,
    departure: "0830",
    arrival: "1045",
    duration_minutes: 135,
    cost: 8500,
    bookingDate: "2024-12-18",
    status: "confirmed"
  },
  {
    id: "BK002",
    airline: "SpiceJet",
    source: "BOM",
    destination: "BLR",
    year: 2024,
    month: 12,
    day: 28,
    departure: "1430",
    arrival: "1545",
    duration_minutes: 75,
    cost: 4200,
    bookingDate: "2024-12-17",
    status: "confirmed"
  }
];

const BookingCard = ({ booking }: { booking: BookedFlight }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "confirmed": return "text-green-600 bg-green-50";
      case "pending": return "text-yellow-600 bg-yellow-50";
      case "cancelled": return "text-red-600 bg-red-50";
      default: return "text-gray-600 bg-gray-50";
    }
  };

  return (
    <Card className="p-6 mb-4 bg-card border transition-all duration-300 hover:shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <Plane className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h3 className="font-semibold text-lg text-foreground">
              {booking.airline || "Flight"}
            </h3>
            <p className="text-sm text-muted-foreground">Booking ID: {booking.id}</p>
          </div>
        </div>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(booking.status)}`}>
          {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="flex items-center gap-2">
          <MapPin className="h-4 w-4 text-muted-foreground" />
          <div>
            <span className="text-sm text-muted-foreground">Route</span>
            <p className="font-medium">{booking.source} → {booking.destination}</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4 text-muted-foreground" />
          <div>
            <span className="text-sm text-muted-foreground">Travel Date</span>
            <p className="font-medium">{booking.year}-{String(booking.month).padStart(2, '0')}-{String(booking.day).padStart(2, '0')}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-muted-foreground" />
          <div>
            <span className="text-sm text-muted-foreground">Duration</span>
            <p className="font-medium">{formatDuration(booking.duration_minutes)}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 text-sm">
        <div>
          <span className="text-muted-foreground">Departure:</span> 
          <span className="font-medium ml-2">{formatTime(booking.departure)}</span>
        </div>
        <div>
          <span className="text-muted-foreground">Arrival:</span> 
          <span className="font-medium ml-2">{formatTime(booking.arrival)}</span>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t">
        <div>
          <span className="text-sm text-muted-foreground">Booked on: </span>
          <span className="font-medium">{booking.bookingDate}</span>
        </div>
        <div className="flex items-center gap-2">
          <DollarSign className="h-4 w-4 text-primary" />
          <span className="text-xl font-bold text-primary">₹{booking.cost.toLocaleString()}</span>
        </div>
      </div>
    </Card>
  );
};

const Bookings = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-indigo-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Link to="/">
            <Button variant="ghost" className="mb-4">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Search
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-foreground mb-2">My Bookings</h1>
          <p className="text-muted-foreground">View and manage your flight bookings</p>
        </div>

        <div className="max-w-4xl mx-auto">
          {mockBookings.length > 0 ? (
            <div className="space-y-4">
              {mockBookings.map((booking) => (
                <BookingCard key={booking.id} booking={booking} />
              ))}
            </div>
          ) : (
            <Card className="p-12 text-center">
              <div className="p-4 rounded-full bg-muted/50 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <Plane className="h-8 w-8 text-muted-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-2">No bookings yet</h3>
              <p className="text-muted-foreground mb-4">
                You haven't made any flight bookings yet. Start by searching for flights!
              </p>
              <Link to="/">
                <Button>Search Flights</Button>
              </Link>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default Bookings;