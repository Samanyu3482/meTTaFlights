"use client"

import { useState, useEffect } from "react"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { useAuth } from "@/components/auth-provider"
import { bookingsService, Booking } from "@/lib/bookings"
import { Plane, Calendar, MapPin, Clock, Download, Share, AlertCircle, CheckCircle, XCircle, Trash2, Settings } from "lucide-react"
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
    if (user) {
      const userBookings = bookingsService.getUserBookings(user.id)
      setBookings(userBookings)
    }
    setLoading(false)
  }, [user])

  // Refresh bookings when component mounts (useful after booking completion)
  useEffect(() => {
    const refreshBookings = () => {
      if (user) {
        const userBookings = bookingsService.getUserBookings(user.id)
        setBookings(userBookings)
      }
    }

    // Refresh on mount
    refreshBookings()

    // Listen for storage changes (in case bookings are added from another tab)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'userBookings') {
        refreshBookings()
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [user])

  if (!user) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-20">
          <Card className="max-w-md mx-auto text-center">
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
      bookingsService.deleteBooking(bookingId)
      setBookings(bookings.filter(booking => booking.id !== bookingId))
      toast({
        title: "Booking removed",
        description: "Your booking has been removed successfully.",
      })
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
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">My Trips</h1>
          <p className="text-muted-foreground">
            Manage your bookings, check flight status, and access your travel documents.
          </p>
        </div>

        {/* Search */}
        <div className="mb-6">
          <Input
            placeholder="Search by booking reference, destination, or airline..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="max-w-md"
          />
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 max-w-md">
            <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
            <TabsTrigger value="completed">Completed</TabsTrigger>
            <TabsTrigger value="cancelled">Cancelled</TabsTrigger>
          </TabsList>

          <TabsContent value={activeTab} className="mt-6">
            {loading ? (
              <Card className="text-center py-12">
                <CardContent>
                  <Plane className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                  <h3 className="text-xl font-semibold mb-2">Loading trips...</h3>
                  <p className="text-muted-foreground mb-6">Please wait while we fetch your bookings.</p>
                </CardContent>
              </Card>
            ) : filteredTrips.length === 0 ? (
              <Card className="text-center py-12">
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
                {filteredTrips.map((booking) => {
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
                    <Card key={booking.id} className="hover:shadow-lg transition-shadow">
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
                            <Button variant="outline" size="sm">
                              <Download className="h-4 w-4 mr-1" />
                              Download
                            </Button>
                            <Button variant="outline" size="sm">
                              <Share className="h-4 w-4 mr-1" />
                              Share
                            </Button>
                            <AlertDialog>
                              <AlertDialogTrigger asChild>
                                <Button variant="outline" size="sm">
                                  <Trash2 className="h-4 w-4 mr-1" />
                                  Remove
                                </Button>
                              </AlertDialogTrigger>
                              <AlertDialogContent>
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
                                    <Plane className="h-4 w-4 text-muted-foreground mx-auto mb-1" />
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
                                <Button variant="outline" className="w-full bg-transparent" size="sm">
                                  Check-in Online
                                </Button>
                                <Button 
                                  variant="outline" 
                                  className="w-full bg-transparent" 
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
  )
}
