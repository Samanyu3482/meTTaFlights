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
      // If no date is provided but we're searching for connecting flights, use today's date
      let searchParams = { ...params };
      if (!searchParams.year && !searchParams.month && !searchParams.day && searchParams.include_connections) {
        const today = new Date();
        searchParams = {
          ...searchParams,
          year: today.getFullYear(),
          month: today.getMonth() + 1,
          day: today.getDate(),
        };
        console.log('No date provided, using today\'s date for connecting flights:', searchParams);
      }
      
      const results = await apiService.searchFlights(searchParams);
      setFlights(results);
      
      if (results.length === 0) {
        // Provide more specific feedback for connecting flights
        if (searchParams.include_connections && searchParams.source && searchParams.destination) {
          toast({
            title: "No connecting flights found",
            description: "Try selecting a specific date or check if direct flights are available.",
            variant: "destructive",
          });
        } else {
          toast({
            title: "No flights found",
            description: "Try adjusting your search criteria or selecting a date.",
            variant: "destructive",
          });
        }
      } else {
        const priorityText = searchParams.priority === "cost" ? "lowest cost" : 
                           searchParams.priority === "time" ? "shortest duration" : "optimized";
        const connectionText = searchParams.include_connections ? " (including connections)" : "";
        toast({
          title: `${results.length} flights found`,
          description: `Results sorted by ${priorityText}${connectionText}.`,
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

  const searchByRoute = useCallback(async (source: string, destination: string, priority: string = "cost") => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await apiService.searchByRoute(source, destination, priority);
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

  const getAllFlights = useCallback(async (priority: string = "cost") => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await apiService.getAllFlights(priority);
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