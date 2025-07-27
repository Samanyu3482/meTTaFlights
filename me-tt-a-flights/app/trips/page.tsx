"use client"

import { useState } from "react"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { useAuth } from "@/components/auth-provider"
import { Plane, Calendar, MapPin, Clock, Download, Share, AlertCircle, CheckCircle, XCircle } from "lucide-react"
import Link from "next/link"

interface Trip {
  id: string
  bookingRef: string
  status: "confirmed" | "cancelled" | "completed"
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
  airline: string
  flightNumber: string
  duration: string
  seat: string
  class: string
  price: number
  passengers: string[]
}

const mockTrips: Trip[] = [
  {
    id: "1",
    bookingRef: "ABC123DEF",
    status: "confirmed",
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
    airline: "Delta Airlines",
    flightNumber: "DL 1234",
    duration: "6h 15m",
    seat: "12A",
    class: "Economy",
    price: 299,
    passengers: ["John Doe"],
  },
  {
    id: "2",
    bookingRef: "XYZ789GHI",
    status: "completed",
    departure: {
      airport: "LAX",
      city: "Los Angeles",
      time: "14:20",
      date: "2024-02-10",
    },
    arrival: {
      airport: "LHR",
      city: "London",
      time: "09:35",
      date: "2024-02-11",
    },
    airline: "British Airways",
    flightNumber: "BA 269",
    duration: "11h 15m",
    seat: "8C",
    class: "Premium Economy",
    price: 899,
    passengers: ["John Doe"],
  },
]

export default function TripsPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [activeTab, setActiveTab] = useState("upcoming")
  const { user } = useAuth()

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

  const filteredTrips = mockTrips.filter((trip) => {
    const matchesSearch =
      trip.bookingRef.toLowerCase().includes(searchTerm.toLowerCase()) ||
      trip.departure.city.toLowerCase().includes(searchTerm.toLowerCase()) ||
      trip.arrival.city.toLowerCase().includes(searchTerm.toLowerCase())

    if (activeTab === "upcoming") {
      return matchesSearch && trip.status === "confirmed"
    } else if (activeTab === "completed") {
      return matchesSearch && trip.status === "completed"
    } else {
      return matchesSearch && trip.status === "cancelled"
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
            {filteredTrips.length === 0 ? (
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
                {filteredTrips.map((trip) => (
                  <Card key={trip.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className="flex items-center space-x-2">
                            {getStatusIcon(trip.status)}
                            <Badge className={getStatusColor(trip.status)}>
                              {trip.status.charAt(0).toUpperCase() + trip.status.slice(1)}
                            </Badge>
                          </div>
                          <div>
                            <CardTitle className="text-lg">{trip.airline}</CardTitle>
                            <p className="text-sm text-muted-foreground">Booking Ref: {trip.bookingRef}</p>
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
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Flight Route */}
                        <div className="md:col-span-2">
                          <div className="flex items-center justify-between mb-4">
                            <div className="text-center">
                              <p className="text-2xl font-bold">{trip.departure.time}</p>
                              <p className="text-sm font-medium">{trip.departure.airport}</p>
                              <p className="text-xs text-muted-foreground">{trip.departure.city}</p>
                            </div>

                            <div className="flex-1 mx-4">
                              <div className="flex items-center justify-center space-x-2">
                                <div className="flex-1 h-px bg-border"></div>
                                <div className="text-center">
                                  <Plane className="h-4 w-4 text-muted-foreground mx-auto mb-1" />
                                  <p className="text-xs text-muted-foreground">{trip.duration}</p>
                                  <p className="text-xs font-medium">{trip.flightNumber}</p>
                                </div>
                                <div className="flex-1 h-px bg-border"></div>
                              </div>
                            </div>

                            <div className="text-center">
                              <p className="text-2xl font-bold">{trip.arrival.time}</p>
                              <p className="text-sm font-medium">{trip.arrival.airport}</p>
                              <p className="text-xs text-muted-foreground">{trip.arrival.city}</p>
                            </div>
                          </div>

                          <div className="flex items-center justify-center space-x-4 text-sm text-muted-foreground">
                            <div className="flex items-center">
                              <Calendar className="h-4 w-4 mr-1" />
                              {new Date(trip.departure.date).toLocaleDateString()}
                            </div>
                            <div className="flex items-center">
                              <MapPin className="h-4 w-4 mr-1" />
                              Seat {trip.seat}
                            </div>
                            <div className="flex items-center">
                              <Clock className="h-4 w-4 mr-1" />
                              {trip.class}
                            </div>
                          </div>
                        </div>

                        {/* Trip Details */}
                        <div className="space-y-4">
                          <div>
                            <p className="text-sm text-muted-foreground">Total Price</p>
                            <p className="text-2xl font-bold text-primary">${trip.price}</p>
                          </div>

                          <div>
                            <p className="text-sm text-muted-foreground">Passengers</p>
                            <div className="space-y-1">
                              {trip.passengers.map((passenger, index) => (
                                <p key={index} className="text-sm font-medium">
                                  {passenger}
                                </p>
                              ))}
                            </div>
                          </div>

                          {trip.status === "confirmed" && (
                            <div className="space-y-2">
                              <Button variant="outline" className="w-full bg-transparent" size="sm">
                                Check-in Online
                              </Button>
                              <Button variant="outline" className="w-full bg-transparent" size="sm">
                                Manage Booking
                              </Button>
                            </div>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
