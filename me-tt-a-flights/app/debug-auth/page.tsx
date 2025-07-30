"use client"

import { useAuth } from '@/components/auth-provider'
import { debugAuthState, isAuthenticated, getAuthToken } from '@/lib/auth-utils'
import { useState } from 'react'

export default function DebugAuthPage() {
  const { user, login, register, logout } = useAuth()
  const [email, setEmail] = useState('test@example.com')
  const [password, setPassword] = useState('password123')
  const [name, setName] = useState('Test User')
  const [testResult, setTestResult] = useState<string>('')

  const handleDebugAuth = () => {
    debugAuthState()
    setTestResult('Check browser console for debug info')
  }

  const handleTestLogin = async () => {
    try {
      await login(email, password)
      setTestResult('Login successful!')
    } catch (error) {
      setTestResult(`Login failed: ${error}`)
    }
  }

  const handleTestRegister = async () => {
    try {
      await register(email, password, name)
      setTestResult('Registration successful!')
    } catch (error) {
      setTestResult(`Registration failed: ${error}`)
    }
  }

  const handleTestLogout = () => {
    logout()
    setTestResult('Logged out successfully!')
  }

  const handleTestBookingAPI = async () => {
    try {
      const token = getAuthToken()
      if (!token) {
        setTestResult('No token found. Please log in first.')
        return
      }

      const response = await fetch('http://localhost:8001/api/bookings', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const data = await response.json()
        setTestResult(`Booking API test successful! Found ${data.bookings?.length || 0} bookings.`)
      } else {
        const errorData = await response.json().catch(() => ({}))
        setTestResult(`Booking API test failed: ${response.status} - ${errorData.detail || 'Unknown error'}`)
      }
    } catch (error) {
      setTestResult(`Booking API test error: ${error}`)
    }
  }

  return (
    <div className="container mx-auto p-6 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">Authentication Debug Page</h1>
      
      <div className="bg-gray-100 p-4 rounded-lg mb-6">
        <h2 className="text-xl font-semibold mb-2">Current Auth State</h2>
        <p><strong>Authenticated:</strong> {isAuthenticated() ? 'Yes' : 'No'}</p>
        <p><strong>User:</strong> {user ? `${user.name} (${user.email})` : 'Not logged in'}</p>
        <p><strong>Token:</strong> {getAuthToken() ? 'Present' : 'Missing'}</p>
      </div>

      <div className="space-y-4">
        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-lg font-semibold mb-2">Debug Actions</h3>
          <button
            onClick={handleDebugAuth}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mr-2"
          >
            Debug Auth State
          </button>
          <button
            onClick={handleTestBookingAPI}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Test Booking API
          </button>
        </div>

        <div className="bg-white p-4 rounded-lg border">
          <h3 className="text-lg font-semibold mb-2">Authentication Test</h3>
          <div className="space-y-2">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border rounded"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border rounded"
            />
            <input
              type="text"
              placeholder="Name (for register)"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full p-2 border rounded"
            />
            <div className="space-x-2">
              <button
                onClick={handleTestLogin}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Test Login
              </button>
              <button
                onClick={handleTestRegister}
                className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
              >
                Test Register
              </button>
              <button
                onClick={handleTestLogout}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        {testResult && (
          <div className="bg-white p-4 rounded-lg border">
            <h3 className="text-lg font-semibold mb-2">Test Result</h3>
            <p className="text-gray-700">{testResult}</p>
          </div>
        )}
      </div>
    </div>
  )
} 