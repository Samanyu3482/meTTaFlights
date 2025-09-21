import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatTime(time: string): string {
  // Handle different time formats from API
  if (!time) return time;
  
  // Remove any existing colons or spaces
  const cleanTime = time.toString().replace(/[:\s]/g, '');
  
  // Handle different length formats
  if (cleanTime.length === 3) {
    // Format: "845" -> "08:45"
    return `0${cleanTime.slice(0, 1)}:${cleanTime.slice(1, 3)}`;
  } else if (cleanTime.length === 4) {
    // Format: "1845" -> "18:45"
    return `${cleanTime.slice(0, 2)}:${cleanTime.slice(2, 4)}`;
  } else if (cleanTime.length === 1 || cleanTime.length === 2) {
    // Handle single or double digit hours with no minutes
    const paddedTime = cleanTime.padStart(2, '0');
    return `${paddedTime}:00`;
  }
  
  // If already formatted or unrecognized format, return as is
  return time;
}

export function formatDuration(minutes: number): string {
  // Convert minutes to hours and minutes format
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  if (hours === 0) {
    return `${mins}m`;
  } else if (mins === 0) {
    return `${hours}h`;
  } else {
    return `${hours}h ${mins}m`;
  }
}
