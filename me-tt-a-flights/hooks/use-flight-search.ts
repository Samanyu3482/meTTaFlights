import { useState, useCallback } from 'react';
import { apiService, FlightSearchRequest, Flight } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

export function useFlightSearch() {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const searchFlights = useCallback(async (params: FlightSearchRequest) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await apiService.searchFlights(params);
      setFlights(results);
      
      if (results.length === 0) {
        toast({
          title: "No flights found",
          description: "Try adjusting your search criteria.",
          variant: "destructive",
        });
      } else {
        toast({
          title: `${results.length} flights found`,
          description: "Here are your search results.",
        });
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to search flights';
      setError(errorMessage);
      toast({
        title: "Search failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const searchBySource = useCallback(async (source: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await apiService.searchBySource(source);
      setFlights(results);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to search flights';
      setError(errorMessage);
      toast({
        title: "Search failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const searchByDestination = useCallback(async (destination: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await apiService.searchByDestination(destination);
      setFlights(results);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to search flights';
      setError(errorMessage);
      toast({
        title: "Search failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const searchByRoute = useCallback(async (source: string, destination: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await apiService.searchByRoute(source, destination);
      setFlights(results);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to search flights';
      setError(errorMessage);
      toast({
        title: "Search failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const getAllFlights = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await apiService.getAllFlights();
      setFlights(results);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch flights';
      setError(errorMessage);
      toast({
        title: "Failed to fetch flights",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const clearResults = useCallback(() => {
    setFlights([]);
    setError(null);
  }, []);

  return {
    flights,
    loading,
    error,
    searchFlights,
    searchBySource,
    searchByDestination,
    searchByRoute,
    getAllFlights,
    clearResults,
  };
} 