"use client"

import { useState, useEffect } from "react"
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
import { Plane, Filter, Calendar, MapPin, DollarSign, Star, Heart, Loader2, ArrowLeftRight, Clock, Zap } from "lucide-react"
import { useFlightSearch } from "@/hooks/use-flight-search"
import { Flight } from "@/lib/api"
import { getAirportLocation } from "@/lib/airports"

export default function FlightsPage() {
  const { flights: mettaFlights, loading, error, getAllFlights, searchFlights } = useFlightSearch()
  const [filteredFlights, setFilteredFlights] = useState<Flight[]>([])
  const [priority, setPriority] = useState<"cost" | "time" | "optimized">("cost")
  const [includeConnections, setIncludeConnections] = useState(true)
  const [priceRange, setPriceRange] = useState([0, 10000])
  const [selectedSources, setSelectedSources] = useState<string[]>([])
  const [selectedDestinations, setSelectedDestinations] = useState<string[]>([])
  const [showFilters, setShowFilters] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  // Update filtered flights when MeTTa flights change
  useEffect(() => {
    setFilteredFlights(mettaFlights)
    if (mettaFlights.length > 0) {
      console.log('Updated flights with airline data:', mettaFlights)
    }
  }, [mettaFlights])

  const handleSearch = async (searchData: any) => {
    setHasSearched(true)
    
    // Extract search parameters from the search data
    const year = searchData.departDate?.getFullYear()
    const month = searchData.departDate ? searchData.departDate.getMonth() + 1 : undefined
    const day = searchData.departDate?.getDate()
    
    const searchParams = {
      source: searchData.from || undefined,
      destination: searchData.to || undefined,
      year,
      month,
      day,
      priority,
      include_connections: includeConnections,
    }
    
    try {
      await searchFlights(searchParams)
    } catch (err) {
      console.error('Search error:', err)
    }
  }

  // Get unique sources and destinations for filters
  const uniqueSources = [...new Set(mettaFlights.map(f => f.source))].sort()
  const uniqueDestinations = [...new Set(mettaFlights.map(f => f.destination))].sort()

  // Apply filters and sorting
  const sortedAndFilteredFlights = filteredFlights
    .filter(flight => {
      const cost = parseInt(flight.cost)
      const inPriceRange = cost >= priceRange[0] && cost <= priceRange[1]
      const sourceMatch = selectedSources.length === 0 || selectedSources.includes(flight.source)
      const destMatch = selectedDestinations.length === 0 || selectedDestinations.includes(flight.destination)
      return inPriceRange && sourceMatch && destMatch
    })

  const formatDate = (year: string, month: string, day: string) => {
    // Pad month and day with zeros if needed
    const paddedMonth = month.padStart(2, '0')
    const paddedDay = day.padStart(2, '0')
    const date = new Date(`${year}-${paddedMonth}-${paddedDay}`)
    
    // Check if the date is valid
    if (isNaN(date.getTime())) {
      return `${month}/${day}/${year}`
    }
    
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    })
  }

  const formatCost = (cost: string) => {
    return `$${parseInt(cost).toLocaleString()}`
  }

  const formatTime = (time: string) => {
    // Convert HHMM to HH:MM format
    const hour = time.slice(0, 2)
    const minute = time.slice(2, 4)
    return `${hour}:${minute}`
  }

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}h ${mins}m`
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Search Section */}
        <div className="mb-8">
          <FlightSearch onSearch={handleSearch} />
        </div>

        {/* Priority and Connection Options */}
        <div className="mb-6 flex flex-wrap gap-4 items-center">
          <div className="flex items-center space-x-2">
            <Label htmlFor="priority">Sort by:</Label>
            <Select value={priority} onValueChange={(value: "cost" | "time" | "optimized") => setPriority(value)}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="cost">Cost</SelectItem>
                <SelectItem value="time">Time</SelectItem>
                <SelectItem value="optimized">Optimized</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="flex items-center space-x-2">
            <Checkbox 
              id="connections" 
              checked={includeConnections} 
              onCheckedChange={(checked) => setIncludeConnections(checked as boolean)}
            />
            <Label htmlFor="connections">Include connecting flights</Label>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center">
                    <Filter className="mr-2 h-4 w-4" />
                    Filters
                  </CardTitle>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowFilters(!showFilters)}
                  >
                    {showFilters ? "Hide" : "Show"}
                  </Button>
                </div>
              </CardHeader>
              
              {showFilters && (
                <CardContent className="space-y-6">
                  {/* Price Range */}
                  <div>
                    <Label className="text-sm font-medium">
                      Price Range: ${priceRange[0]} - ${priceRange[1]}
                    </Label>
                    <Slider
                      value={priceRange}
                      onValueChange={setPriceRange}
                      max={10000}
                      min={0}
                      step={100}
                      className="mt-2"
                    />
                  </div>

                  {/* Source Airports */}
                  <div>
                    <Label className="text-sm font-medium">Source Airports</Label>
                    <div className="mt-2 space-y-2 max-h-32 overflow-y-auto">
                      {uniqueSources.map((source) => (
                        <div key={source} className="flex items-center space-x-2">
                          <Checkbox
                            id={`source-${source}`}
                            checked={selectedSources.includes(source)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                setSelectedSources([...selectedSources, source])
                              } else {
                                setSelectedSources(selectedSources.filter(s => s !== source))
                              }
                            }}
                          />
                          <Label htmlFor={`source-${source}`} className="text-sm">
                            {source}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Destination Airports */}
                  <div>
                    <Label className="text-sm font-medium">Destination Airports</Label>
                    <div className="mt-2 space-y-2 max-h-32 overflow-y-auto">
                      {uniqueDestinations.map((dest) => (
                        <div key={dest} className="flex items-center space-x-2">
                          <Checkbox
                            id={`dest-${dest}`}
                            checked={selectedDestinations.includes(dest)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                setSelectedDestinations([...selectedDestinations, dest])
                              } else {
                                setSelectedDestinations(selectedDestinations.filter(d => d !== dest))
                              }
                            }}
                          />
                          <Label htmlFor={`dest-${dest}`} className="text-sm">
                            {dest}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              )}
            </Card>
          </div>

          {/* Flight Results */}
          <div className="lg:col-span-3">
            {loading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin mr-2" />
                <span>Searching flights...</span>
              </div>
            )}

            {error && (
              <Card className="border-destructive">
                <CardContent className="pt-6">
                  <div className="text-destructive text-center">
                    <p className="font-medium">Search Error</p>
                    <p className="text-sm">{error}</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {!loading && !error && sortedAndFilteredFlights.length === 0 && hasSearched && (
              <Card>
                <CardContent className="pt-6">
                  <div className="text-center text-muted-foreground">
                    <Plane className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p className="font-medium">No flights found</p>
                    <p className="text-sm">Try adjusting your search criteria or filters.</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {!loading && !error && sortedAndFilteredFlights.length > 0 && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold">
                    {sortedAndFilteredFlights.length} flights found
                  </h2>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => getAllFlights(priority)}
                  >
                    Show All Flights
                  </Button>
                </div>

                {sortedAndFilteredFlights.map((flight, index) => (
                  <Card key={index} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between">
                        {/* Flight Info */}
                        <div className="flex-1">
                          <div className="flex items-center space-x-4 mb-4">
                            {/* Airline Logo */}
                            {flight.airline?.logo && (
                              <img 
                                src={flight.airline.logo} 
                                alt={flight.airline.name}
                                className="h-8 w-8 object-contain"
                                onError={(e) => {
                                  e.currentTarget.style.display = 'none'
                                }}
                              />
                            )}
                            
                            {/* Route */}
                            <div className="flex items-center space-x-2">
                              <span className="font-semibold text-lg">{flight.source}</span>
                              <ArrowLeftRight className="h-4 w-4 text-muted-foreground" />
                              <span className="font-semibold text-lg">{flight.destination}</span>
                            </div>

                            {/* Connection Badge */}
                            {flight.is_connecting && (
                              <Badge variant="secondary" className="ml-2">
                                <Plane className="h-3 w-3 mr-1" />
                                Connecting
                              </Badge>
                            )}
                          </div>

                          {/* Flight Details */}
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                            <div>
                              <p className="text-muted-foreground">Date</p>
                              <p className="font-medium">{formatDate(flight.year, flight.month, flight.day)}</p>
                            </div>
                            <div>
                              <p className="text-muted-foreground">Time</p>
                              <p className="font-medium">
                                {formatTime(flight.takeoff)} - {formatTime(flight.landing)}
                              </p>
                            </div>
                            <div>
                              <p className="text-muted-foreground">Duration</p>
                              <p className="font-medium flex items-center">
                                <Clock className="h-3 w-3 mr-1" />
                                {formatDuration(flight.duration)}
                              </p>
                            </div>
                            <div>
                              <p className="text-muted-foreground">Price</p>
                              <p className="font-medium text-lg text-green-600">
                                {formatCost(flight.cost)}
                              </p>
                            </div>
                          </div>

                          {/* Connection Details */}
                          {flight.is_connecting && flight.connection_airport && (
                            <div className="mt-3 p-3 bg-muted rounded-lg">
                              <p className="text-sm text-muted-foreground">
                                Connection at {flight.connection_airport}
                                {flight.layover_hours && ` (${flight.layover_hours.toFixed(1)}h layover)`}
                              </p>
                            </div>
                          )}

                          {/* Airline Info */}
                          {flight.airline && (
                            <div className="mt-3 flex items-center space-x-2">
                              <span className="text-sm text-muted-foreground">Operated by</span>
                              <span className="text-sm font-medium">{flight.airline.name}</span>
                            </div>
                          )}
                        </div>

                        {/* Action Buttons */}
                        <div className="flex flex-col space-y-2 ml-4">
                          <Button size="sm">
                            <DollarSign className="h-4 w-4 mr-1" />
                            Book Now
                          </Button>
                          <Button variant="outline" size="sm">
                            <Heart className="h-4 w-4 mr-1" />
                            Save
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
