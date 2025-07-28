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
import { Plane, Filter, Calendar, MapPin, DollarSign, Star, Heart, Loader2, ArrowLeftRight } from "lucide-react"
import { useFlightSearch } from "@/hooks/use-flight-search"
import { Flight } from "@/lib/api"
import { getAirportLocation } from "@/lib/airports"

export default function FlightsPage() {
  const { flights: mettaFlights, loading, error, getAllFlights, searchFlights } = useFlightSearch()
  const [filteredFlights, setFilteredFlights] = useState<Flight[]>([])
  const [sortBy, setSortBy] = useState("cost")
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
    .sort((a, b) => {
      switch (sortBy) {
        case "cost":
          return parseInt(a.cost) - parseInt(b.cost)
        case "date":
          const dateA = new Date(`${a.year}-${a.month}-${a.day}`)
          const dateB = new Date(`${b.year}-${b.month}-${b.day}`)
          return dateA.getTime() - dateB.getTime()
        case "source":
          return a.source.localeCompare(b.source)
        case "destination":
          return a.destination.localeCompare(b.destination)
        default:
          return 0
      }
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
                    max={10000}
                    min={0}
                    step={100}
                    className="mb-2"
                  />
                  <div className="flex justify-between text-sm text-muted-foreground">
                    <span>${priceRange[0]}</span>
                    <span>${priceRange[1]}</span>
                  </div>
                </div>

                <Separator />

                {/* Source Airports */}
                <div>
                  <Label className="text-sm font-medium mb-3 block">Source Airports</Label>
                  <div className="space-y-2 max-h-40 overflow-y-auto">
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
                        <Label htmlFor={`source-${source}`} className="text-sm">{source}</Label>
                      </div>
                    ))}
                  </div>
                </div>

                <Separator />

                {/* Destination Airports */}
                <div>
                  <Label className="text-sm font-medium mb-3 block">Destination Airports</Label>
                  <div className="space-y-2 max-h-40 overflow-y-auto">
                    {uniqueDestinations.map((destination) => (
                      <div key={destination} className="flex items-center space-x-2">
                        <Checkbox
                          id={`dest-${destination}`}
                          checked={selectedDestinations.includes(destination)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedDestinations([...selectedDestinations, destination])
                            } else {
                              setSelectedDestinations(selectedDestinations.filter(d => d !== destination))
                            }
                          }}
                        />
                        <Label htmlFor={`dest-${destination}`} className="text-sm">{destination}</Label>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-3">
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold">Flight Results</h2>
                <p className="text-muted-foreground">
                  {!hasSearched ? "Nothing searched yet" : loading ? "Loading flights..." : mettaFlights.length > 0 ? `${sortedAndFilteredFlights.length} flights found` : "Search for flights to get started"}
                </p>
              </div>
              
              <div className="flex items-center space-x-4">
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="w-40">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="cost">Price: Low to High</SelectItem>
                    <SelectItem value="date">Date</SelectItem>
                    <SelectItem value="source">Source</SelectItem>
                    <SelectItem value="destination">Destination</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Loading State */}
            {hasSearched && loading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin mr-2" />
                <span>Loading flights...</span>
              </div>
            )}

            {/* Error State */}
            {error && (
              <Card className="border-destructive">
                <CardContent className="pt-6">
                  <div className="text-center text-destructive">
                    <p>Error loading flights: {error}</p>
                    <Button onClick={getAllFlights} className="mt-2">Try Again</Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* No Results */}
            {!hasSearched && !loading && !error && (
              <Card>
                <CardContent className="pt-6">
                  <div className="text-center">
                    <Plane className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                    <h3 className="text-lg font-semibold mb-2">Ready to search flights</h3>
                    <p className="text-muted-foreground mb-4">
                      Use the search form above to find flights from our comprehensive flight database.
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* No Search Results */}
            {hasSearched && !loading && !error && sortedAndFilteredFlights.length === 0 && (
              <Card>
                <CardContent className="pt-6">
                  <div className="text-center">
                    <Plane className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                    <h3 className="text-lg font-semibold mb-2">No flights found</h3>
                    <p className="text-muted-foreground mb-4">
                      Try adjusting your search criteria or filters.
                    </p>
                    <Button onClick={() => {
                      setSelectedSources([])
                      setSelectedDestinations([])
                      setPriceRange([0, 10000])
                    }}>
                      Clear Filters
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Flight Results */}
            {hasSearched && !loading && !error && sortedAndFilteredFlights.length > 0 && (
              <div className="space-y-4">
                {sortedAndFilteredFlights.map((flight, index) => (
                  <Card key={`${flight.source}-${flight.destination}-${flight.year}-${flight.month}-${flight.day}-${index}`} className="hover:shadow-md transition-shadow">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          {flight.airline ? (
                            <div className="flex items-center justify-center w-12 h-12 bg-white border rounded-lg overflow-hidden relative">
                              <img 
                                src={flight.airline.logo} 
                                alt={flight.airline.name}
                                className="w-full h-full object-contain p-1"
                                onError={(e) => {
                                  // Fallback to plane icon if image fails to load
                                  e.currentTarget.style.display = 'none';
                                  const fallback = e.currentTarget.parentElement?.querySelector('.fallback-icon');
                                  if (fallback) {
                                    fallback.classList.remove('hidden');
                                  }
                                }}
                              />
                              <Plane className="h-6 w-6 text-primary hidden fallback-icon absolute inset-0 m-auto" />
                            </div>
                          ) : (
                            <div className="flex items-center justify-center w-12 h-12 bg-primary/10 rounded-full">
                              <Plane className="h-6 w-6 text-primary" />
                            </div>
                          )}
                          
                          <div className="space-y-1">
                            <div className="flex items-center space-x-8">
                              <div className="flex items-center space-x-2">
                                <MapPin className="h-4 w-4 text-muted-foreground" />
                                <div>
                                  <span className="font-medium">{flight.source}</span>
                                  <div className="text-xs text-muted-foreground">
                                    {getAirportLocation(flight.source)}
                                  </div>
                                </div>
                              </div>
                              
                              {/* Arrow separator */}
                              <div className="flex items-center text-muted-foreground">
                                <ArrowLeftRight className="h-4 w-4" />
                              </div>
                              
                              <div className="flex items-center space-x-2">
                                <MapPin className="h-4 w-4 text-muted-foreground" />
                                <div>
                                  <span className="font-medium">{flight.destination}</span>
                                  <div className="text-xs text-muted-foreground">
                                    {getAirportLocation(flight.destination)}
                                  </div>
                                </div>
                              </div>
                            </div>
                            
                            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                              <div className="flex items-center space-x-1">
                                <Calendar className="h-4 w-4" />
                                <span>{formatDate(flight.year, flight.month, flight.day)}</span>
                              </div>
                              {flight.airline && (
                                <div className="flex items-center space-x-1">
                                  <span className="text-xs font-medium text-primary">{flight.airline.code}</span>
                                  <span>•</span>
                                  <span className="text-xs">{flight.airline.name}</span>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>

                        <div className="text-right">
                          <div className="text-2xl font-bold text-primary">
                            {formatCost(flight.cost)}
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {flight.airline ? flight.airline.name : 'MeTTa Flight'}
                          </div>
                        </div>
                      </div>

                      <div className="mt-4 flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Badge variant="secondary">Direct Flight</Badge>
                          {flight.airline && (
                            <Badge variant="outline" className="text-xs">
                              {flight.airline.code}
                            </Badge>
                          )}
                          <Badge variant="outline">MeTTa Data</Badge>
                        </div>
                        
                        <Button size="sm">
                          Select Flight
                        </Button>
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
