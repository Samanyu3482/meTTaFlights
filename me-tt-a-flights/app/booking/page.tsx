"use client"

import { useState } from "react"
import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Progress } from "@/components/ui/progress"
import { Checkbox } from "@/components/ui/checkbox"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Plane, Shield, Check, ArrowRight } from "lucide-react"

const bookingSteps = [
  { id: 1, name: "Passenger Details", completed: false, current: true },
  { id: 2, name: "Seat Selection", completed: false, current: false },
  { id: 3, name: "Add-ons", completed: false, current: false },
  { id: 4, name: "Payment", completed: false, current: false },
  { id: 5, name: "Confirmation", completed: false, current: false },
]

export default function BookingPage() {
  const [currentStep, setCurrentStep] = useState(1)
  const [passengerData, setPassengerData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    dateOfBirth: "",
    passportNumber: "",
    nationality: "",
  })
  const [selectedSeat, setSelectedSeat] = useState("")
  const [addOns, setAddOns] = useState<string[]>([])
  const [paymentMethod, setPaymentMethod] = useState("card")

  const flightDetails = {
    airline: "Delta Airlines",
    flightNumber: "DL 1234",
    departure: {
      airport: "JFK",
      city: "New York",
      time: "08:30",
      date: "March 15, 2024",
    },
    arrival: {
      airport: "LAX",
      city: "Los Angeles",
      time: "11:45",
      date: "March 15, 2024",
    },
    duration: "6h 15m",
    price: 299,
    class: "Economy",
  }

  const seatMap = [
    ["1A", "1B", "", "1D", "1E", "1F"],
    ["2A", "2B", "", "2D", "2E", "2F"],
    ["3A", "3B", "", "3D", "3E", "3F"],
    ["4A", "4B", "", "4D", "4E", "4F"],
    ["5A", "5B", "", "5D", "5E", "5F"],
    ["6A", "6B", "", "6D", "6E", "6F"],
  ]

  const availableAddOns = [
    {
      id: "meal",
      name: "Special Meal",
      price: 25,
      description: "Choose from vegetarian, vegan, or gluten-free options",
    },
    { id: "baggage", name: "Extra Baggage", price: 50, description: "Additional 23kg checked baggage" },
    { id: "priority", name: "Priority Boarding", price: 15, description: "Board the aircraft first" },
    { id: "lounge", name: "Airport Lounge Access", price: 40, description: "Relax in comfort before your flight" },
  ]

  const handleNextStep = () => {
    if (currentStep < 5) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePreviousStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const calculateTotal = () => {
    const addOnTotal = addOns.reduce((total, addOnId) => {
      const addOn = availableAddOns.find((a) => a.id === addOnId)
      return total + (addOn?.price || 0)
    }, 0)
    return flightDetails.price + addOnTotal
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Passenger Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    value={passengerData.firstName}
                    onChange={(e) => setPassengerData({ ...passengerData, firstName: e.target.value })}
                    placeholder="Enter first name"
                  />
                </div>
                <div>
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    value={passengerData.lastName}
                    onChange={(e) => setPassengerData({ ...passengerData, lastName: e.target.value })}
                    placeholder="Enter last name"
                  />
                </div>
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={passengerData.email}
                    onChange={(e) => setPassengerData({ ...passengerData, email: e.target.value })}
                    placeholder="Enter email address"
                  />
                </div>
                <div>
                  <Label htmlFor="phone">Phone Number</Label>
                  <Input
                    id="phone"
                    value={passengerData.phone}
                    onChange={(e) => setPassengerData({ ...passengerData, phone: e.target.value })}
                    placeholder="Enter phone number"
                  />
                </div>
                <div>
                  <Label htmlFor="dateOfBirth">Date of Birth</Label>
                  <Input
                    id="dateOfBirth"
                    type="date"
                    value={passengerData.dateOfBirth}
                    onChange={(e) => setPassengerData({ ...passengerData, dateOfBirth: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="nationality">Nationality</Label>
                  <Select
                    value={passengerData.nationality}
                    onValueChange={(value) => setPassengerData({ ...passengerData, nationality: value })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select nationality" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="us">United States</SelectItem>
                      <SelectItem value="uk">United Kingdom</SelectItem>
                      <SelectItem value="ca">Canada</SelectItem>
                      <SelectItem value="au">Australia</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          </div>
        )

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Select Your Seat</h3>
              <div className="bg-muted/50 p-6 rounded-lg">
                <div className="text-center mb-4">
                  <Plane className="h-8 w-8 mx-auto mb-2 text-primary" />
                  <p className="text-sm text-muted-foreground">Front of Aircraft</p>
                </div>
                <div className="space-y-2">
                  {seatMap.map((row, rowIndex) => (
                    <div key={rowIndex} className="flex justify-center space-x-2">
                      {row.map((seat, seatIndex) =>
                        seat ? (
                          <Button
                            key={seat}
                            variant={selectedSeat === seat ? "default" : "outline"}
                            size="sm"
                            className="w-10 h-10 p-0"
                            onClick={() => setSelectedSeat(seat)}
                          >
                            {seat}
                          </Button>
                        ) : (
                          <div key={seatIndex} className="w-10 h-10"></div>
                        ),
                      )}
                    </div>
                  ))}
                </div>
                <div className="flex justify-center mt-4 space-x-4 text-xs">
                  <div className="flex items-center">
                    <div className="w-4 h-4 border border-border rounded mr-2"></div>
                    Available
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-primary rounded mr-2"></div>
                    Selected
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-muted rounded mr-2"></div>
                    Occupied
                  </div>
                </div>
              </div>
            </div>
          </div>
        )

      case 3:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Add-ons & Extras</h3>
              <div className="space-y-4">
                {availableAddOns.map((addOn) => (
                  <Card key={addOn.id} className="cursor-pointer hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <Checkbox
                            checked={addOns.includes(addOn.id)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                setAddOns([...addOns, addOn.id])
                              } else {
                                setAddOns(addOns.filter((id) => id !== addOn.id))
                              }
                            }}
                          />
                          <div>
                            <h4 className="font-medium">{addOn.name}</h4>
                            <p className="text-sm text-muted-foreground">{addOn.description}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">${addOn.price}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        )

      case 4:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Payment Information</h3>
              <RadioGroup value={paymentMethod} onValueChange={setPaymentMethod}>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="card" id="card" />
                  <Label htmlFor="card">Credit/Debit Card</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="paypal" id="paypal" />
                  <Label htmlFor="paypal">PayPal</Label>
                </div>
              </RadioGroup>

              {paymentMethod === "card" && (
                <div className="mt-6 space-y-4">
                  <div>
                    <Label htmlFor="cardNumber">Card Number</Label>
                    <Input id="cardNumber" placeholder="1234 5678 9012 3456" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="expiry">Expiry Date</Label>
                      <Input id="expiry" placeholder="MM/YY" />
                    </div>
                    <div>
                      <Label htmlFor="cvv">CVV</Label>
                      <Input id="cvv" placeholder="123" />
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="cardName">Name on Card</Label>
                    <Input id="cardName" placeholder="John Doe" />
                  </div>
                </div>
              )}
            </div>
          </div>
        )

      case 5:
        return (
          <div className="space-y-6 text-center">
            <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
              <Check className="h-8 w-8 text-green-600" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-green-600 mb-2">Booking Confirmed!</h3>
              <p className="text-muted-foreground">Your flight has been successfully booked.</p>
            </div>
            <div className="bg-muted/50 p-6 rounded-lg">
              <h4 className="font-semibold mb-2">Booking Reference</h4>
              <p className="text-2xl font-mono font-bold">ABC123DEF</p>
            </div>
            <Button size="lg" className="flight-gradient text-white">
              View Booking Details
            </Button>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            {bookingSteps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div
                  className={`flex items-center justify-center w-8 h-8 rounded-full border-2 ${
                    step.id <= currentStep
                      ? "bg-primary border-primary text-primary-foreground"
                      : "border-muted-foreground text-muted-foreground"
                  }`}
                >
                  {step.id < currentStep ? (
                    <Check className="h-4 w-4" />
                  ) : (
                    <span className="text-sm font-medium">{step.id}</span>
                  )}
                </div>
                <span
                  className={`ml-2 text-sm font-medium ${
                    step.id <= currentStep ? "text-foreground" : "text-muted-foreground"
                  }`}
                >
                  {step.name}
                </span>
                {index < bookingSteps.length - 1 && <ArrowRight className="h-4 w-4 mx-4 text-muted-foreground" />}
              </div>
            ))}
          </div>
          <Progress value={(currentStep / bookingSteps.length) * 100} className="h-2" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>
                  Step {currentStep}: {bookingSteps[currentStep - 1].name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {renderStepContent()}

                <div className="flex justify-between mt-8">
                  <Button variant="outline" onClick={handlePreviousStep} disabled={currentStep === 1}>
                    Previous
                  </Button>
                  <Button onClick={handleNextStep} disabled={currentStep === 5} className="flight-gradient text-white">
                    {currentStep === 4 ? "Complete Booking" : "Next"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Booking Summary */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle>Booking Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Flight Details */}
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <Plane className="h-4 w-4 text-primary" />
                    <span className="font-medium">{flightDetails.airline}</span>
                  </div>
                  <p className="text-sm text-muted-foreground">{flightDetails.flightNumber}</p>
                </div>

                <Separator />

                {/* Route */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{flightDetails.departure.airport}</p>
                      <p className="text-sm text-muted-foreground">{flightDetails.departure.city}</p>
                    </div>
                    <ArrowRight className="h-4 w-4 text-muted-foreground" />
                    <div className="text-right">
                      <p className="font-medium">{flightDetails.arrival.airport}</p>
                      <p className="text-sm text-muted-foreground">{flightDetails.arrival.city}</p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <span>{flightDetails.departure.date}</span>
                    <span>{flightDetails.duration}</span>
                  </div>
                </div>

                <Separator />

                {/* Selected Options */}
                {selectedSeat && (
                  <div>
                    <p className="font-medium">Selected Seat</p>
                    <p className="text-sm text-muted-foreground">{selectedSeat}</p>
                  </div>
                )}

                {addOns.length > 0 && (
                  <div>
                    <p className="font-medium mb-2">Add-ons</p>
                    {addOns.map((addOnId) => {
                      const addOn = availableAddOns.find((a) => a.id === addOnId)
                      return addOn ? (
                        <div key={addOnId} className="flex justify-between text-sm">
                          <span>{addOn.name}</span>
                          <span>${addOn.price}</span>
                        </div>
                      ) : null
                    })}
                  </div>
                )}

                <Separator />

                {/* Price Breakdown */}
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Base Fare</span>
                    <span>${flightDetails.price}</span>
                  </div>
                  {addOns.map((addOnId) => {
                    const addOn = availableAddOns.find((a) => a.id === addOnId)
                    return addOn ? (
                      <div key={addOnId} className="flex justify-between text-sm">
                        <span>{addOn.name}</span>
                        <span>${addOn.price}</span>
                      </div>
                    ) : null
                  })}
                  <Separator />
                  <div className="flex justify-between font-bold text-lg">
                    <span>Total</span>
                    <span>${calculateTotal()}</span>
                  </div>
                </div>

                {/* Security Badge */}
                <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                  <Shield className="h-4 w-4" />
                  <span>Secure booking protected by SSL encryption</span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
