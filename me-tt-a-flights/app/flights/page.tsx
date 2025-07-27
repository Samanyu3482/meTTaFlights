"use client"

import { useState } from "react"
import { Navigation } from "@/components/navigation"
import { FlightSearch } from "@/components/flight-search"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Plane, Filter, Wifi, Coffee, Utensils, Star, Heart } from "lucide-react"

interface Flight {
  id: string
  airline: string
  logo: string
  flightNumber: string
  departure: {
    airport: string
    city: string
    time: string
    date: string
  }
  arrival: {
    airport: string
    city: string
    time: string
    date: string
  }
  duration: string
  stops: number
  price: number
  class: string
  amenities: string[]
  rating: number
  baggage: string
}

const mockFlights: Flight[] = [
  {
    id: "1",
    airline: "Delta Airlines",
    logo: "/placeholder.svg?height=40&width=40",
    flightNumber: "DL 1234",
    departure: {
      airport: "JFK",
      city: "New York",
      time: "08:30",
      date: "2024-03-15",
    },
    arrival: {
      airport: "LAX",
      city: "Los Angeles",
      time: "11:45",
      date: "2024-03-15",
    },
    duration: "6h 15m",
    stops: 0,
    price: 299,
    class: "Economy",
    amenities: ["wifi", "entertainment", "meals"],
    rating: 4.5,
    baggage: "1 carry-on, 1 checked bag",
  },
  {
    id: "2",
    airline: "American Airlines",
    logo: "/placeholder.svg?height=40&width=40",
    flightNumber: "AA 5678",
    departure: {
      airport: "JFK",
      city: "New York",
      time: "14:20",
      date: "2024-03-15",
    },
    arrival: {
      airport: "LAX",
      city: "Los Angeles",
      time: "17:35",
      date: "2024-03-15",
    },
    duration: "6h 15m",
    stops: 0,
    price: 349,
    class: "Economy",
    amenities: ["wifi", "entertainment"],
    rating: 4.2,
    baggage: "1 carry-on, 1 checked bag",
  },
  {
    id: "3",
    airline: "United Airlines",
    logo: "/placeholder.svg?height=40&width=40",
    flightNumber: "UA 9012",
    departure: {
      airport: "JFK",
      city: "New York",
      time: "19:45",
      date: "2024-03-15",
    },
    arrival: {
      airport: "LAX",
      city: "Los Angeles",
      time: "23:00",
      date: "2024-03-15",
    },
    duration: "6h 15m",
    stops: 0,
    price: 279,
    class: "Economy",
    amenities: ["wifi", "entertainment", "meals"],
    rating: 4.3,
    baggage: "1 carry-on, 1 checked bag",
  },
]

