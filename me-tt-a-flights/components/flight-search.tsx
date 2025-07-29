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
import { getAirportLocation } from "@/lib/airports"
import { AirportAutocomplete } from "./airport-autocomplete"

interface FlightSearchProps {
  onSearch?: (searchData: any) => void
  className?: string
  initialFrom?: string
  initialTo?: string
  initialDate?: Date
}

export function FlightSearch({ onSearch, className, initialFrom, initialTo, initialDate }: FlightSearchProps) {
  const [tripType, setTripType] = useState("roundtrip")
  const [from, setFrom] = useState(initialFrom || "")
  const [to, setTo] = useState(initialTo || "")
  const [departDate, setDepartDate] = useState<Date>(() => {
    if (initialDate) return initialDate
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow;
  }) // Default to tomorrow
  const [returnDate, setReturnDate] = useState<Date>()
  const [passengers, setPassengers] = useState("1")
  const [customPassengers, setCustomPassengers] = useState("")
  const [showCustomPassengers, setShowCustomPassengers] = useState(false)
  const [travelClass, setTravelClass] = useState("economy")
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    setLoading(true)
    
    // Prepare search data for the parent component
    const searchData = {
      tripType,
      from,
      to,
      departDate,
      returnDate,
      passengers: showCustomPassengers && customPassengers 
        ? Number.parseInt(customPassengers) 
        : Number.parseInt(passengers),
      travelClass,
    }
    
    // Call the parent's onSearch callback
    if (onSearch) {
      await onSearch(searchData)
    }
    
    setLoading(false)
  }

  const swapLocations = () => {
    // Only swap if both fields have values
    if (from && to) {
      const temp = from
      setFrom(to)
      setTo(temp)
    } else if (from && !to) {
      // If only "from" has a value, move it to "to"
      setTo(from)
      setFrom("")
    } else if (!from && to) {
      // If only "to" has a value, move it to "from"
      setFrom(to)
      setTo("")
    }
    // If both are empty, do nothing
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
            <div className="grid gap-6">
              {/* From and To */}
              <div className="space-y-3">
                <div className="flex items-center justify-center gap-4">
                  <div className="flex-1 max-w-[280px]">
                    <AirportAutocomplete
                      value={from}
                      onChange={setFrom}
                      label="From"
                      placeholder="Search airports (code, name, or city)"
                    />
                  </div>

                  {/* Swap button in the center */}
                  <Button
                    variant="outline"
                    size="icon"
                    className="hidden md:flex bg-background border-2 hover:bg-muted shadow-sm mt-6 transition-all duration-200 hover:scale-110"
                    onClick={swapLocations}
                    title="Swap origin and destination"
                  >
                    <ArrowLeftRight className="h-4 w-4" />
                  </Button>

                  <div className="flex-1 max-w-[280px]">
                    <AirportAutocomplete
                      value={to}
                      onChange={setTo}
                      label="To"
                      placeholder="Search airports (code, name, or city)"
                    />
                  </div>
                </div>

                {/* Search tips */}
                <div className="text-center">
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    💡 Try typing: airport codes (LAX), city names (Los Angeles), or airport names (Kennedy)
                  </p>
                </div>
              </div>

              {/* Quick Route Presets */}
              <div className="space-y-3">
                <Label className="text-sm">Quick Routes</Label>
                <div className="flex flex-wrap gap-3">
                  <Button 
                    variant="outline" 
                    size="sm" 
                                          onClick={() => { 
                        setFrom("JFK"); 
                        setTo("LAX"); 
                        const tomorrow = new Date();
                        tomorrow.setDate(tomorrow.getDate() + 1);
                        setDepartDate(tomorrow);
                      }}
                    className="text-xs"
                    title="New York JFK → Los Angeles LAX"
                  >
                    JFK → LAX
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                                          onClick={() => { 
                        setFrom("EWR"); 
                        setTo("ATL"); 
                        const nextWeek = new Date();
                        nextWeek.setDate(nextWeek.getDate() + 7);
                        setDepartDate(nextWeek);
                      }}
                    className="text-xs"
                    title="Newark EWR → Atlanta ATL"
                  >
                    EWR → ATL
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                                          onClick={() => { 
                        setFrom("EWR"); 
                        setTo("BOS"); 
                        const nextWeek = new Date();
                        nextWeek.setDate(nextWeek.getDate() + 7);
                        setDepartDate(nextWeek);
                      }}
                    className="text-xs"
                    title="Newark EWR → Boston BOS"
                  >
                    EWR → BOS
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                                          onClick={() => { 
                        setFrom("EWR"); 
                        setTo("SEA"); 
                        const nextWeek = new Date();
                        nextWeek.setDate(nextWeek.getDate() + 7);
                        setDepartDate(nextWeek);
                      }}
                    className="text-xs"
                    title="Newark EWR → Seattle SEA"
                  >
                    EWR → SEA
                  </Button>
                </div>
              </div>

              {/* Dates */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <Label>Departure Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button variant="outline" className="w-full justify-start text-left font-normal bg-transparent">
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {departDate ? format(departDate, "PPP") : "Select date"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar 
                        mode="single" 
                        selected={departDate} 
                        onSelect={setDepartDate} 
                        initialFocus
                        disabled={(date) => date < new Date()}
                        fromYear={2024}
                        toYear={2026}
                        captionLayout="dropdown-buttons"
                      />
                    </PopoverContent>
                  </Popover>
                </div>

                {tripType === "roundtrip" && (
                  <div className="space-y-3">
                    <Label>Return Date</Label>
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button variant="outline" className="w-full justify-start text-left font-normal bg-transparent">
                          <CalendarIcon className="mr-2 h-4 w-4" />
                          {returnDate ? format(returnDate, "PPP") : "Select date"}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0">
                        <Calendar 
                          mode="single" 
                          selected={returnDate} 
                          onSelect={setReturnDate} 
                          initialFocus
                          disabled={(date) => date < new Date()}
                          fromYear={2024}
                          toYear={2026}
                          captionLayout="dropdown-buttons"
                        />
                      </PopoverContent>
                    </Popover>
                  </div>
                )}
              </div>



              {/* Passengers and Class */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <Label>Passengers</Label>
                  {!showCustomPassengers ? (
                    <Select 
                      value={passengers} 
                      onValueChange={(value) => {
                        if (value === "custom") {
                          setShowCustomPassengers(true)
                        } else {
                          setPassengers(value)
                        }
                      }}
                    >
                      <SelectTrigger>
                        <Users className="mr-2 h-4 w-4" />
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1">1 Passenger</SelectItem>
                        <SelectItem value="2">2 Passengers</SelectItem>
                        <SelectItem value="custom">Custom</SelectItem>
                      </SelectContent>
                    </Select>
                  ) : (
                    <div className="space-y-2">
                      <div className="flex gap-2">
                        <Input
                          type="number"
                          min="1"
                          max="20"
                          placeholder="Enter number"
                          value={customPassengers}
                          onChange={(e) => setCustomPassengers(e.target.value)}
                          className="flex-1"
                        />
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setShowCustomPassengers(false)
                            setCustomPassengers("")
                          }}
                        >
                          Cancel
                        </Button>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        Enter a number between 1-20
                      </p>
                    </div>
                  )}
                </div>

                <div className="space-y-3">
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
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Search Button */}
              <Button onClick={handleSearch} size="lg" className="w-full flight-gradient text-white font-semibold" disabled={loading}>
                <Search className="mr-2 h-5 w-5" />
                {loading ? "Searching..." : "Search Flights"}
              </Button>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
