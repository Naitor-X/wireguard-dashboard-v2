import React from 'react';
import { 
  Paper, 
  Typography, 
  Box, 
  Grid, 
  Divider, 
  Button,
  Switch,
  FormControlLabel,
  Tooltip,
  CircularProgress
} from '@mui/material';
import { 
  Refresh as RefreshIcon,
  AccessTime as AccessTimeIcon,
  Storage as StorageIcon,
  People as PeopleIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';
import { SystemStatusData } from '../../hooks/useClientStatus';
import { StatusIndicator } from './StatusIndicator';
import { TrafficStatistics } from './TrafficStatistics';

interface SystemStatusPanelProps {
  systemStatus?: SystemStatusData;
  isLoading: boolean;
  isError: boolean;
  error?: any;
  isAutoRefreshEnabled: boolean;
  onToggleAutoRefresh: () => void;
  onRefresh: () => void;
  lastUpdated: string;
}

// Hilfsfunktion zur Formatierung der Uptime
const formatUptime = (uptimeInSeconds: number): string => {
  const days = Math.floor(uptimeInSeconds / (3600 * 24));
  const hours = Math.floor((uptimeInSeconds % (3600 * 24)) / 3600);
  const minutes = Math.floor((uptimeInSeconds % 3600) / 60);
  
  const parts = [];
  if (days > 0) parts.push(`${days} Tage`);
  if (hours > 0) parts.push(`${hours} Stunden`);
  if (minutes > 0) parts.push(`${minutes} Minuten`);
  
  return parts.join(', ');
};

export const SystemStatusPanel: React.FC<SystemStatusPanelProps> = ({
  systemStatus,
  isLoading,
  isError,
  error,
  isAutoRefreshEnabled,
  onToggleAutoRefresh,
  onRefresh,
  lastUpdated,
}) => {
  // Bestimme den Serverstatus basierend auf den verfügbaren Daten
  const serverStatus = systemStatus ? 'online' : 'offline';
  
  // Formatiere das letzte Update-Datum
  const formattedLastUpdated = new Date(lastUpdated).toLocaleString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });

  return (
    <Paper 
      elevation={1} 
      sx={{ 
        p: 3, 
        borderRadius: 2,
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Header mit Titel und Status */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <StorageIcon sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h6">
            System-Status
          </Typography>
        </Box>
        
        <StatusIndicator 
          status={serverStatus} 
          showLabel 
          size="medium"
        />
      </Box>
      
      {/* Lade-Indikator */}
      {isLoading && (
        <Box 
          sx={{ 
            position: 'absolute', 
            top: 0, 
            left: 0, 
            right: 0, 
            bottom: 0, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            bgcolor: 'rgba(255, 255, 255, 0.7)',
            zIndex: 1
          }}
        >
          <CircularProgress size={40} />
        </Box>
      )}
      
      {/* Fehleranzeige */}
      {isError && (
        <Box 
          sx={{ 
            p: 2, 
            mb: 2, 
            bgcolor: 'error.light', 
            color: 'error.dark',
            borderRadius: 1
          }}
        >
          <Typography variant="body2">
            Fehler beim Laden der Statusdaten: {error?.message || 'Unbekannter Fehler'}
          </Typography>
        </Box>
      )}
      
      {/* Hauptinhalt */}
      <Grid container spacing={3}>
        {/* Client-Statistiken */}
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <PeopleIcon sx={{ mr: 1, fontSize: 20 }} />
              Client-Statistiken
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, ml: 2 }}>
              <Typography variant="body2">
                Aktive Clients: <strong>{systemStatus?.active_clients || 0}</strong>
              </Typography>
              <Typography variant="body2">
                Gesamtzahl Clients: <strong>{systemStatus?.total_clients || 0}</strong>
              </Typography>
            </Box>
          </Box>
        </Grid>
        
        {/* Server-Uptime */}
        <Grid item xs={12} md={6}>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <AccessTimeIcon sx={{ mr: 1, fontSize: 20 }} />
              Server-Uptime
            </Typography>
            
            <Typography variant="body2" sx={{ ml: 2 }}>
              {systemStatus ? formatUptime(systemStatus.server_uptime) : 'Keine Daten verfügbar'}
            </Typography>
          </Box>
        </Grid>
      </Grid>
      
      <Divider sx={{ my: 2 }} />
      
      {/* Traffic-Statistiken */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <SpeedIcon sx={{ mr: 1, fontSize: 20 }} />
          Traffic-Übersicht
        </Typography>
        
        <TrafficStatistics 
          transferRx={systemStatus?.total_transfer_rx} 
          transferTx={systemStatus?.total_transfer_tx}
          variant="detailed"
          elevation={0}
        />
      </Box>
      
      <Divider sx={{ my: 2 }} />
      
      {/* Footer mit Aktualisierungsoptionen */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
        <Box>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'flex', alignItems: 'center' }}>
            <AccessTimeIcon sx={{ mr: 0.5, fontSize: 14 }} />
            Letztes Update: {formattedLastUpdated}
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <FormControlLabel
            control={
              <Switch 
                size="small" 
                checked={isAutoRefreshEnabled}
                onChange={onToggleAutoRefresh}
                color="primary"
              />
            }
            label={
              <Typography variant="body2">
                Auto-Refresh
              </Typography>
            }
          />
          
          <Tooltip title="Manuell aktualisieren">
            <Button
              startIcon={<RefreshIcon />}
              onClick={onRefresh}
              size="small"
              sx={{ ml: 1 }}
            >
              Aktualisieren
            </Button>
          </Tooltip>
        </Box>
      </Box>
    </Paper>
  );
}; 