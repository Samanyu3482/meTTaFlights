const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

export interface SavedPassenger {
  id: number
  first_name: string
  last_name: string
  date_of_birth: string
  passport_number: string
  email: string
  phone: string
  seat_preference: string
  special_requests?: string
  is_primary: boolean
  created_at: string
  updated_at: string
}

export interface SavedPayment {
  id: number
  card_number: string  // Last 4 digits only
  card_holder_name: string
  expiry_month: string
  expiry_year: string
  billing_address: string
  city: string
  state: string
  zip_code: string
  country: string
  is_default: boolean
  created_at: string
  updated_at: string
}

export interface SavedPassengerRequest {
  first_name: string
  last_name: string
  date_of_birth: string
  passport_number: string
  email: string
  phone: string
  seat_preference: string
  special_requests?: string
  is_primary: boolean
}

export interface SavedPaymentRequest {
  card_number: string
  card_holder_name: string
  expiry_month: string
  expiry_year: string
  billing_address: string
  city: string
  state: string
  zip_code: string
  country: string
  is_default: boolean
}

class SavedDetailsApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  // Saved Passengers
  async getSavedPassengers(): Promise<SavedPassenger[]> {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        console.warn('No access token found. User must be logged in to view saved passengers.')
        return []
      }

      const response = await fetch(`${API_BASE_URL}/api/user/saved-passengers`, {
        headers: this.getAuthHeaders()
      })

      if (response.status === 401) {
        console.warn('Authentication failed. Please log in again.')
        // Clear invalid token
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        return []
      }

      if (!response.ok) {
        throw new Error(`Failed to fetch saved passengers: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error getting saved passengers:', error)
      return []
    }
  }

  async savePassenger(passengerData: SavedPassengerRequest): Promise<SavedPassenger | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/saved-passengers`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(passengerData)
      })

      if (!response.ok) {
        throw new Error(`Failed to save passenger: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error saving passenger:', error)
      return null
    }
  }

  async updateSavedPassenger(passengerId: number, passengerData: SavedPassengerRequest): Promise<SavedPassenger | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/saved-passengers/${passengerId}`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(passengerData)
      })

      if (!response.ok) {
        throw new Error(`Failed to update saved passenger: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error updating saved passenger:', error)
      return null
    }
  }

  async deleteSavedPassenger(passengerId: number): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/saved-passengers/${passengerId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Failed to delete saved passenger: ${response.status}`)
      }

      return true
    } catch (error) {
      console.error('Error deleting saved passenger:', error)
      return false
    }
  }

  // Saved Payments
  async getSavedPayments(): Promise<SavedPayment[]> {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        console.warn('No access token found. User must be logged in to view saved payments.')
        return []
      }

      const response = await fetch(`${API_BASE_URL}/api/user/saved-payments`, {
        headers: this.getAuthHeaders()
      })

      if (response.status === 401) {
        console.warn('Authentication failed. Please log in again.')
        // Clear invalid token
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        return []
      }

      if (!response.ok) {
        throw new Error(`Failed to fetch saved payments: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error getting saved payments:', error)
      return []
    }
  }

  async savePayment(paymentData: SavedPaymentRequest): Promise<SavedPayment | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/saved-payments`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(paymentData)
      })

      if (!response.ok) {
        throw new Error(`Failed to save payment: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error saving payment:', error)
      return null
    }
  }

  async updateSavedPayment(paymentId: number, paymentData: SavedPaymentRequest): Promise<SavedPayment | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/saved-payments/${paymentId}`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(paymentData)
      })

      if (!response.ok) {
        throw new Error(`Failed to update saved payment: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error updating saved payment:', error)
      return null
    }
  }

  async deleteSavedPayment(paymentId: number): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/saved-payments/${paymentId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error(`Failed to delete saved payment: ${response.status}`)
      }

      return true
    } catch (error) {
      console.error('Error deleting saved payment:', error)
      return false
    }
  }

  // Convert saved passenger to booking passenger format
  convertSavedPassengerToBookingPassenger(savedPassenger: SavedPassenger) {
    return {
      first_name: savedPassenger.first_name,
      last_name: savedPassenger.last_name,
      date_of_birth: savedPassenger.date_of_birth,
      passport_number: savedPassenger.passport_number,
      email: savedPassenger.email,
      phone: savedPassenger.phone,
      seat_preference: savedPassenger.seat_preference,
      special_requests: savedPassenger.special_requests
    }
  }

  // Convert saved payment to booking payment format
  convertSavedPaymentToBookingPayment(savedPayment: SavedPayment) {
    return {
      card_number: savedPayment.card_number, // Note: This will only be last 4 digits
      card_holder_name: savedPayment.card_holder_name,
      expiry_month: savedPayment.expiry_month,
      expiry_year: savedPayment.expiry_year,
      billing_address: savedPayment.billing_address,
      city: savedPayment.city,
      state: savedPayment.state,
      zip_code: savedPayment.zip_code,
      country: savedPayment.country
    }
  }
}

export const savedDetailsApiService = new SavedDetailsApiService() 