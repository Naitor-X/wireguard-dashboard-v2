import { useState, useEffect, useCallback } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';

export interface ClientData {
  id: number;
  name: string;
  public_key: string;
  allowed_ips: string[];
  email?: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  last_handshake?: string;
  transfer_rx?: number;
  transfer_tx?: number;
}

export interface SystemStatusData {
  total_clients: number;
  active_clients: number;
  total_transfer_rx: number;
  total_transfer_tx: number;
  server_uptime: number;
  last_updated: string;
}

interface UseClientStatusOptions {
  pollingInterval?: number;
  enabled?: boolean;
}

export function useClientStatus({ pollingInterval = 5000, enabled = true }: UseClientStatusOptions = {}) {
  const queryClient = useQueryClient();
  const [isAutoRefreshEnabled, setIsAutoRefreshEnabled] = useState(enabled);

  // Abfrage für alle Clients
  const clientsQuery = useQuery<{ clients: ClientData[], total: number }>({
    queryKey: ['clients'],
    queryFn: async () => {
      const response = await apiClient.get('/api/clients');
      return response.data;
    },
    refetchInterval: isAutoRefreshEnabled ? pollingInterval : false,
    refetchOnWindowFocus: isAutoRefreshEnabled,
  });

  // Abfrage für Systemstatus
  const systemStatusQuery = useQuery<SystemStatusData>({
    queryKey: ['systemStatus'],
    queryFn: async () => {
      const response = await apiClient.get('/api/status');
      return response.data;
    },
    refetchInterval: isAutoRefreshEnabled ? pollingInterval : false,
    refetchOnWindowFocus: isAutoRefreshEnabled,
  });

  // Manuelle Aktualisierung
  const refreshData = useCallback(() => {
    queryClient.invalidateQueries({ queryKey: ['clients'] });
    queryClient.invalidateQueries({ queryKey: ['systemStatus'] });
  }, [queryClient]);

  // Auto-Refresh umschalten
  const toggleAutoRefresh = useCallback(() => {
    setIsAutoRefreshEnabled(prev => !prev);
  }, []);

  return {
    clients: clientsQuery.data?.clients || [],
    totalClients: clientsQuery.data?.total || 0,
    systemStatus: systemStatusQuery.data,
    isLoading: clientsQuery.isLoading || systemStatusQuery.isLoading,
    isError: clientsQuery.isError || systemStatusQuery.isError,
    error: clientsQuery.error || systemStatusQuery.error,
    refreshData,
    isAutoRefreshEnabled,
    toggleAutoRefresh,
    lastUpdated: systemStatusQuery.data?.last_updated || new Date().toISOString()
  };
} 