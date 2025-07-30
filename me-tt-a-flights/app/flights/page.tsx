"use client"

import { useState, useEffect } from "react"
import { useSearchParams, useRouter } from "next/navigation"
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
import { Plane, Filter, Calendar, MapPin, DollarSign, Star, Heart, Loader2, ArrowLeftRight, Clock, Zap, Search } from "lucide-react"
import { useFlightSearch } from "@/hooks/use-flight-search"
import { useAuth } from "@/components/auth-provider"
import { useToast } from "@/hooks/use-toast"
import { Flight } from "@/lib/api"
import { getAirportLocation } from "@/lib/airports"

// Add skeleton component for loading states
const FlightCardSkeleton = () => (
  <Card className="animate-pulse">
    <CardContent className="p-6">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-4 mb-4">
            <div className="h-8 w-8 bg-muted rounded"></div>
            <div className="flex items-center space-x-2">
              <div className="h-6 w-12 bg-muted rounded"></div>
              <ArrowLeftRight className="h-4 w-4 text-muted-foreground" />
              <div className="h-6 w-12 bg-muted rounded"></div>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i}>
                <div className="h-4 w-16 bg-muted rounded mb-1"></div>
                <div className="h-5 w-20 bg-muted rounded"></div>
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-col space-y-2 ml-4">
          <div className="h-8 w-24 bg-muted rounded"></div>
          <div className="h-8 w-20 bg-muted rounded"></div>
        </div>
      </div>
    </CardContent>
  </Card>
)

