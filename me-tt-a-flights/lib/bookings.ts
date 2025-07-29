export interface PassengerInfo {
  firstName: string
  lastName: string
  dateOfBirth: string
  passportNumber: string
  email: string
  phone: string
  seatPreference: string
  specialRequests: string
}

export interface PaymentInfo {
  cardNumber: string
  cardHolderName: string
  expiryMonth: string
  expiryYear: string
  cvv: string
  billingAddress: string
  city: string
  state: string
  zipCode: string
  country: string
}

export interface Booking {
  id: string
  bookingRef: string
  status: "confirmed" | "cancelled" | "completed"
  createdAt: string
  userId: string
  
  // Flight details
  flight: {
    year: string
    month: string
    day: string
    source: string
    destination: string
    cost: string
    takeoff: string
    landing: string
    duration: number
    is_connecting?: boolean
    connection_airport?: string
    layover_hours?: number
    airline?: {
      code: string
      name: string
      logo: string
      description: string
    }
  }
  
  // Booking details
  passengers: PassengerInfo[]
  payment: PaymentInfo
  totalCost: number
  passengerCount: number
}

class BookingsService {
  private readonly STORAGE_KEY = 'userBookings'

  // Get all bookings for a user
  getUserBookings(userId: string): Booking[] {
    try {
      const bookings = localStorage.getItem(this.STORAGE_KEY)
      if (bookings) {
        const allBookings: Booking[] = JSON.parse(bookings)
        return allBookings.filter(booking => booking.userId === userId)
      }
      return []
    } catch (error) {
      console.error('Error getting user bookings:', error)
      return []
    }
  }

  // Add a new booking
  addBooking(booking: Booking): void {
    try {
      const existingBookings = localStorage.getItem(this.STORAGE_KEY)
      const allBookings: Booking[] = existingBookings ? JSON.parse(existingBookings) : []
      
      allBookings.push(booking)
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(allBookings))
    } catch (error) {
      console.error('Error adding booking:', error)
    }
  }

  // Update booking status
  updateBookingStatus(bookingId: string, status: Booking['status']): void {
    try {
      const bookings = localStorage.getItem(this.STORAGE_KEY)
      if (bookings) {
        const allBookings: Booking[] = JSON.parse(bookings)
        const updatedBookings = allBookings.map(booking => 
          booking.id === bookingId ? { ...booking, status } : booking
        )
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(updatedBookings))
      }
    } catch (error) {
      console.error('Error updating booking status:', error)
    }
  }

  // Delete a booking
  deleteBooking(bookingId: string): void {
    try {
      const bookings = localStorage.getItem(this.STORAGE_KEY)
      if (bookings) {
        const allBookings: Booking[] = JSON.parse(bookings)
        const filteredBookings = allBookings.filter(booking => booking.id !== bookingId)
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(filteredBookings))
      }
    } catch (error) {
      console.error('Error deleting booking:', error)
    }
  }

  // Generate unique booking reference
  generateBookingRef(): string {
    const timestamp = Date.now().toString().slice(-8)
    const random = Math.random().toString(36).substring(2, 6).toUpperCase()
    return `BK${timestamp}${random}`
  }

  // Generate unique booking ID
  generateBookingId(): string {
    return `booking_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`
  }

  // Create a new booking from flight and form data
  createBooking(
    userId: string,
    flight: any,
    passengers: PassengerInfo[],
    payment: PaymentInfo,
    passengerCount: number
  ): Booking {
    const totalCost = parseInt(flight.cost) * passengerCount
    
    return {
      id: this.generateBookingId(),
      bookingRef: this.generateBookingRef(),
      status: "confirmed",
      createdAt: new Date().toISOString(),
      userId,
      flight,
      passengers,
      payment,
      totalCost,
      passengerCount
    }
  }

  // Get bookings by status
  getBookingsByStatus(userId: string, status: Booking['status']): Booking[] {
    const userBookings = this.getUserBookings(userId)
    return userBookings.filter(booking => booking.status === status)
  }

  // Get upcoming bookings (confirmed and future date)
  getUpcomingBookings(userId: string): Booking[] {
    const userBookings = this.getUserBookings(userId)
    const now = new Date()
    
    return userBookings.filter(booking => {
      if (booking.status !== "confirmed") return false
      
      const flightDate = new Date(
        parseInt(booking.flight.year),
        parseInt(booking.flight.month) - 1,
        parseInt(booking.flight.day)
      )
      
      return flightDate > now
    })
  }

  // Get completed bookings (past date)
  getCompletedBookings(userId: string): Booking[] {
    const userBookings = this.getUserBookings(userId)
    const now = new Date()
    
    return userBookings.filter(booking => {
      const flightDate = new Date(
        parseInt(booking.flight.year),
        parseInt(booking.flight.month) - 1,
        parseInt(booking.flight.day)
      )
      
      return flightDate < now
    })
  }
}

export const bookingsService = new BookingsService()