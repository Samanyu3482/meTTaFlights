"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ArrowLeft, Plane, Clock, DollarSign, Star, Check, X, ArrowLeftRight } from "lucide-react"
import { useAuth } from "@/components/auth-provider"
import { useToast } from "@/hooks/use-toast"
import { Flight } from "@/lib/api"

export default function FlightComparisonPage() {
  const router = useRouter()
  const { user } = useAuth()
  const { toast } = useToast()
  const [flights, setFlights] = useState<Flight[]>([])

  useEffect(() => {
    const comparisonData = localStorage.getItem('flightComparison')
    if (comparisonData) {
      try {
        const parsedFlights = JSON.parse(comparisonData)
        setFlights(parsedFlights)
      } catch (e) {
        console.error('Error parsing comparison data:', e)
        toast({
          title: "Error loading comparison",
          description: "Failed to load flight comparison data.",
          variant: "destructive",
        })
        router.push('/flights')
      }
    } else {
      router.push('/flights')
    }
  }, [router, toast])

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
    
    localStorage.setItem('selectedFlight', JSON.stringify(flight))
    router.push('/booking/new')
  }

  const formatDate = (year: string, month: string, day: string) => {
    const paddedMonth = month.padStart(2, '0')
    const paddedDay = day.padStart(2, '0')
    const date = new Date(`${year}-${paddedMonth}-${paddedDay}`)
    
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
    const hour = time.slice(0, 2)
    const minute = time.slice(2, 4)
    return `${hour}:${minute}`
  }

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}h ${mins}m`
  }

  const getBestValue = () => {
    if (flights.length === 0) return null
    return flights.reduce((best, current) => 
      parseInt(current.cost) < parseInt(best.cost) ? current : best
    )
  }

  const getFastest = () => {
    if (flights.length === 0) return null
    return flights.reduce((fastest, current) => 
      current.duration < fastest.duration ? current : fastest
    )
  }

  if (flights.length === 0) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <p>Loading comparison...</p>
          </div>
        </div>
      </div>
    )
  }

  const bestValue = getBestValue()
  const fastest = getFastest()

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Button 
            variant="ghost" 
            onClick={() => router.push('/flights')}
            className="mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Search
          </Button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Flight Comparison</h1>
              <p className="text-muted-foreground">
                Compare {flights.length} flights to find the best option
              </p>
            </div>
            
            <div className="flex items-center space-x-2">
              {bestValue && (
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  <DollarSign className="h-3 w-3 mr-1" />
                  Best Value: {formatCost(bestValue.cost)}
                </Badge>
              )}
              {fastest && (
                <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                  <Clock className="h-3 w-3 mr-1" />
                  Fastest: {formatDuration(fastest.duration)}
                </Badge>
              )}
            </div>
          </div>
        </div>

        {/* Comparison Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {flights.map((flight, index) => (
            <Card key={index} className="relative">
              {/* Best Value Badge */}
              {bestValue && flight === bestValue && (
                <div className="absolute -top-2 -right-2 z-10">
                  <Badge className="bg-green-500 text-white">
                    <DollarSign className="h-3 w-3 mr-1" />
                    Best Value
                  </Badge>
                </div>
              )}
              
              {/* Fastest Badge */}
              {fastest && flight === fastest && (
                <div className="absolute -top-2 -left-2 z-10">
                  <Badge className="bg-blue-500 text-white">
                    <Clock className="h-3 w-3 mr-1" />
                    Fastest
                  </Badge>
                </div>
              )}

              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {flight.airline?.logo && (
                      <img 
                        src={flight.airline.logo} 
                        alt={flight.airline.name}
                        className="h-6 w-6 object-contain"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none'
                        }}
                      />
                    )}
                    <span className="text-lg">{flight.source} → {flight.destination}</span>
                  </div>
                </CardTitle>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Route and Date */}
                <div className="text-center">
                  <p className="text-sm text-muted-foreground">Date</p>
                  <p className="font-medium">{formatDate(flight.year, flight.month, flight.day)}</p>
                </div>

                {/* Flight Times */}
                <div className="flex items-center justify-between">
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Departure</p>
                    <p className="font-semibold">{formatTime(flight.takeoff)}</p>
                    <p className="text-xs text-muted-foreground">{flight.source}</p>
                  </div>
                  
                  <div className="flex flex-col items-center">
                    <ArrowLeftRight className="h-4 w-4 text-muted-foreground mb-1" />
                    <p className="text-xs text-muted-foreground">
                      {formatDuration(flight.duration)}
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Arrival</p>
                    <p className="font-semibold">{formatTime(flight.landing)}</p>
                    <p className="text-xs text-muted-foreground">{flight.destination}</p>
                  </div>
                </div>

                <Separator />

                {/* Price */}
                <div className="text-center">
                  <p className="text-sm text-muted-foreground">Price</p>
                  <p className="text-2xl font-bold text-green-600">
                    {formatCost(flight.cost)}
                  </p>
                </div>

                {/* Airline Info */}
                {flight.airline && (
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Airline</p>
                    <p className="font-medium">{flight.airline.name}</p>
                  </div>
                )}

                {/* Connection Info */}
                {flight.is_connecting && (
                  <div className="text-center">
                    <Badge variant="outline">
                      <Plane className="h-3 w-3 mr-1" />
                      Connecting Flight
                    </Badge>
                    {flight.connection_airport && (
                      <p className="text-xs text-muted-foreground mt-1">
                        Via {flight.connection_airport}
                      </p>
                    )}
                  </div>
                )}

                {/* Action Buttons */}
                <div className="space-y-2">
                  <Button 
                    onClick={() => handleBookNow(flight)}
                    className="w-full"
                    variant={user ? "default" : "secondary"}
                  >
                    <DollarSign className="h-4 w-4 mr-2" />
                    {user ? "Book Now" : "Login to Book"}
                  </Button>
                  
                  <Button variant="outline" className="w-full">
                    <Star className="h-4 w-4 mr-2" />
                    Save for Later
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Summary */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Comparison Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Price Range</p>
                <p className="font-semibold">
                  {formatCost(Math.min(...flights.map(f => parseInt(f.cost)).toString()))} - {formatCost(Math.max(...flights.map(f => parseInt(f.cost)).toString()))}
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Duration Range</p>
                <p className="font-semibold">
                  {formatDuration(Math.min(...flights.map(f => f.duration)))} - {formatDuration(Math.max(...flights.map(f => f.duration)))}
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Airlines</p>
                <p className="font-semibold">
                  {new Set(flights.map(f => f.airline?.name).filter(Boolean)).size} different
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 