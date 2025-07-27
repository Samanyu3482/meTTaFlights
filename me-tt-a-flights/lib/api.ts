const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface FlightSearchParams {
  source?: string;
  destination?: string;
  year?: number;
  month?: number;
  day?: number;
}

export interface AirlineInfo {
  code: string;
  name: string;
  logo: string;
  description: string;
}

export interface Flight {
  year: string;
  month: string;
  day: string;
  source: string;
  destination: string;
  cost: string;
  airline?: AirlineInfo;
}

export interface FlightSearchRequest {
  source?: string;
  destination?: string;
  year?: number;
  month?: number;
  day?: number;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  async searchFlights(params: FlightSearchRequest): Promise<Flight[]> {
    return this.request<Flight[]>('/api/flights/search', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  async getAllFlights(): Promise<Flight[]> {
    return this.request<Flight[]>('/api/flights/all');
  }

  async searchBySource(source: string): Promise<Flight[]> {
    return this.request<Flight[]>(`/api/flights/source/${encodeURIComponent(source)}`);
  }

  async searchByDestination(destination: string): Promise<Flight[]> {
    return this.request<Flight[]>(`/api/flights/destination/${encodeURIComponent(destination)}`);
  }

  async searchByRoute(source: string, destination: string): Promise<Flight[]> {
    return this.request<Flight[]>(`/api/flights/route/${encodeURIComponent(source)}/${encodeURIComponent(destination)}`);
  }

  async healthCheck(): Promise<{ status: string; message: string }> {
    return this.request<{ status: string; message: string }>('/health');
  }
}

export const apiService = new ApiService(); 