"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { LoadingScreen } from "@/components/loading-screen"

interface LoadingWrapperProps {
  children: React.ReactNode
}

export function LoadingWrapper({ children }: LoadingWrapperProps) {
  const [isLoading, setIsLoading] = useState(true)
  const [showContent, setShowContent] = useState(false)

  const handleLoadingComplete = () => {
    setIsLoading(false)
    setTimeout(() => setShowContent(true), 300)
  }

  useEffect(() => {
    // Minimum loading time of 2 seconds
    const minLoadTime = setTimeout(() => {
      if (!isLoading) return
    }, 2000)

    return () => clearTimeout(minLoadTime)
  }, [isLoading])

  if (isLoading) {
    return <LoadingScreen onComplete={handleLoadingComplete} />
  }

  return (
    <div className={`transition-opacity duration-500 ${showContent ? "opacity-100" : "opacity-0"}`}>{children}</div>
  )
}
