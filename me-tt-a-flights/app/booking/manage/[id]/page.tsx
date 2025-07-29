"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { useToast } from "@/hooks/use-toast"
import { useAuth } from "@/components/auth-provider"
import { bookingsService, Booking } from "@/lib/bookings"
import { 
  Plane, 
  Calendar, 
  MapPin, 
  Clock, 
  DollarSign,
  User,
  CreditCard,
  ArrowLeft,
  Download,
  Share,
  CheckCircle,
  AlertCircle,
  Loader2,
  Phone,
  Mail,
  FileText,
  CreditCard as CardIcon
} from "lucide-react"

export default function ManageBookingPage() {
  const params = useParams()
  const router = useRouter()
  const { toast } = useToast()
  const { user } = useAuth()
  const [booking, setBooking] = useState<Booking | null>(null)
  const [loading, setLoading] = useState(true)

  const bookingId = params.id as string

  useEffect(() => {
    if (!user) {
      router.push('/login')
      return
    }

    const loadBooking = () => {
      try {
        const userBookings = bookingsService.getUserBookings(user.id)
        const foundBooking = userBookings.find(b => b.id === bookingId)
        
        if (foundBooking) {
          setBooking(foundBooking)
        } else {
          toast({
            title: "Booking not found",
            description: "The requested booking could not be found.",
            variant: "destructive",
          })
          router.push('/trips')
        }
      } catch (error) {
        toast({
          title: "Error loading booking",
          description: "Failed to load booking details.",
          variant: "destructive",
        })
        router.push('/trips')
      } finally {
        setLoading(false)
      }
    }

    loadBooking()
  }, [bookingId, user, router, toast])

  if (!user) {
    return null
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-20">
          <div className="flex items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin" />
            <span className="ml-2">Loading booking details...</span>
          </div>
        </div>
      </div>
    )
  }

  if (!booking) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-20">
          <Card className="max-w-md mx-auto text-center">
            <CardContent className="p-8">
              <AlertCircle className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
              <h2 className="text-2xl font-bold mb-4">Booking Not Found</h2>
              <p className="text-muted-foreground mb-6">The requested booking could not be found.</p>
              <Button onClick={() => router.push('/trips')}>
                Back to Trips
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
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

  const formatDate = (year: string, month: string, day: string) => {
    const paddedMonth = month.padStart(2, '0')
    const paddedDay = day.padStart(2, '0')
    const date = new Date(`${year}-${paddedMonth}-${paddedDay}`)
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "confirmed":
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case "cancelled":
        return <AlertCircle className="h-4 w-4 text-red-600" />
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

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={() => router.push('/trips')}
            className="mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Trips
          </Button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Manage Booking</h1>
              <p className="text-muted-foreground">
                Booking Reference: {booking.bookingRef}
              </p>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline">
                <Download className="h-4 w-4 mr-1" />
                Download
              </Button>
              <Button variant="outline">
                <Share className="h-4 w-4 mr-1" />
                Share
              </Button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Flight Details */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center">
                    <Plane className="h-5 w-5 mr-2" />
                    Flight Details
                  </CardTitle>
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(booking.status)}
                    <Badge className={getStatusColor(booking.status)}>
                      {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between mb-6">
                  <div className="text-center">
                    <p className="text-2xl font-bold">{formatTime(booking.flight.takeoff)}</p>
                    <p className="text-lg font-medium">{booking.flight.source}</p>
                    <p className="text-sm text-muted-foreground">Departure</p>
                  </div>

                  <div className="flex-1 mx-6">
                    <div className="flex items-center justify-center space-x-2">
                      <div className="flex-1 h-px bg-border"></div>
                      <div className="text-center">
                        <Plane className="h-6 w-6 text-muted-foreground mx-auto mb-2" />
                        <p className="text-sm text-muted-foreground">{formatDuration(booking.flight.duration)}</p>
                        {booking.flight.airline && (
                          <p className="text-sm font-medium">{booking.flight.airline.name}</p>
                        )}
                        {booking.flight.is_connecting && (
                          <p className="text-xs text-muted-foreground">Via {booking.flight.connection_airport}</p>
                        )}
                      </div>
                      <div className="flex-1 h-px bg-border"></div>
                    </div>
                  </div>

                  <div className="text-center">
                    <p className="text-2xl font-bold">{formatTime(booking.flight.landing)}</p>
                    <p className="text-lg font-medium">{booking.flight.destination}</p>
                    <p className="text-sm text-muted-foreground">Arrival</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>{formatDate(booking.flight.year, booking.flight.month, booking.flight.day)}</span>
                  </div>
                  <div className="flex items-center">
                    <MapPin className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>{booking.passengerCount} Passenger{booking.passengerCount > 1 ? 's' : ''}</span>
                  </div>
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>Economy Class</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Passenger Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <User className="h-5 w-5 mr-2" />
                  Passenger Information
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {booking.passengers.map((passenger, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <h4 className="font-semibold mb-3">Passenger {index + 1}</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Full Name</p>
                          <p className="font-medium">{passenger.firstName} {passenger.lastName}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Date of Birth</p>
                          <p className="font-medium">{passenger.dateOfBirth}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Email</p>
                          <p className="font-medium flex items-center">
                            <Mail className="h-3 w-3 mr-1" />
                            {passenger.email}
                          </p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Phone</p>
                          <p className="font-medium flex items-center">
                            <Phone className="h-3 w-3 mr-1" />
                            {passenger.phone}
                          </p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Passport Number</p>
                          <p className="font-medium flex items-center">
                            <FileText className="h-3 w-3 mr-1" />
                            {passenger.passportNumber}
                          </p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Seat Preference</p>
                          <p className="font-medium capitalize">{passenger.seatPreference}</p>
                        </div>
                        {passenger.specialRequests && (
                          <div className="md:col-span-2">
                            <p className="text-muted-foreground">Special Requests</p>
                            <p className="font-medium">{passenger.specialRequests}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Payment Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CreditCard className="h-5 w-5 mr-2" />
                  Payment Information
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">Card Holder</p>
                    <p className="font-medium">{booking.payment.cardHolderName}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Card Number</p>
                    <p className="font-medium flex items-center">
                      <CardIcon className="h-3 w-3 mr-1" />
                      {booking.payment.cardNumber}
                    </p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Expiry Date</p>
                    <p className="font-medium">{booking.payment.expiryMonth}/{booking.payment.expiryYear}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Billing Address</p>
                    <p className="font-medium">{booking.payment.billingAddress}</p>
                    <p className="font-medium">{booking.payment.city}, {booking.payment.state} {booking.payment.zipCode}</p>
                    <p className="font-medium">{booking.payment.country}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Booking Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Booking Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Flight Cost</span>
                    <span>${parseInt(booking.flight.cost).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Passengers</span>
                    <span>{booking.passengerCount}</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between font-semibold text-lg">
                    <span>Total</span>
                    <span className="text-primary">${booking.totalCost.toLocaleString()}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Booking Actions */}
            {booking.status === "confirmed" && (
              <Card>
                <CardHeader>
                  <CardTitle>Booking Actions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <Button className="w-full">
                      Check-in Online
                    </Button>
                    <Button variant="outline" className="w-full">
                      Download Boarding Pass
                    </Button>
                    <Button variant="outline" className="w-full">
                      Modify Booking
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Contact Information */}
            <Card>
              <CardHeader>
                <CardTitle>Need Help?</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-sm">
                  <p>If you need assistance with your booking, please contact our customer service:</p>
                  <div className="flex items-center">
                    <Phone className="h-4 w-4 mr-2" />
                    <span>1-800-FLIGHTS</span>
                  </div>
                  <div className="flex items-center">
                    <Mail className="h-4 w-4 mr-2" />
                    <span>support@flights.com</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}