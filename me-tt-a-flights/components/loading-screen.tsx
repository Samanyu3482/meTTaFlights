"use client"

import { useEffect, useState } from "react"
import { Plane } from "lucide-react"
import { Progress } from "@/components/ui/progress"

interface LoadingScreenProps {
  onComplete: () => void
}

export function LoadingScreen({ onComplete }: LoadingScreenProps) {
  const [progress, setProgress] = useState(0)
  const [showPlane, setShowPlane] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setShowPlane(true), 500)

    const progressTimer = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressTimer)
          setTimeout(onComplete, 500)
          return 100
        }
        return prev + 2
      })
    }, 60)

    return () => {
      clearTimeout(timer)
      clearInterval(progressTimer)
    }
  }, [onComplete])

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-purple-600 via-purple-700 to-pink-600">
      <div className="text-center text-white">
        {/* Flying Plane Animation */}
        <div className="relative h-32 mb-8 overflow-hidden">
          {showPlane && (
            <div className="animate-fly-in">
              <Plane className="h-12 w-12 text-white" />
            </div>
          )}
          {/* Flight Path Trail */}
          <div className="absolute top-1/2 left-0 w-full h-0.5 bg-white/30">
            <div className="h-full bg-white/60 animate-pulse"></div>
          </div>
        </div>

        {/* Logo */}
        <div className="flex items-center justify-center space-x-3 mb-8">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/20 backdrop-blur">
            <Plane className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-4xl font-bold">meTTaFlights</h1>
        </div>

        {/* Loading Text */}
        <div className="mb-8">
          <p className="text-xl mb-2">Preparing your journey</p>
          <div className="flex justify-center space-x-1">
            <div className="w-2 h-2 bg-white rounded-full loading-dots" style={{ animationDelay: "0s" }}></div>
            <div className="w-2 h-2 bg-white rounded-full loading-dots" style={{ animationDelay: "0.2s" }}></div>
            <div className="w-2 h-2 bg-white rounded-full loading-dots" style={{ animationDelay: "0.4s" }}></div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-80 mx-auto">
          <Progress value={progress} className="h-2 bg-white/20" />
          <p className="text-sm mt-2 opacity-80">{progress}% Complete</p>
        </div>
      </div>
    </div>
  )
}
