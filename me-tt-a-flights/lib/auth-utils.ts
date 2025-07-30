// Authentication utility functions

export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') return false
  const token = localStorage.getItem('access_token')
  return !!token
}

export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('access_token')
}

export function clearAuthData(): void {
  if (typeof window === 'undefined') return
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
}

export function debugAuthState(): void {
  if (typeof window === 'undefined') return
  
  const token = localStorage.getItem('access_token')
  const user = localStorage.getItem('user')
  
  console.log('=== Authentication Debug Info ===')
  console.log('Access Token:', token ? 'Present' : 'Missing')
  console.log('User Data:', user ? 'Present' : 'Missing')
  
  if (token) {
    try {
      // Decode JWT token (without verification)
      const payload = JSON.parse(atob(token.split('.')[1]))
      console.log('Token Expiry:', new Date(payload.exp * 1000).toLocaleString())
      console.log('Token Type:', payload.type)
    } catch (error) {
      console.log('Token Decode Error:', error)
    }
  }
  
  if (user) {
    try {
      const userData = JSON.parse(user)
      console.log('User Email:', userData.email)
      console.log('User Name:', userData.name)
    } catch (error) {
      console.log('User Data Parse Error:', error)
    }
  }
  console.log('================================')
}

export function validateToken(): boolean {
  const token = getAuthToken()
  if (!token) return false
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const now = Math.floor(Date.now() / 1000)
    
    if (payload.exp < now) {
      console.warn('Token has expired')
      clearAuthData()
      return false
    }
    
    return true
  } catch (error) {
    console.error('Token validation error:', error)
    clearAuthData()
    return false
  }
}

// Function to handle API authentication errors
export function handleAuthError(status: number): void {
  if (status === 401) {
    console.warn('Authentication failed. Clearing auth data.')
    clearAuthData()
    
    // Redirect to login if in browser
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }
} 