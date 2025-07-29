"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { CalendarIcon, Search, ArrowLeftRight } from "lucide-react"
import { format } from "date-fns"
import { AirportAutocomplete } from "./airport-autocomplete"

export function HomeSearch() {
  const router = useRouter()
  const [from, setFrom] = useState("")
  const [to, setTo] = useState("")
  const [departDate, setDepartDate] = useState<Date>(() => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow;
  })

  const handleSearch = () => {
    // Build query parameters
    const params = new URLSearchParams()
    if (from) params.append('from', from)
    if (to) params.append('to', to)
    if (departDate) {
      params.append('date', format(departDate, 'yyyy-MM-dd'))
    }
    
    // Redirect to flights page with search parameters
    const queryString = params.toString()
    router.push(`/flights${queryString ? `?${queryString}` : ''}`)
  }

  const swapLocations = () => {
    if (from && to) {
      const temp = from
      setFrom(to)
      setTo(temp)
    } else if (from && !to) {
      setTo(from)
      setFrom("")
    } else if (!from && to) {
      setFrom(to)
      setTo("")
    }
  }

  return (
    <Card className="w-full max-w-4xl mx-auto shadow-xl border-0 bg-white/95 backdrop-blur-sm">
      <CardContent className="p-8">
        <div className="space-y-6">
          {/* From and To */}
          <div className="space-y-4">
            <div className="flex items-center justify-center gap-4">
              <div className="flex-1 max-w-[280px]">
                <AirportAutocomplete
                  value={from}
                  onChange={setFrom}
                  label="From"
                  placeholder="Search airports (code, name, or city)"
                />
              </div>

              {/* Swap button in the center */}
              <Button
                variant="outline"
                size="icon"
                className="hidden md:flex bg-background border-2 hover:bg-muted shadow-sm mt-6 transition-all duration-200 hover:scale-110"
                onClick={swapLocations}
                title="Swap origin and destination"
              >
                <ArrowLeftRight className="h-4 w-4" />
              </Button>

              <div className="flex-1 max-w-[280px]">
                <AirportAutocomplete
                  value={to}
                  onChange={setTo}
                  label="To"
                  placeholder="Search airports (code, name, or city)"
                />
              </div>
            </div>

            {/* Search tips */}
            <div className="text-center">
              <p className="text-xs text-muted-foreground leading-relaxed">
                💡 Try typing: airport codes (LAX), city names (Los Angeles), or airport names (Kennedy)
              </p>
            </div>
          </div>

          {/* Quick Route Presets */}
          <div className="space-y-3">
            <Label className="text-sm">Quick Routes</Label>
            <div className="flex flex-wrap gap-3">
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => { 
                  setFrom("JFK"); 
                  setTo("LAX"); 
                  const tomorrow = new Date();
                  tomorrow.setDate(tomorrow.getDate() + 1);
                  setDepartDate(tomorrow);
                }}
                className="text-xs"
                title="New York JFK → Los Angeles LAX"
              >
                JFK → LAX
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => { 
                  setFrom("EWR"); 
                  setTo("ATL"); 
                  const nextWeek = new Date();
                  nextWeek.setDate(nextWeek.getDate() + 7);
                  setDepartDate(nextWeek);
                }}
                className="text-xs"
                title="Newark EWR → Atlanta ATL"
              >
                EWR → ATL
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => { 
                  setFrom("EWR"); 
                  setTo("BOS"); 
                  const nextWeek = new Date();
                  nextWeek.setDate(nextWeek.getDate() + 7);
                  setDepartDate(nextWeek);
                }}
                className="text-xs"
                title="Newark EWR → Boston BOS"
              >
                EWR → BOS
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => { 
                  setFrom("EWR"); 
                  setTo("SEA"); 
                  const nextWeek = new Date();
                  nextWeek.setDate(nextWeek.getDate() + 7);
                  setDepartDate(nextWeek);
                }}
                className="text-xs"
                title="Newark EWR → Seattle SEA"
              >
                EWR → SEA
              </Button>
            </div>
          </div>

          {/* Date */}
          <div className="space-y-3">
            <Label>Departure Date</Label>
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" className="w-full justify-start text-left font-normal bg-transparent">
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {departDate ? format(departDate, "PPP") : "Select date"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0">
                <Calendar 
                  mode="single" 
                  selected={departDate} 
                  onSelect={setDepartDate} 
                  initialFocus
                  disabled={(date) => date < new Date()}
                  fromYear={2024}
                  toYear={2026}
                  captionLayout="dropdown-buttons"
                />
              </PopoverContent>
            </Popover>
          </div>

          {/* Search Button */}
          <Button 
            onClick={handleSearch} 
            size="lg" 
            className="w-full flight-gradient text-white font-semibold text-lg py-6 hover:scale-105 transition-transform"
          >
            <Search className="mr-2 h-5 w-5" />
            Search Flights
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}