export default function FlightsPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const { flights: mettaFlights, loading, error, getAllFlights, searchFlights } = useFlightSearch()
  const { user } = useAuth()
  const { toast } = useToast()
  const [filteredFlights, setFilteredFlights] = useState<Flight[]>([])
  const [priority, setPriority] = useState<"cost" | "time" | "optimized">("cost")
  const [includeConnections, setIncludeConnections] = useState(true)
  const [priceRange, setPriceRange] = useState([0, 50000])
  const [selectedSources, setSelectedSources] = useState<string[]>([])
  const [selectedDestinations, setSelectedDestinations] = useState<string[]>([])
  const [selectedAirlines, setSelectedAirlines] = useState<string[]>([])
  const [durationRange, setDurationRange] = useState([0, 1440]) // 0 to 24 hours in minutes
  const [showFilters, setShowFilters] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)
  const [recentSearches, setRecentSearches] = useState<Array<{from: string, to: string, date: string}>>([])
  const [selectedForComparison, setSelectedForComparison] = useState<Flight[]>([])
  const [searchStats, setSearchStats] = useState<{
    totalSearches: number
    averageResults: number
    lastSearchTime?: number
  }>({ totalSearches: 0, averageResults: 0 })

  // Get initial values from URL parameters
  const initialFrom = searchParams.get('from') || undefined
  const initialTo = searchParams.get('to') || undefined
  const initialDateStr = searchParams.get('date')
  const initialDate = initialDateStr ? new Date(initialDateStr) : undefined

  // Load recent searches from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('recentSearches')
    if (saved) {
      try {
        setRecentSearches(JSON.parse(saved))
      } catch (e) {
        console.error('Error loading recent searches:', e)
      }
    }
  }, [])

  // Load search stats from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('searchStats')
    if (saved) {
      try {
        setSearchStats(JSON.parse(saved))
      } catch (e) {
        console.error('Error loading search stats:', e)
      }
    }
  }, [])

  // Update search stats
  const updateSearchStats = (resultsCount: number) => {
    const newStats = {
      totalSearches: searchStats.totalSearches + 1,
      averageResults: Math.round((searchStats.averageResults * searchStats.totalSearches + resultsCount) / (searchStats.totalSearches + 1)),
      lastSearchTime: Date.now()
    }
    setSearchStats(newStats)
    localStorage.setItem('searchStats', JSON.stringify(newStats))
  }

  // Save search to recent searches
  const saveToRecentSearches = (searchData: any) => {
    const newSearch = {
      from: searchData.from,
      to: searchData.to,
      date: searchData.departDate?.toISOString().split('T')[0] || ''
    }
    
    const updated = [newSearch, ...recentSearches.filter(s => 
      !(s.from === newSearch.from && s.to === newSearch.to && s.date === newSearch.date)
    )].slice(0, 5)
    
    setRecentSearches(updated)
    localStorage.setItem('recentSearches', JSON.stringify(updated))
  }

  // Handle URL parameters on page load
  useEffect(() => {
    const from = searchParams.get('from')
    const to = searchParams.get('to')
    const date = searchParams.get('date')
    
    if (from || to || date) {
      // Parse the date if provided
      let departDate: Date | undefined
      if (date) {
        departDate = new Date(date)
        // Check if the date is valid
        if (isNaN(departDate.getTime())) {
          departDate = undefined
        }
      }
      
      const searchData = {
        from: from || '',
        to: to || '',
        departDate,
      }
      
      handleSearch(searchData)
    }
  }, [searchParams])

  // Update filtered flights when MeTTa flights change
  useEffect(() => {
    setFilteredFlights(mettaFlights)
    if (mettaFlights.length > 0) {
      console.log(`Loaded ${mettaFlights.length} flights`)
    }
  }, [mettaFlights])

  const handleSearch = async (searchData: any) => {
    setHasSearched(true)
    saveToRecentSearches(searchData)
    
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
      // Update stats after successful search
      if (mettaFlights.length > 0) {
        updateSearchStats(mettaFlights.length)
      }
    } catch (err) {
      console.error('Search error:', err)
    }
  }

  const resetFilters = () => {
    setPriceRange([0, 50000])
    setSelectedSources([])
    setSelectedDestinations([])
    setSelectedAirlines([])
    setDurationRange([0, 1440])
  }

  const handleBookNow = (flight: Flight) => {
    if (!user) {
      toast({
        title: "Authentication required",
        description: "Please log in to book a flight.",
        variant: "destructive",
      })
      router.push('/login')
      return
    }
    
    // Store flight data in localStorage for the booking page
    localStorage.setItem('selectedFlight', JSON.stringify(flight))
    // Navigate to booking page
    router.push('/booking/new')
  }

  const handleCompareFlights = () => {
    if (selectedForComparison.length < 2) {
      toast({
        title: "Select flights to compare",
        description: "Please select at least 2 flights to compare.",
        variant: "destructive",
      })
      return
    }
    
    // Store comparison data and navigate to comparison page
    localStorage.setItem('flightComparison', JSON.stringify(selectedForComparison))
    router.push('/flights/compare')
  }

  const toggleFlightComparison = (flight: Flight) => {
    const isSelected = selectedForComparison.some(f => 
      f.source === flight.source && 
      f.destination === flight.destination && 
      f.takeoff === flight.takeoff &&
      f.cost === flight.cost
    )
    
    if (isSelected) {
      setSelectedForComparison(selectedForComparison.filter(f => 
        !(f.source === flight.source && 
          f.destination === flight.destination && 
          f.takeoff === flight.takeoff &&
          f.cost === flight.cost)
      ))
    } else {
      if (selectedForComparison.length >= 3) {
        toast({
          title: "Maximum flights reached",
          description: "You can compare up to 3 flights at a time.",
          variant: "destructive",
        })
        return
      }
      setSelectedForComparison([...selectedForComparison, flight])
    }
  }

  // Get unique sources and destinations for filters
  const uniqueSources = [...new Set(mettaFlights.map(f => f.source))].sort()
  const uniqueDestinations = [...new Set(mettaFlights.map(f => f.destination))].sort()
  const uniqueAirlines = [...new Set(mettaFlights.map(f => f.airline?.name).filter((name): name is string => Boolean(name)))].sort()

  // Apply filters and sorting
  const sortedAndFilteredFlights = filteredFlights
    .filter(flight => {
      const cost = parseInt(flight.cost)
      const inPriceRange = cost >= priceRange[0] && cost <= priceRange[1]
      const sourceMatch = selectedSources.length === 0 || selectedSources.includes(flight.source)
      const destMatch = selectedDestinations.length === 0 || selectedDestinations.includes(flight.destination)
      const airlineMatch = selectedAirlines.length === 0 || (flight.airline?.name && selectedAirlines.includes(flight.airline.name))
      const durationMatch = flight.duration >= durationRange[0] && flight.duration <= durationRange[1]
      return inPriceRange && sourceMatch && destMatch && airlineMatch && durationMatch
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
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Background Images */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {/* Top Left - Airport Terminal */}
        <div className="absolute top-0 left-0 w-80 h-80 opacity-30 animate-float-slow">
          <div className="w-full h-full bg-gradient-to-br from-blue-500 to-purple-700 rounded-full blur-2xl transform -translate-x-1/2 -translate-y-1/2 animate-pulse-slow bg-glow"></div>
        </div>
        
        {/* Top Right - Plane Taking Off */}
        <div className="absolute top-0 right-0 w-96 h-96 opacity-25 animate-float-medium">
          <div className="w-full h-full bg-gradient-to-bl from-pink-500 to-orange-600 rounded-full blur-2xl transform translate-x-1/2 -translate-y-1/2 animate-pulse-slow bg-glow-pink"></div>
        </div>
        
        {/* Bottom Left - Plane in Flight */}
        <div className="absolute bottom-0 left-0 w-88 h-88 opacity-35 animate-float-fast">
          <div className="w-full h-full bg-gradient-to-tr from-green-500 to-blue-600 rounded-full blur-2xl transform -translate-x-1/2 translate-y-1/2 animate-pulse-slow bg-glow-green"></div>
        </div>
        
        {/* Bottom Right - Airport Runway */}
        <div className="absolute bottom-0 right-0 w-112 h-112 opacity-20 animate-float-slow">
          <div className="w-full h-full bg-gradient-to-tl from-purple-600 to-pink-700 rounded-full blur-2xl transform translate-x-1/2 translate-y-1/2 animate-pulse-slow bg-glow-purple"></div>
        </div>
        
        {/* Additional Medium Orbs */}
        <div className="absolute top-1/3 left-1/4 w-48 h-48 opacity-20 animate-float-medium">
          <div className="w-full h-full bg-gradient-to-r from-cyan-400 to-blue-500 rounded-full blur-xl"></div>
        </div>
        <div className="absolute bottom-1/3 right-1/4 w-56 h-56 opacity-15 animate-float-fast">
          <div className="w-full h-full bg-gradient-to-l from-pink-400 to-purple-500 rounded-full blur-xl"></div>
        </div>
        
        {/* Floating Plane Icons */}
        <div className="absolute top-24 left-24 opacity-20 animate-float-medium">
          <Plane className="w-20 h-20 text-blue-600 transform rotate-45 drop-shadow-lg" />
        </div>
        <div className="absolute top-40 right-40 opacity-15 animate-float-fast">
          <Plane className="w-16 h-16 text-pink-600 transform -rotate-12 drop-shadow-lg" />
        </div>
        <div className="absolute bottom-40 left-40 opacity-25 animate-float-slow">
          <Plane className="w-18 h-18 text-green-600 transform rotate-90 drop-shadow-lg" />
        </div>
        <div className="absolute bottom-24 right-24 opacity-20 animate-float-medium">
          <Plane className="w-14 h-14 text-purple-600 transform -rotate-45 drop-shadow-lg" />
        </div>
        
        {/* Additional Small Planes */}
        <div className="absolute top-1/2 left-16 opacity-15 animate-float-fast">
          <Plane className="w-12 h-12 text-cyan-500 transform rotate-30 drop-shadow-md" />
        </div>
        <div className="absolute bottom-1/2 right-16 opacity-15 animate-float-medium">
          <Plane className="w-10 h-10 text-orange-500 transform -rotate-60 drop-shadow-md" />
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        <Navigation />

        <div className="container mx-auto px-4 py-8">
          {/* Authentication Notice */}
          {!user && (
            <Card className="mb-6 border-blue-200 glass-card">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Plane className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="font-medium text-blue-900">Login to Book Flights</p>
                      <p className="text-sm text-blue-700">Sign in to your account to book flights and save your preferences.</p>
                    </div>
                  </div>
                  <Button 
                    size="sm" 
                    onClick={() => router.push('/login')}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    Sign In
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Search Section */}
          <div className="mb-8">
            <FlightSearch 
              onSearch={handleSearch} 
              initialFrom={initialFrom}
              initialTo={initialTo}
              initialDate={initialDate}
            />
            
            {/* Recent Searches */}
            {recentSearches.length > 0 && !hasSearched && (
              <Card className="mt-4 glass-card">
                <CardContent className="pt-6">
                  <div className="flex items-center space-x-2 mb-3">
                    <Clock className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm font-medium">Recent Searches</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {recentSearches.map((search, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          const searchData = {
                            from: search.from,
                            to: search.to,
                            departDate: search.date ? new Date(search.date) : undefined
                          }
                          handleSearch(searchData)
                        }}
                        className="text-xs"
                      >
                        {search.from} → {search.to}
                        {search.date && ` (${new Date(search.date).toLocaleDateString()})`}
                      </Button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
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
               <Card className="sticky top-4 glass-card">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center">
                      <Filter className="mr-2 h-4 w-4" />
                      Filters
                    </CardTitle>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={resetFilters}
                      >
                        Reset
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setShowFilters(!showFilters)}
                      >
                        {showFilters ? "Hide" : "Show"}
                      </Button>
                    </div>
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
                        max={50000}
                        min={0}
                        step={100}
                        className="mt-2"
                      />
                    </div>

                    {/* Duration Range */}
                    <div>
                      <Label className="text-sm font-medium">
                        Duration: {Math.floor(durationRange[0]/60)}h {durationRange[0]%60}m - {Math.floor(durationRange[1]/60)}h {durationRange[1]%60}m
                      </Label>
                      <Slider
                        value={durationRange}
                        onValueChange={setDurationRange}
                        max={1440}
                        min={0}
                        step={30}
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

                    {/* Airlines */}
                    <div>
                      <Label className="text-sm font-medium">Airlines</Label>
                      <div className="mt-2 space-y-2 max-h-32 overflow-y-auto">
                        {uniqueAirlines.map((airline) => (
                          <div key={airline} className="flex items-center space-x-2">
                            <Checkbox
                              id={`airline-${airline}`}
                              checked={selectedAirlines.includes(airline)}
                              onCheckedChange={(checked) => {
                                if (checked) {
                                  setSelectedAirlines([...selectedAirlines, airline])
                                } else {
                                  setSelectedAirlines(selectedAirlines.filter(a => a !== airline))
                                }
                              }}
                            />
                            <Label htmlFor={`airline-${airline}`} className="text-sm">
                              {airline}
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
                <div className="space-y-4">
                  <div className="flex items-center justify-center py-4">
                    <Loader2 className="h-6 w-6 animate-spin mr-2" />
                    <span>Searching flights...</span>
                  </div>
                  {[...Array(3)].map((_, i) => (
                    <FlightCardSkeleton key={i} />
                  ))}
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
                      <p className="text-sm mb-4">Try adjusting your search criteria or filters.</p>
                      
                      <div className="flex flex-col sm:flex-row gap-2 justify-center">
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => {
                            resetFilters()
                            setHasSearched(false)
                          }}
                        >
                          Clear Filters
                        </Button>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => getAllFlights(priority)}
                        >
                          Show All Flights
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {!loading && !error && !hasSearched && (
                <Card>
                  <CardContent className="pt-6">
                    <div className="text-center text-muted-foreground">
                      <Search className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p className="font-medium">Ready to search flights</p>
                      <p className="text-sm">Enter your travel details above to find available flights.</p>
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
                    <div className="flex items-center space-x-2">
                      {searchStats.totalSearches > 0 && (
                        <div className="text-xs text-muted-foreground hidden md:block">
                          Avg: {searchStats.averageResults} results
                        </div>
                      )}
                      {selectedForComparison.length > 0 && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={handleCompareFlights}
                          className="bg-blue-50 border-blue-200 text-blue-700 hover:bg-blue-100"
                        >
                          Compare ({selectedForComparison.length})
                        </Button>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => getAllFlights(priority)}
                      >
                        Show All Flights
                      </Button>
                    </div>
                  </div>

                                     {sortedAndFilteredFlights.map((flight, index) => (
                     <Card key={index} className="hover:shadow-md transition-shadow group glass-card">
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

                              {/* Price Badge */}
                              <Badge variant="outline" className="ml-auto">
                                <DollarSign className="h-3 w-3 mr-1" />
                                {formatCost(flight.cost)}
                              </Badge>
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
                                {flight.airline.description && (
                                  <span className="text-xs text-muted-foreground">• {flight.airline.description}</span>
                                )}
                              </div>
                            )}

                            {/* Flight Segments for Connecting Flights */}
                            {flight.is_connecting && flight.segments && flight.segments.length > 0 && (
                              <div className="mt-3 space-y-2">
                                <p className="text-sm font-medium text-muted-foreground">Flight Segments:</p>
                                {flight.segments.map((segment, segIndex) => (
                                  <div key={segIndex} className="flex items-center space-x-2 text-xs bg-muted/50 p-2 rounded">
                                    <span className="font-medium">{segment.source} → {segment.destination}</span>
                                    <span className="text-muted-foreground">
                                      {formatTime(segment.takeoff)}-{formatTime(segment.landing)}
                                    </span>
                                    <span className="text-muted-foreground">
                                      ({formatDuration(segment.duration)})
                                    </span>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>

                          {/* Action Buttons */}
                          <div className="flex flex-col space-y-2 ml-4">
                            <Button 
                              size="sm" 
                              onClick={() => handleBookNow(flight)}
                              variant={user ? "default" : "secondary"}
                              className={user ? "" : "border-dashed"}
                            >
                              <DollarSign className="h-4 w-4 mr-1" />
                              {user ? "Book Now" : "Login to Book"}
                            </Button>
                            <Button variant="outline" size="sm">
                              <Heart className="h-4 w-4 mr-1" />
                              Save
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm" 
                              className="opacity-0 group-hover:opacity-100 transition-opacity"
                              onClick={() => toggleFlightComparison(flight)}
                            >
                              {selectedForComparison.some(f => 
                                f.source === flight.source && 
                                f.destination === flight.destination && 
                                f.takeoff === flight.takeoff &&
                                f.cost === flight.cost
                              ) ? (
                                <>
                                  <Star className="h-4 w-4 mr-1 fill-yellow-400 text-yellow-400" />
                                  Selected
                                </>
                              ) : (
                                <>
                                  <Star className="h-4 w-4 mr-1" />
                                  Compare
                                </>
                              )}
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
    </div>
  )
}
