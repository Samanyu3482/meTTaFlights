"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Badge } from "@/components/ui/badge"
import { CalendarIcon, Search, MapPin, Users, ArrowLeftRight } from "lucide-react"
import { format } from "date-fns"

interface FlightSearchProps {
  onSearch?: (searchData: any) => void
  className?: string
}

export function FlightSearch({ onSearch, className }: FlightSearchProps) {
  const [tripType, setTripType] = useState("roundtrip")
  const [from, setFrom] = useState("")
  const [to, setTo] = useState("")
  const [departDate, setDepartDate] = useState<Date>()
  const [returnDate, setReturnDate] = useState<Date>()
  const [passengers, setPassengers] = useState("1")
  const [travelClass, setTravelClass] = useState("economy")

  const handleSearch = () => {
    const searchData = {
      tripType,
      from,
      to,
      departDate,
      returnDate,
      passengers: Number.parseInt(passengers),
      travelClass,
    }
    onSearch?.(searchData)
  }

  const swapLocations = () => {
    const temp = from
    setFrom(to)
    setTo(temp)
  }

  return (
    <Card className={`w-full ${className}`}>
      <CardContent className="p-6">
        <Tabs value={tripType} onValueChange={setTripType} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="roundtrip">Round Trip</TabsTrigger>
            <TabsTrigger value="oneway">One Way</TabsTrigger>
            <TabsTrigger value="multicity">Multi-city</TabsTrigger>
          </TabsList>

          <TabsContent value={tripType} className="mt-6">
            <div className="grid gap-4">
              {/* From and To */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 relative">
                <div className="space-y-2">
                  <Label htmlFor="from">From</Label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="from"
                      placeholder="Departure city or airport"
                      value={from}
                      onChange={(e) => setFrom(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="to">To</Label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="to"
                      placeholder="Destination city or airport"
                      value={to}
                      onChange={(e) => setTo(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                <Button
                  variant="outline"
                  size="icon"
                  className="absolute top-8 left-1/2 transform -translate-x-1/2 z-10 hidden md:flex bg-transparent"
                  onClick={swapLocations}
                >
                  <ArrowLeftRight className="h-4 w-4" />
                </Button>
              </div>

              {/* Dates */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Departure Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button variant="outline" className="w-full justify-start text-left font-normal bg-transparent">
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {departDate ? format(departDate, "PPP") : "Select date"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar mode="single" selected={departDate} onSelect={setDepartDate} initialFocus />
                    </PopoverContent>
                  </Popover>
                </div>

                {tripType === "roundtrip" && (
                  <div className="space-y-2">
                    <Label>Return Date</Label>
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button variant="outline" className="w-full justify-start text-left font-normal bg-transparent">
                          <CalendarIcon className="mr-2 h-4 w-4" />
                          {returnDate ? format(returnDate, "PPP") : "Select date"}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0">
                        <Calendar mode="single" selected={returnDate} onSelect={setReturnDate} initialFocus />
                      </PopoverContent>
                    </Popover>
                  </div>
                )}
              </div>

              {/* Passengers and Class */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Passengers</Label>
                  <Select value={passengers} onValueChange={setPassengers}>
                    <SelectTrigger>
                      <Users className="mr-2 h-4 w-4" />
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
                        <SelectItem key={num} value={num.toString()}>
                          {num} {num === 1 ? "Passenger" : "Passengers"}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Class</Label>
                  <Select value={travelClass} onValueChange={setTravelClass}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="economy">
                        <div className="flex items-center">
                          Economy
                          <Badge variant="secondary" className="ml-2">
                            Best Value
                          </Badge>
                        </div>
                      </SelectItem>
                      <SelectItem value="premium">Premium Economy</SelectItem>
                      <SelectItem value="business">Business</SelectItem>
                      <SelectItem value="first">First Class</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Search Button */}
              <Button onClick={handleSearch} size="lg" className="w-full flight-gradient text-white font-semibold">
                <Search className="mr-2 h-5 w-5" />
                Search Flights
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
