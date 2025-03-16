import React, { useState, useMemo } from 'react';
import { 
  Box, 
  Grid, 
  Typography, 
  TextField, 
  InputAdornment,
  Button,
  Paper,
  Divider,
  Alert,
  Snackbar
} from '@mui/material';
import { 
  Search as SearchIcon, 
  Add as AddIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { useClientStatus } from '../../hooks/useClientStatus';
import { ClientStatusCard } from './ClientStatusCard';
import { SystemStatusPanel } from './SystemStatusPanel';

interface ClientsMonitoringPanelProps {
  onAddClient?: () => void;
  onEditClient?: (clientId: number) => void;
  onDeleteClient?: (clientId: number) => void;
  onDownloadConfig?: (clientId: number) => void;
  pollingInterval?: number;
}

export const ClientsMonitoringPanel: React.FC<ClientsMonitoringPanelProps> = ({
  onAddClient,
  onEditClient,
  onDeleteClient,
  onDownloadConfig,
  pollingInterval = 5000,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  
  // Client-Status-Hook mit Echtzeit-Updates
  const { 
    clients, 
    systemStatus, 
    isLoading, 
    isError, 
    error, 
    refreshData, 
    isAutoRefreshEnabled, 
    toggleAutoRefresh,
    lastUpdated
  } = useClientStatus({ pollingInterval });

  // Gefilterte Clients basierend auf der Suche
  const filteredClients = useMemo(() => {
    if (!searchQuery.trim()) return clients;
    
    const query = searchQuery.toLowerCase();
    return clients.filter(client => 
      client.name.toLowerCase().includes(query) || 
      client.description?.toLowerCase().includes(query) ||
      client.email?.toLowerCase().includes(query) ||
      client.public_key.toLowerCase().includes(query) ||
      client.allowed_ips.some(ip => ip.toLowerCase().includes(query))
    );
  }, [clients, searchQuery]);

  // Sortiere Clients: Online zuerst, dann nach Namen
  const sortedClients = useMemo(() => {
    return [...filteredClients].sort((a, b) => {
      // Zuerst nach Online-Status sortieren
      if (a.is_active && !b.is_active) return -1;
      if (!a.is_active && b.is_active) return 1;
      
      // Dann nach Namen sortieren
      return a.name.localeCompare(b.name);
    });
  }, [filteredClients]);

  // Event-Handler
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
  };

  const handleRefresh = () => {
    refreshData();
    showSnackbar('Daten werden aktualisiert...');
  };

  const handleDownloadConfig = (clientId: number) => {
    if (onDownloadConfig) {
      onDownloadConfig(clientId);
      showSnackbar('Konfiguration wird heruntergeladen...');
    }
  };

  const handleDeleteClient = (clientId: number) => {
    if (onDeleteClient) {
      onDeleteClient(clientId);
      showSnackbar('Client wird gelöscht...');
    }
  };

  const handleEditClient = (clientId: number) => {
    if (onEditClient) {
      onEditClient(clientId);
    }
  };

  const showSnackbar = (message: string) => {
    setSnackbarMessage(message);
    setSnackbarOpen(true);
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  return (
    <Box>
      {/* Fehleranzeige */}
      {isError && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }}
        >
          Fehler beim Laden der Daten: {error?.message || 'Unbekannter Fehler'}
        </Alert>
      )}
      
      {/* Aktionsleiste */}
      <Paper sx={{ p: 2, mb: 3, borderRadius: 2 }}>
        <Box sx={{ 
          display: 'flex', 
          flexDirection: { xs: 'column', sm: 'row' }, 
          justifyContent: 'space-between', 
          alignItems: { xs: 'stretch', sm: 'center' }
        }}>
          <Box sx={{ display: 'flex', mb: { xs: 2, sm: 0 } }}>
            {onAddClient && (
              <Button 
                variant="contained" 
                color="primary" 
                startIcon={<AddIcon />}
                onClick={onAddClient}
                sx={{ 
                  borderRadius: 50, 
                  textTransform: 'none'
                }}
              >
                Client hinzufügen
              </Button>
            )}
            
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={handleRefresh}
              sx={{ 
                ml: 1, 
                borderRadius: 50, 
                textTransform: 'none'
              }}
            >
              Aktualisieren
            </Button>
          </Box>
          
          <TextField
            placeholder="Suche..."
            size="small"
            value={searchQuery}
            onChange={handleSearchChange}
            sx={{ 
              width: { xs: '100%', sm: 300 },
              '& .MuiOutlinedInput-root': {
                borderRadius: 50
              }
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Box>
      </Paper>
      
      <Grid container spacing={3}>
        {/* System-Status-Panel */}
        <Grid item xs={12} lg={4}>
          <SystemStatusPanel 
            systemStatus={systemStatus}
            isLoading={isLoading}
            isError={isError}
            error={error}
            isAutoRefreshEnabled={isAutoRefreshEnabled}
            onToggleAutoRefresh={toggleAutoRefresh}
            onRefresh={refreshData}
            lastUpdated={lastUpdated}
          />
        </Grid>
        
        {/* Client-Karten */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3, borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom>
              Clients ({sortedClients.length})
            </Typography>
            
            <Divider sx={{ mb: 3 }} />
            
            {sortedClients.length === 0 ? (
              <Box sx={{ py: 4, textAlign: 'center' }}>
                <Typography variant="body1" color="text.secondary">
                  {isLoading 
                    ? 'Lade Clients...' 
                    : searchQuery 
                      ? 'Keine Clients gefunden, die dem Suchbegriff entsprechen.' 
                      : 'Keine Clients vorhanden.'}
                </Typography>
              </Box>
            ) : (
              <Grid container spacing={3}>
                {sortedClients.map(client => (
                  <Grid item xs={12} md={6} key={client.id}>
                    <ClientStatusCard 
                      client={client}
                      onDownload={handleDownloadConfig}
                      onDelete={handleDeleteClient}
                      onEdit={handleEditClient}
                    />
                  </Grid>
                ))}
              </Grid>
            )}
          </Paper>
        </Grid>
      </Grid>
      
      {/* Benachrichtigungen */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
        message={snackbarMessage}
      />
    </Box>
  );
}; 