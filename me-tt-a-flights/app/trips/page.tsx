"use client"

import { useState, useEffect } from "react"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { useAuth } from "@/components/auth-provider"
import { bookingsApiService } from "@/lib/bookings-api"
import { Booking } from "@/lib/bookings"
import { Plane, Calendar, MapPin, Clock, Download, Share, AlertCircle, CheckCircle, XCircle, Trash2, Settings, Globe, Compass, Map } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

export default function TripsPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [activeTab, setActiveTab] = useState("upcoming")
  const [bookings, setBookings] = useState<Booking[]>([])
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()
  const router = useRouter()
  const { toast } = useToast()

  // Load user bookings
  useEffect(() => {
    const loadBookings = async () => {
      if (user) {
        setLoading(true)
        try {
          const userBookings = await bookingsApiService.getUserBookings()
          setBookings(userBookings)
        } catch (error) {
          console.error('Error loading bookings:', error)
        } finally {
          setLoading(false)
        }
      } else {
        setLoading(false)
      }
    }
    
    loadBookings()
  }, [user])

  // Refresh bookings when component mounts (useful after booking completion)
  useEffect(() => {
    const refreshBookings = async () => {
      if (user) {
        try {
          const userBookings = await bookingsApiService.getUserBookings()
          setBookings(userBookings)
        } catch (error) {
          console.error('Error refreshing bookings:', error)
        }
      }
    }

    // Refresh on mount
    refreshBookings()
  }, [user])

  if (!user) {
    return (
      <div className="min-h-screen bg-background relative overflow-hidden">
        {/* Background for non-authenticated state */}
        <div className="fixed inset-0 pointer-events-none z-0">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 opacity-20"></div>
        </div>
        
        <div className="relative z-10">
          <Navigation />
          <div className="container mx-auto px-4 py-20">
            <Card className="max-w-md mx-auto text-center glass-card">
              <CardContent className="p-8">
                <Plane className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                <h2 className="text-2xl font-bold mb-4">Sign In Required</h2>
                <p className="text-muted-foreground mb-6">Please sign in to view your trips and bookings.</p>
                <Button asChild className="flight-gradient text-white">
                  <Link href="/login">Sign In</Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "confirmed":
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case "cancelled":
        return <XCircle className="h-4 w-4 text-red-600" />
      case "completed":
        return <CheckCircle className="h-4 w-4 text-blue-600" />
      default:
        return <AlertCircle className="h-4 w-4 text-yellow-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "confirmed":
        return "bg-green-100 text-green-800"
      case "cancelled":
        return "bg-red-100 text-red-800"
      case "completed":
        return "bg-blue-100 text-blue-800"
      default:
        return "bg-yellow-100 text-yellow-800"
    }
  }

  const handleRemoveBooking = async (bookingId: string) => {
    try {
      const success = await bookingsApiService.deleteBooking(bookingId)
      if (success) {
        setBookings(bookings.filter(booking => booking.id !== bookingId))
        toast({
          title: "Booking removed",
          description: "Your booking has been removed successfully.",
        })
      } else {
        throw new Error('Failed to delete booking')
      }
    } catch (error) {
      toast({
        title: "Error removing booking",
        description: "Failed to remove booking. Please try again.",
        variant: "destructive",
      })
    }
  }

  const handleManageBooking = (bookingId: string) => {
    router.push(`/booking/manage/${bookingId}`)
  }

  const filteredTrips = bookings.filter((booking) => {
    const matchesSearch =
      booking.bookingRef.toLowerCase().includes(searchTerm.toLowerCase()) ||
      booking.flight.source.toLowerCase().includes(searchTerm.toLowerCase()) ||
      booking.flight.destination.toLowerCase().includes(searchTerm.toLowerCase()) ||
      booking.flight.airline?.name.toLowerCase().includes(searchTerm.toLowerCase())

    if (activeTab === "upcoming") {
      return matchesSearch && booking.status === "confirmed"
    } else if (activeTab === "completed") {
      return matchesSearch && booking.status === "completed"
    } else {
      return matchesSearch && booking.status === "cancelled"
    }
  })

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* HD Background Images and 3D Animations */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {/* World Map Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-sky-400 via-blue-500 to-indigo-600 opacity-10"></div>
        
        {/* Travel-themed background patterns */}
        <div className="absolute top-0 left-0 w-full h-full opacity-20">
          <div className="w-full h-full bg-gradient-to-br from-white/5 to-transparent"></div>
        </div>
        
        {/* Floating 3D Elements */}
        <div className="absolute top-20 left-20 opacity-20 animate-3d-float">
          <Globe className="w-24 h-24 text-blue-600 drop-shadow-2xl transform rotate-12" />
        </div>
        
        <div className="absolute top-40 right-40 opacity-15 animate-3d-rotate">
          <Compass className="w-20 h-20 text-green-600 drop-shadow-2xl transform -rotate-45" />
        </div>
        
        <div className="absolute bottom-40 left-40 opacity-25 animate-3d-scale">
          <Map className="w-28 h-28 text-purple-600 drop-shadow-2xl transform rotate-90" />
        </div>
        
        <div className="absolute bottom-20 right-20 opacity-20 animate-3d-float">
          <Plane className="w-32 h-32 text-orange-500 drop-shadow-2xl transform -rotate-30" />
        </div>
        
        {/* Additional 3D Plane Elements */}
        <div className="absolute top-1/3 left-1/3 opacity-15 animate-3d-rotate">
          <Plane className="w-16 h-16 text-cyan-500 drop-shadow-lg transform rotate-60" />
        </div>
        
        <div className="absolute bottom-1/3 right-1/3 opacity-15 animate-3d-scale">
          <Plane className="w-12 h-12 text-pink-500 drop-shadow-lg transform -rotate-75" />
        </div>
        
        {/* Gradient Orbs for Depth */}
        <div className="absolute top-0 left-0 w-96 h-96 opacity-15 animate-float-slow">
          <div className="w-full h-full bg-gradient-to-br from-blue-500 to-purple-700 rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2 animate-pulse-slow bg-glow"></div>
        </div>
        
        <div className="absolute bottom-0 right-0 w-80 h-80 opacity-20 animate-float-medium">
          <div className="w-full h-full bg-gradient-to-tl from-green-500 to-blue-600 rounded-full blur-3xl transform translate-x-1/2 translate-y-1/2 animate-pulse-slow bg-glow-green"></div>
        </div>
        
        <div className="absolute top-1/2 left-0 w-64 h-64 opacity-10 animate-float-fast">
          <div className="w-full h-full bg-gradient-to-r from-pink-500 to-orange-600 rounded-full blur-2xl transform -translate-x-1/2 -translate-y-1/2"></div>
        </div>
        
        {/* Travel Route Lines */}
        <div className="absolute top-1/4 left-1/4 w-1/2 h-1/2 opacity-5">
          <div className="w-full h-full border border-white/10 rounded-full"></div>
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        <Navigation />

        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              My Trips
            </h1>
            <p className="text-muted-foreground text-lg">
              Manage your bookings, check flight status, and access your travel documents.
            </p>
          </div>

          {/* Search */}
          <div className="mb-6">
            <Input
              placeholder="Search by booking reference, destination, or airline..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-md glass-card border-0"
            />
          </div>

          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 max-w-md glass-card">
              <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
              <TabsTrigger value="completed">Completed</TabsTrigger>
              <TabsTrigger value="cancelled">Cancelled</TabsTrigger>
            </TabsList>

            <TabsContent value={activeTab} className="mt-6">
              {loading ? (
                <Card className="text-center py-12 glass-card">
                  <CardContent>
                    <Plane className="h-16 w-16 mx-auto mb-4 text-muted-foreground animate-bounce" />
                    <h3 className="text-xl font-semibold mb-2">Loading trips...</h3>
                    <p className="text-muted-foreground mb-6">Please wait while we fetch your bookings.</p>
                  </CardContent>
                </Card>
              ) : filteredTrips.length === 0 ? (
                <Card className="text-center py-12 glass-card">
                  <CardContent>
                    <Plane className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                    <h3 className="text-xl font-semibold mb-2">No trips found</h3>
                    <p className="text-muted-foreground mb-6">
                      {activeTab === "upcoming"
                        ? "You don't have any upcoming trips. Ready to plan your next adventure?"
                        : `No ${activeTab} trips found.`}
                    </p>
                    {activeTab === "upcoming" && (
                      <Button asChild className="flight-gradient text-white">
                        <Link href="/flights">Search Flights</Link>
                      </Button>
                    )}
                  </CardContent>
                </Card>
              ) : (
                <div className="space-y-6">
                  {filteredTrips.map((booking, index) => {
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

                    const formatDate = (year: string, month: string, day: string) => {
                      const paddedMonth = month.padStart(2, '0')
                      const paddedDay = day.padStart(2, '0')
                      const date = new Date(`${year}-${paddedMonth}-${paddedDay}`)
                      return date.toLocaleDateString()
                    }

                    return (
                      <Card 
                        key={booking.id} 
                        className="hover:shadow-2xl transition-all duration-300 glass-card-trips transform hover:scale-[1.02] hover:-translate-y-1 animate-card-enter"
                        style={{ animationDelay: `${index * 150}ms` }}
                      >
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className="flex items-center space-x-2">
                                {getStatusIcon(booking.status)}
                                <Badge className={getStatusColor(booking.status)}>
                                  {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                                </Badge>
                              </div>
                              <div>
                                <CardTitle className="text-lg">{booking.flight.airline?.name || 'Flight'}</CardTitle>
                                <p className="text-sm text-muted-foreground">Booking Ref: {booking.bookingRef}</p>
                              </div>
                            </div>
                            <div className="flex space-x-2">
                              <Button variant="outline" size="sm" className="glass-card">
                                <Download className="h-4 w-4 mr-1" />
                                Download
                              </Button>
                              <Button variant="outline" size="sm" className="glass-card">
                                <Share className="h-4 w-4 mr-1" />
                                Share
                              </Button>
                              <AlertDialog>
                                <AlertDialogTrigger asChild>
                                  <Button variant="outline" size="sm" className="glass-card">
                                    <Trash2 className="h-4 w-4 mr-1" />
                                    Remove
                                  </Button>
                                </AlertDialogTrigger>
                                <AlertDialogContent className="glass-card">
                                  <AlertDialogHeader>
                                    <AlertDialogTitle>Remove Booking</AlertDialogTitle>
                                    <AlertDialogDescription>
                                      Are you sure you want to remove this booking? This action cannot be undone.
                                    </AlertDialogDescription>
                                  </AlertDialogHeader>
                                  <AlertDialogFooter>
                                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                                    <AlertDialogAction 
                                      onClick={() => handleRemoveBooking(booking.id)}
                                      className="bg-red-600 hover:bg-red-700"
                                    >
                                      Remove
                                    </AlertDialogAction>
                                  </AlertDialogFooter>
                                </AlertDialogContent>
                              </AlertDialog>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {/* Flight Route */}
                            <div className="md:col-span-2">
                              <div className="flex items-center justify-between mb-4">
                                <div className="text-center">
                                  <p className="text-2xl font-bold">{formatTime(booking.flight.takeoff)}</p>
                                  <p className="text-sm font-medium">{booking.flight.source}</p>
                                  <p className="text-xs text-muted-foreground">Departure</p>
                                </div>

                                <div className="flex-1 mx-4">
                                  <div className="flex items-center justify-center space-x-2">
                                    <div className="flex-1 h-px bg-border"></div>
                                    <div className="text-center">
                                      <Plane className="h-4 w-4 text-muted-foreground mx-auto mb-1 animate-pulse" />
                                      <p className="text-xs text-muted-foreground">{formatDuration(booking.flight.duration)}</p>
                                      {booking.flight.is_connecting && (
                                        <p className="text-xs font-medium">Via {booking.flight.connection_airport}</p>
                                      )}
                                    </div>
                                    <div className="flex-1 h-px bg-border"></div>
                                  </div>
                                </div>

                                <div className="text-center">
                                  <p className="text-2xl font-bold">{formatTime(booking.flight.landing)}</p>
                                  <p className="text-sm font-medium">{booking.flight.destination}</p>
                                  <p className="text-xs text-muted-foreground">Arrival</p>
                                </div>
                              </div>

                              <div className="flex items-center justify-center space-x-4 text-sm text-muted-foreground">
                                <div className="flex items-center">
                                  <Calendar className="h-4 w-4 mr-1" />
                                  {formatDate(booking.flight.year, booking.flight.month, booking.flight.day)}
                                </div>
                                <div className="flex items-center">
                                  <MapPin className="h-4 w-4 mr-1" />
                                  {booking.passengerCount} Passenger{booking.passengerCount > 1 ? 's' : ''}
                                </div>
                                <div className="flex items-center">
                                  <Clock className="h-4 w-4 mr-1" />
                                  Economy
                                </div>
                              </div>
                            </div>

                            {/* Trip Details */}
                            <div className="space-y-4">
                              <div>
                                <p className="text-sm text-muted-foreground">Total Price</p>
                                <p className="text-2xl font-bold text-primary">${booking.totalCost.toLocaleString()}</p>
                              </div>

                              <div>
                                <p className="text-sm text-muted-foreground">Passengers</p>
                                <div className="space-y-1">
                                  {booking.passengers.map((passenger, index) => (
                                    <p key={index} className="text-sm font-medium">
                                      {passenger.firstName} {passenger.lastName}
                                    </p>
                                  ))}
                                </div>
                              </div>

                              {booking.status === "confirmed" && (
                                <div className="space-y-2">
                                  <Button variant="outline" className="w-full glass-card" size="sm">
                                    Check-in Online
                                  </Button>
                                  <Button 
                                    variant="outline" 
                                    className="w-full glass-card" 
                                    size="sm"
                                    onClick={() => handleManageBooking(booking.id)}
                                  >
                                    <Settings className="h-4 w-4 mr-1" />
                                    Manage Booking
                                  </Button>
                                </div>
                              )}
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    )
                  })}
                </div>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