export default function FlightsPage() {
  const [flights, setFlights] = useState<Flight[]>(mockFlights)
  const [sortBy, setSortBy] = useState("price")
  const [priceRange, setPriceRange] = useState([0, 1000])
  const [selectedAirlines, setSelectedAirlines] = useState<string[]>([])
  const [stopsFilter, setStopsFilter] = useState<string>("any")
  const [showFilters, setShowFilters] = useState(false)

  const handleSearch = (searchData: any) => {
    // In a real app, this would make an API call
    console.log("Search data:", searchData)
    // For demo, we'll just show the existing flights
  }

  const sortedFlights = [...flights].sort((a, b) => {
    switch (sortBy) {
      case "price":
        return a.price - b.price
      case "duration":
        return a.duration.localeCompare(b.duration)
      case "departure":
        return a.departure.time.localeCompare(b.departure.time)
      case "rating":
        return b.rating - a.rating
      default:
        return 0
    }
  })

  const getAmenityIcon = (amenity: string) => {
    switch (amenity) {
      case "wifi":
        return <Wifi className="h-4 w-4" />
      case "entertainment":
        return <Star className="h-4 w-4" />
      case "meals":
        return <Utensils className="h-4 w-4" />
      default:
        return <Coffee className="h-4 w-4" />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Search Section */}
        <div className="mb-8">
          <FlightSearch onSearch={handleSearch} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center">
                    <Filter className="mr-2 h-5 w-5" />
                    Filters
                  </CardTitle>
                  <Button variant="ghost" size="sm" className="lg:hidden" onClick={() => setShowFilters(!showFilters)}>
                    {showFilters ? "Hide" : "Show"}
                  </Button>
                </div>
              </CardHeader>
              <CardContent className={`space-y-6 ${showFilters ? "block" : "hidden lg:block"}`}>
                {/* Price Range */}
                <div>
                  <Label className="text-sm font-medium mb-3 block">Price Range</Label>
                  <Slider
                    value={priceRange}
                    onValueChange={setPriceRange}
                    max={1000}
                    min={0}
                    step={50}
                    className="mb-2"
                  />
                  <div className="flex justify-between text-sm text-muted-foreground">
                    <span>${priceRange[0]}</span>
                    <span>${priceRange[1]}</span>
                  </div>
                </div>

                <Separator />

                {/* Airlines */}
                <div>
                  <Label className="text-sm font-medium mb-3 block">Airlines</Label>
                  <div className="space-y-2">
                    {["Delta Airlines", "American Airlines", "United Airlines"].map((airline) => (
                      <div key={airline} className="flex items-center space-x-2">
                        <Checkbox
                          id={airline}
                          checked={selectedAirlines.includes(airline)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedAirlines([...selectedAirlines, airline])
                            } else {
                              setSelectedAirlines(selectedAirlines.filter((a) => a !== airline))
                            }
                          }}
                        />
                        <Label htmlFor={airline} className="text-sm">
                          {airline}
                        </Label>
                      </div>
                    ))}
                  </div>
                </div>

                <Separator />

                {/* Stops */}
                <div>
                  <Label className="text-sm font-medium mb-3 block">Stops</Label>
                  <Select value={stopsFilter} onValueChange={setStopsFilter}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="any">Any number of stops</SelectItem>
                      <SelectItem value="0">Non-stop</SelectItem>
                      <SelectItem value="1">1 stop</SelectItem>
                      <SelectItem value="2+">2+ stops</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-3">
            {/* Sort and Results Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold">Flight Results</h2>
                <p className="text-muted-foreground">{flights.length} flights found</p>
              </div>
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="price">Price (Low to High)</SelectItem>
                  <SelectItem value="duration">Duration</SelectItem>
                  <SelectItem value="departure">Departure Time</SelectItem>
                  <SelectItem value="rating">Rating</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Flight Cards */}
            <div className="space-y-4">
              {sortedFlights.map((flight) => (
                <Card key={flight.id} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
                      {/* Airline Info */}
                      <div className="md:col-span-2">
                        <div className="flex items-center space-x-3">
                          <img
                            src={flight.logo || "/placeholder.svg"}
                            alt={flight.airline}
                            className="w-10 h-10 rounded"
                          />
                          <div>
                            <p className="font-medium text-sm">{flight.airline}</p>
                            <p className="text-xs text-muted-foreground">{flight.flightNumber}</p>
                          </div>
                        </div>
                      </div>

                      {/* Flight Times */}
                      <div className="md:col-span-6">
                        <div className="flex items-center justify-between">
                          <div className="text-center">
                            <p className="text-2xl font-bold">{flight.departure.time}</p>
                            <p className="text-sm text-muted-foreground">{flight.departure.airport}</p>
                            <p className="text-xs text-muted-foreground">{flight.departure.city}</p>
                          </div>

                          <div className="flex-1 mx-4">
                            <div className="flex items-center justify-center space-x-2">
                              <div className="flex-1 h-px bg-border"></div>
                              <div className="text-center">
                                <Plane className="h-4 w-4 text-muted-foreground mx-auto mb-1" />
                                <p className="text-xs text-muted-foreground">{flight.duration}</p>
                                {flight.stops === 0 ? (
                                  <Badge variant="secondary" className="text-xs">
                                    Non-stop
                                  </Badge>
                                ) : (
                                  <Badge variant="outline" className="text-xs">
                                    {flight.stops} stop{flight.stops > 1 ? "s" : ""}
                                  </Badge>
                                )}
                              </div>
                              <div className="flex-1 h-px bg-border"></div>
                            </div>
                          </div>

                          <div className="text-center">
                            <p className="text-2xl font-bold">{flight.arrival.time}</p>
                            <p className="text-sm text-muted-foreground">{flight.arrival.airport}</p>
                            <p className="text-xs text-muted-foreground">{flight.arrival.city}</p>
                          </div>
                        </div>
                      </div>

                      {/* Price and Book */}
                      <div className="md:col-span-4 text-right">
                        <div className="flex items-center justify-end space-x-4">
                          <div>
                            <p className="text-3xl font-bold text-primary">${flight.price}</p>
                            <p className="text-sm text-muted-foreground">{flight.class}</p>
                            <div className="flex items-center justify-end mt-1">
                              <Star className="h-3 w-3 fill-yellow-400 text-yellow-400 mr-1" />
                              <span className="text-xs text-muted-foreground">{flight.rating}</span>
                            </div>
                          </div>
                          <Button className="flight-gradient text-white">Select Flight</Button>
                        </div>
                      </div>
                    </div>

                    {/* Flight Details */}
                    <div className="mt-4 pt-4 border-t">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center space-x-2">
                            {flight.amenities.map((amenity, index) => (
                              <div key={index} className="flex items-center space-x-1 text-muted-foreground">
                                {getAmenityIcon(amenity)}
                                <span className="text-xs capitalize">{amenity}</span>
                              </div>
                            ))}
                          </div>
                          <Separator orientation="vertical" className="h-4" />
                          <p className="text-xs text-muted-foreground">{flight.baggage}</p>
                        </div>
                        <Button variant="ghost" size="sm">
                          <Heart className="h-4 w-4 mr-1" />
                          Save
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Load More */}
            <div className="text-center mt-8">
              <Button variant="outline" size="lg">
                Load More Flights
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
