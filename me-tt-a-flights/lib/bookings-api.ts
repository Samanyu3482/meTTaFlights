import { Booking } from './bookings'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

export interface BookingApiResponse {
  id: number
  booking_ref: string
  status: string
  user_id: number
  
  // Flight details
  flight_year: string
  flight_month: string
  flight_day: string
  source: string
  destination: string
  cost: string
  takeoff: string
  landing: string
  duration: number
  
  // Airline details
  airline_code?: string
  airline_name?: string
  airline_logo?: string
  airline_description?: string
  
  // Flight type
  is_connecting: boolean
  connection_airport?: string
  layover_hours?: number
  
  // Booking details
  total_cost: number
  passenger_count: number
  
  // Timestamps
  created_at: string
  updated_at: string
  
  // Related data
  passengers: Array<{
    id: number
    first_name: string
    last_name: string
    date_of_birth: string
    passport_number: string
    email: string
    phone: string
    seat_preference: string
    special_requests?: string
  }>
  payment: {
    id: number
    card_number: string
    card_holder_name: string
    expiry_month: string
    expiry_year: string
    cvv: string
    billing_address: string
    city: string
    state: string
    zip_code: string
    country: string
  }
}

export interface BookingListResponse {
  bookings: BookingApiResponse[]
  total: number
  page: number
  per_page: number
}

export interface CreateBookingRequest {
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
  passengers: Array<{
    first_name: string
    last_name: string
    date_of_birth: string
    passport_number: string
    email: string
    phone: string
    seat_preference: string
    special_requests?: string
  }>
  payment: {
    card_number: string
    card_holder_name: string
    expiry_month: string
    expiry_year: string
    cvv: string
    billing_address: string
    city: string
    state: string
    zip_code: string
    country: string
  }
  passenger_count: number
}

class BookingsApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  // Convert API response to frontend Booking format
  private convertApiResponseToBooking(apiBooking: BookingApiResponse): Booking {
    return {
      id: apiBooking.id.toString(), // Use numeric ID for backend compatibility
      bookingRef: apiBooking.booking_ref,
      status: apiBooking.status as "confirmed" | "cancelled" | "completed",
      createdAt: apiBooking.created_at,
      userId: apiBooking.user_id.toString(),
      
      // Flight details
      flight: {
        year: apiBooking.flight_year,
        month: apiBooking.flight_month,
        day: apiBooking.flight_day,
        source: apiBooking.source,
        destination: apiBooking.destination,
        cost: apiBooking.cost,
        takeoff: apiBooking.takeoff,
        landing: apiBooking.landing,
        duration: apiBooking.duration,
        is_connecting: apiBooking.is_connecting,
        connection_airport: apiBooking.connection_airport,
        layover_hours: apiBooking.layover_hours,
        airline: apiBooking.airline_code ? {
          code: apiBooking.airline_code,
          name: apiBooking.airline_name || '',
          logo: apiBooking.airline_logo || '',
          description: apiBooking.airline_description || ''
        } : undefined
      },
      
      // Convert passengers
      passengers: apiBooking.passengers.map(p => ({
        firstName: p.first_name,
        lastName: p.last_name,
        dateOfBirth: p.date_of_birth,
        passportNumber: p.passport_number,
        email: p.email,
        phone: p.phone,
        seatPreference: p.seat_preference,
        specialRequests: p.special_requests || ''
      })),
      
      // Convert payment
      payment: {
        cardNumber: apiBooking.payment.card_number,
        cardHolderName: apiBooking.payment.card_holder_name,
        expiryMonth: apiBooking.payment.expiry_month,
        expiryYear: apiBooking.payment.expiry_year,
        cvv: '', // Not stored in backend for security
        billingAddress: apiBooking.payment.billing_address,
        city: apiBooking.payment.city,
        state: apiBooking.payment.state,
        zipCode: apiBooking.payment.zip_code,
        country: apiBooking.payment.country
      },
      
      totalCost: apiBooking.total_cost,
      passengerCount: apiBooking.passenger_count
    }
  }

  // Get all bookings for a user
  async getUserBookings(): Promise<Booking[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch bookings: ${response.status}`)
      }

      const data: BookingListResponse = await response.json()
      return data.bookings.map(booking => this.convertApiResponseToBooking(booking))
    } catch (error) {
      console.error('Error getting user bookings:', error)
      return []
    }
  }

  // Create a new booking
  async createBooking(bookingData: CreateBookingRequest): Promise<Booking | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(bookingData)
      })

      if (!response.ok) {
        throw new Error(`Failed to create booking: ${response.status}`)
      }

      const apiBooking: BookingApiResponse = await response.json()
      return this.convertApiResponseToBooking(apiBooking)
    } catch (error) {
      console.error('Error creating booking:', error)
      return null
    }
  }

  // Update booking status
  async updateBookingStatus(bookingId: string, status: "confirmed" | "cancelled" | "completed"): Promise<Booking | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings/${bookingId}/status`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ status })
      })

      if (!response.ok) {
        throw new Error(`Failed to update booking status: ${response.status}`)
      }

      const apiBooking: BookingApiResponse = await response.json()
      return this.convertApiResponseToBooking(apiBooking)
    } catch (error) {
      console.error('Error updating booking status:', error)
      return null
    }
  }

  // Delete a booking
  async deleteBooking(bookingId: string): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings/${bookingId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Failed to delete booking: ${response.status}`)
      }

      return true
    } catch (error) {
      console.error('Error deleting booking:', error)
      return false
    }
  }

  // Get upcoming bookings
  async getUpcomingBookings(): Promise<Booking[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings/upcoming`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch upcoming bookings: ${response.status}`)
      }

      const data: BookingListResponse = await response.json()
      return data.bookings.map(booking => this.convertApiResponseToBooking(booking))
    } catch (error) {
      console.error('Error getting upcoming bookings:', error)
      return []
    }
  }

  // Get completed bookings
  async getCompletedBookings(): Promise<Booking[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings/completed`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch completed bookings: ${response.status}`)
      }

      const data: BookingListResponse = await response.json()
      return data.bookings.map(booking => this.convertApiResponseToBooking(booking))
    } catch (error) {
      console.error('Error getting completed bookings:', error)
      return []
    }
  }

  // Get booking by ID
  async getBookingById(bookingId: string): Promise<Booking | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/bookings/${bookingId}`, {
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch booking: ${response.status}`)
      }

      const apiBooking: BookingApiResponse = await response.json()
      return this.convertApiResponseToBooking(apiBooking)
    } catch (error) {
      console.error('Error getting booking:', error)
      return null
    }
  }
}

export const bookingsApiService = new BookingsApiService() 