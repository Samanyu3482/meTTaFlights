"use client"

import { useState, useEffect, useRef } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { MapPin, Plane, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface Airport {
  code: string
  name: string
  city: string
  state: string
  full_name: string
}

interface AirportAutocompleteProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  label?: string
  className?: string
  onAirportSelect?: (airport: Airport) => void
}

export function AirportAutocomplete({
  value,
  onChange,
  placeholder = "Search airports...",
  label,
  className,
  onAirportSelect
}: AirportAutocompleteProps) {
  const [suggestions, setSuggestions] = useState<Airport[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [loading, setLoading] = useState(false)
  const [selectedAirport, setSelectedAirport] = useState<Airport | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const suggestionsRef = useRef<HTMLDivElement>(null)

  // Search airports when input changes
  useEffect(() => {
    const searchAirports = async () => {
      if (!value.trim()) {
        setSuggestions([])
        setShowSuggestions(false)
        setSelectedAirport(null)
        return
      }

      setLoading(true)
      try {
        const response = await fetch(`http://localhost:8000/api/airports/search?query=${encodeURIComponent(value)}&limit=8`)
        if (response.ok) {
          const data = await response.json()
          setSuggestions(data.airports || [])
          setShowSuggestions(data.airports && data.airports.length > 0)
        }
      } catch (error) {
        console.error("Error searching airports:", error)
        setSuggestions([])
        setShowSuggestions(false)
      } finally {
        setLoading(false)
      }
    }

    // Debounce the search
    const timeoutId = setTimeout(searchAirports, 300)
    return () => clearTimeout(timeoutId)
  }, [value])

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        inputRef.current &&
        !inputRef.current.contains(event.target as Node) &&
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleAirportSelect = (airport: Airport) => {
    setSelectedAirport(airport)
    onChange(airport.code)
    setShowSuggestions(false)
    if (onAirportSelect) {
      onAirportSelect(airport)
    }
  }

  const clearSelection = () => {
    setSelectedAirport(null)
    onChange("")
    setSuggestions([])
    setShowSuggestions(false)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value
    onChange(newValue)
    if (selectedAirport && newValue !== selectedAirport.code) {
      setSelectedAirport(null)
    }
  }

  const handleInputFocus = () => {
    if (value.trim() && suggestions.length > 0) {
      setShowSuggestions(true)
    }
  }

  return (
    <div className={cn("relative", className)}>
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 mb-2 block">
          {label}
        </label>
      )}
      
      <div className="relative">
        <MapPin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          ref={inputRef}
          value={value}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          placeholder={placeholder}
          className="pl-10 pr-10"
        />
        
        {selectedAirport && (
          <Button
            variant="ghost"
            size="sm"
            onClick={clearSelection}
            className="absolute right-1 top-1 h-6 w-6 p-0 hover:bg-muted"
          >
            <X className="h-3 w-3" />
          </Button>
        )}
      </div>

      {/* Suggestions Dropdown */}
      {showSuggestions && (
        <Card
          ref={suggestionsRef}
          className="absolute top-full left-0 right-0 z-50 mt-1 max-h-64 overflow-y-auto shadow-lg border"
        >
          <CardContent className="p-0">
            {loading ? (
              <div className="p-4 text-center text-sm text-muted-foreground">
                Searching airports...
              </div>
            ) : suggestions.length > 0 ? (
              <div className="py-1">
                {suggestions.map((airport) => (
                  <button
                    key={airport.code}
                    onClick={() => handleAirportSelect(airport)}
                    className="w-full px-4 py-3 text-left hover:bg-muted transition-colors flex items-center gap-3"
                  >
                    <div className="flex-shrink-0">
                      <Plane className="h-4 w-4 text-muted-foreground" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-sm">{airport.code}</span>
                        <span className="text-xs text-muted-foreground">•</span>
                        <span className="text-sm truncate">{airport.city}, {airport.state}</span>
                      </div>
                      <div className="text-xs text-muted-foreground truncate">
                        {airport.name}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            ) : value.trim() && !loading ? (
              <div className="p-4 text-center text-sm text-muted-foreground">
                No airports found
              </div>
            ) : null}
          </CardContent>
        </Card>
      )}

      {/* Selected Airport Display */}
      {selectedAirport && (
        <div className="mt-2 p-2 bg-muted/50 rounded-md border">
          <div className="flex items-center gap-2">
            <Plane className="h-3 w-3 text-muted-foreground" />
            <span className="text-xs font-medium">{selectedAirport.code}</span>
            <span className="text-xs text-muted-foreground">•</span>
            <span className="text-xs">{selectedAirport.city}, {selectedAirport.state}</span>
          </div>
        </div>
      )}
    </div>
  )
} 