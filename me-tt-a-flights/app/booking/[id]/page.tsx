"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { useToast } from "@/hooks/use-toast"
import { useAuth } from "@/components/auth-provider"
import { Flight } from "@/lib/api"
import { bookingsService, PassengerInfo, PaymentInfo } from "@/lib/bookings"
import { 
  Plane, 
  CreditCard, 
  User, 
  Calendar, 
  MapPin, 
  Clock, 
  DollarSign,
  ArrowLeftRight,
  CheckCircle,
  AlertCircle,
  Loader2
} from "lucide-react"

interface BookingForm {
  passengers: PassengerInfo[]
  payment: PaymentInfo
  termsAccepted: boolean
  marketingEmails: boolean
}

export default function BookingPage() {
  const params = useParams()
  const router = useRouter()
  const { toast } = useToast()
  const { user } = useAuth()
  const [flight, setFlight] = useState<Flight | null>(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [passengerCount, setPassengerCount] = useState(1)
  const [bookingForm, setBookingForm] = useState<BookingForm>({
    passengers: [{
      firstName: "",
      lastName: "",
      dateOfBirth: "",
      passportNumber: "",
      email: "",
      phone: "",
      seatPreference: "window",
      specialRequests: ""
    }],
    payment: {
      cardNumber: "",
      cardHolderName: "",
      expiryMonth: "",
      expiryYear: "",
      cvv: "",
      billingAddress: "",
      city: "",
      state: "",
      zipCode: "",
      country: "United States"
    },
    termsAccepted: false,
    marketingEmails: false
  })

  // Load flight data from localStorage (passed from flight search)
  useEffect(() => {
    const flightData = localStorage.getItem('selectedFlight')
    if (flightData) {
      try {
        const parsedFlight = JSON.parse(flightData)
        setFlight(parsedFlight)
      } catch (error) {
        console.error('Error parsing flight data:', error)
        toast({
          title: "Error",
          description: "Unable to load flight details. Please try searching again.",
          variant: "destructive",
        })
        router.push('/flights')
      }
    } else {
      toast({
        title: "No Flight Selected",
        description: "Please select a flight to book.",
        variant: "destructive",
      })
      router.push('/flights')
    }
    setLoading(false)
  }, [router, toast])

  // Update passengers array when passenger count changes
  useEffect(() => {
    const newPassengers = []
    for (let i = 0; i < passengerCount; i++) {
      newPassengers.push(bookingForm.passengers[i] || {
        firstName: "",
        lastName: "",
        dateOfBirth: "",
        passportNumber: "",
        email: "",
        phone: "",
        seatPreference: "window",
        specialRequests: ""
      })
    }
    setBookingForm(prev => ({ ...prev, passengers: newPassengers }))
  }, [passengerCount])

  const updatePassenger = (index: number, field: keyof PassengerInfo, value: string) => {
    const newPassengers = [...bookingForm.passengers]
    newPassengers[index] = { ...newPassengers[index], [field]: value }
    setBookingForm(prev => ({ ...prev, passengers: newPassengers }))
  }

  const updatePayment = (field: keyof PaymentInfo, value: string) => {
    setBookingForm(prev => ({
      ...prev,
      payment: { ...prev.payment, [field]: value }
    }))
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

  const calculateTotalCost = () => {
    if (!flight) return 0
    const baseCost = parseInt(flight.cost)
    return baseCost * passengerCount
  }

  const validateForm = () => {
    // Validate passengers
    for (let i = 0; i < bookingForm.passengers.length; i++) {
      const passenger = bookingForm.passengers[i]
      if (!passenger.firstName || !passenger.lastName || !passenger.dateOfBirth || 
          !passenger.email || !passenger.phone) {
        toast({
          title: "Missing Information",
          description: `Please fill in all required fields for passenger ${i + 1}.`,
          variant: "destructive",
        })
        return false
      }
    }

    // Validate payment
    const payment = bookingForm.payment
    if (!payment.cardNumber || !payment.cardHolderName || !payment.expiryMonth || 
        !payment.expiryYear || !payment.cvv || !payment.billingAddress || 
        !payment.city || !payment.state || !payment.zipCode) {
      toast({
        title: "Missing Payment Information",
        description: "Please fill in all payment details.",
        variant: "destructive",
      })
      return false
    }

    if (!bookingForm.termsAccepted) {
      toast({
        title: "Terms Not Accepted",
        description: "Please accept the terms and conditions to continue.",
        variant: "destructive",
      })
      return false
    }

    return true
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return
    if (!user) {
      toast({
        title: "Authentication required",
        description: "Please log in to complete your booking.",
        variant: "destructive",
      })
      router.push('/login')
      return
    }

    setSubmitting(true)

    try {
      // Simulate API call for booking
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Create booking using the bookings service
      const booking = bookingsService.createBooking(
        user.id,
        flight!,
        bookingForm.passengers,
        bookingForm.payment,
        passengerCount
      )

      // Save the booking
      bookingsService.addBooking(booking)

      toast({
        title: "Booking Successful!",
        description: `Your booking reference is ${booking.bookingRef}. Check your email for confirmation.`,
      })

      // Clear selected flight from localStorage
      localStorage.removeItem('selectedFlight')

      // Redirect to trips page
      router.push('/trips')
    } catch (error) {
      toast({
        title: "Booking Failed",
        description: "There was an error processing your booking. Please try again.",
        variant: "destructive",
      })
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin mr-2" />
            <span>Loading flight details...</span>
          </div>
        </div>
      </div>
    )
  }

  if (!flight) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 mx-auto mb-4 text-destructive" />
            <h2 className="text-xl font-semibold mb-2">No Flight Selected</h2>
            <p className="text-muted-foreground mb-4">Please select a flight to book.</p>
            <Button onClick={() => router.push('/flights')}>
              Back to Flights
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Button 
            variant="ghost" 
            onClick={() => router.push('/flights')}
            className="mb-4"
          >
            ← Back to Flights
          </Button>
          <h1 className="text-3xl font-bold">Complete Your Booking</h1>
        </div>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Flight Details */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Plane className="mr-2 h-5 w-5" />
                  Flight Details
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Route */}
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-lg">{flight.source}</span>
                  <ArrowLeftRight className="h-4 w-4 text-muted-foreground" />
                  <span className="font-semibold text-lg">{flight.destination}</span>
                </div>

                {/* Connection Badge */}
                {flight.is_connecting && (
                  <Badge variant="secondary">
                    <Plane className="h-3 w-3 mr-1" />
                    Connecting Flight
                  </Badge>
                )}

                {/* Flight Info */}
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Date:</span>
                    <span>{formatDate(flight.year, flight.month, flight.day)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Time:</span>
                    <span>{formatTime(flight.takeoff)} - {formatTime(flight.landing)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Duration:</span>
                    <span>{formatDuration(flight.duration)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Price per passenger:</span>
                    <span className="font-semibold">{formatCost(flight.cost)}</span>
                  </div>
                </div>

                {/* Connection Details */}
                {flight.is_connecting && flight.connection_airport && (
                  <div className="p-3 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">
                      Connection at {flight.connection_airport}
                      {flight.layover_hours && ` (${flight.layover_hours.toFixed(1)}h layover)`}
                    </p>
                  </div>
                )}

                {/* Airline Info */}
                {flight.airline && (
                  <div className="flex items-center space-x-2">
                    {flight.airline.logo && (
                      <img 
                        src={flight.airline.logo} 
                        alt={flight.airline.name}
                        className="h-6 w-6 object-contain"
                      />
                    )}
                    <span className="text-sm">{flight.airline.name}</span>
                  </div>
                )}

                <Separator />

                {/* Total Cost */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Passengers:</span>
                    <span>{passengerCount}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Price per passenger:</span>
                    <span>{formatCost(flight.cost)}</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between font-semibold text-lg">
                    <span>Total:</span>
                    <span className="text-green-600">{formatCost(calculateTotalCost().toString())}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Booking Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Passenger Count */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <User className="mr-2 h-5 w-5" />
                  Number of Passengers
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Select value={passengerCount.toString()} onValueChange={(value) => setPassengerCount(parseInt(value))}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5, 6].map(num => (
                      <SelectItem key={num} value={num.toString()}>
                        {num} {num === 1 ? 'Passenger' : 'Passengers'}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </CardContent>
            </Card>

            {/* Passenger Information */}
            {bookingForm.passengers.map((passenger, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle>Passenger {index + 1}</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor={`firstName-${index}`}>First Name *</Label>
                    <Input
                      id={`firstName-${index}`}
                      value={passenger.firstName}
                      onChange={(e) => updatePassenger(index, 'firstName', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor={`lastName-${index}`}>Last Name *</Label>
                    <Input
                      id={`lastName-${index}`}
                      value={passenger.lastName}
                      onChange={(e) => updatePassenger(index, 'lastName', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor={`dob-${index}`}>Date of Birth *</Label>
                    <Input
                      id={`dob-${index}`}
                      type="date"
                      value={passenger.dateOfBirth}
                      onChange={(e) => updatePassenger(index, 'dateOfBirth', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor={`passport-${index}`}>Passport Number *</Label>
                    <Input
                      id={`passport-${index}`}
                      value={passenger.passportNumber}
                      onChange={(e) => updatePassenger(index, 'passportNumber', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor={`email-${index}`}>Email *</Label>
                    <Input
                      id={`email-${index}`}
                      type="email"
                      value={passenger.email}
                      onChange={(e) => updatePassenger(index, 'email', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor={`phone-${index}`}>Phone *</Label>
                    <Input
                      id={`phone-${index}`}
                      type="tel"
                      value={passenger.phone}
                      onChange={(e) => updatePassenger(index, 'phone', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor={`seat-${index}`}>Seat Preference</Label>
                    <Select 
                      value={passenger.seatPreference} 
                      onValueChange={(value) => updatePassenger(index, 'seatPreference', value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="window">Window</SelectItem>
                        <SelectItem value="aisle">Aisle</SelectItem>
                        <SelectItem value="middle">Middle</SelectItem>
                        <SelectItem value="any">Any</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="md:col-span-2">
                    <Label htmlFor={`requests-${index}`}>Special Requests</Label>
                    <Textarea
                      id={`requests-${index}`}
                      value={passenger.specialRequests}
                      onChange={(e) => updatePassenger(index, 'specialRequests', e.target.value)}
                      placeholder="Any special requests or dietary requirements..."
                    />
                  </div>
                </CardContent>
              </Card>
            ))}

            {/* Payment Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CreditCard className="mr-2 h-5 w-5" />
                  Payment Information
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="cardNumber">Card Number *</Label>
                    <Input
                      id="cardNumber"
                      value={bookingForm.payment.cardNumber}
                      onChange={(e) => updatePayment('cardNumber', e.target.value)}
                      placeholder="1234 5678 9012 3456"
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="cardHolder">Cardholder Name *</Label>
                    <Input
                      id="cardHolder"
                      value={bookingForm.payment.cardHolderName}
                      onChange={(e) => updatePayment('cardHolderName', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="expiryMonth">Expiry Month *</Label>
                    <Select 
                      value={bookingForm.payment.expiryMonth} 
                      onValueChange={(value) => updatePayment('expiryMonth', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Month" />
                      </SelectTrigger>
                      <SelectContent>
                        {Array.from({length: 12}, (_, i) => i + 1).map(month => (
                          <SelectItem key={month} value={month.toString().padStart(2, '0')}>
                            {month.toString().padStart(2, '0')}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="expiryYear">Expiry Year *</Label>
                    <Select 
                      value={bookingForm.payment.expiryYear} 
                      onValueChange={(value) => updatePayment('expiryYear', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Year" />
                      </SelectTrigger>
                      <SelectContent>
                        {Array.from({length: 10}, (_, i) => new Date().getFullYear() + i).map(year => (
                          <SelectItem key={year} value={year.toString()}>
                            {year}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="cvv">CVV *</Label>
                    <Input
                      id="cvv"
                      value={bookingForm.payment.cvv}
                      onChange={(e) => updatePayment('cvv', e.target.value)}
                      placeholder="123"
                      maxLength={4}
                      required
                    />
                  </div>
                </div>

                <Separator />

                <h3 className="font-semibold">Billing Address</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="md:col-span-2">
                    <Label htmlFor="billingAddress">Address *</Label>
                    <Input
                      id="billingAddress"
                      value={bookingForm.payment.billingAddress}
                      onChange={(e) => updatePayment('billingAddress', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="city">City *</Label>
                    <Input
                      id="city"
                      value={bookingForm.payment.city}
                      onChange={(e) => updatePayment('city', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="state">State *</Label>
                    <Input
                      id="state"
                      value={bookingForm.payment.state}
                      onChange={(e) => updatePayment('state', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="zipCode">ZIP Code *</Label>
                    <Input
                      id="zipCode"
                      value={bookingForm.payment.zipCode}
                      onChange={(e) => updatePayment('zipCode', e.target.value)}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="country">Country *</Label>
                    <Select 
                      value={bookingForm.payment.country} 
                      onValueChange={(value) => updatePayment('country', value)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="United States">United States</SelectItem>
                        <SelectItem value="Canada">Canada</SelectItem>
                        <SelectItem value="United Kingdom">United Kingdom</SelectItem>
                        <SelectItem value="Australia">Australia</SelectItem>
                        <SelectItem value="Germany">Germany</SelectItem>
                        <SelectItem value="France">France</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Terms and Conditions */}
            <Card>
              <CardContent className="pt-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="terms"
                      checked={bookingForm.termsAccepted}
                      onCheckedChange={(checked) => 
                        setBookingForm(prev => ({ ...prev, termsAccepted: checked as boolean }))
                      }
                    />
                    <Label htmlFor="terms" className="text-sm">
                      I agree to the terms and conditions and cancellation policy *
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="marketing"
                      checked={bookingForm.marketingEmails}
                      onCheckedChange={(checked) => 
                        setBookingForm(prev => ({ ...prev, marketingEmails: checked as boolean }))
                      }
                    />
                    <Label htmlFor="marketing" className="text-sm">
                      I would like to receive promotional emails and updates
                    </Label>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Submit Button */}
            <div className="flex justify-end">
              <Button 
                type="submit" 
                size="lg" 
                disabled={submitting}
                className="w-full md:w-auto"
              >
                {submitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing Booking...
                  </>
                ) : (
                  <>
                    <CheckCircle className="mr-2 h-4 w-4" />
                    Confirm Booking - {formatCost(calculateTotalCost().toString())}
                  </>
                )}
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}