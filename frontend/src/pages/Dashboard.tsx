import { useState } from 'react';
import { 
  Grid, 
  Typography, 
  Box, 
  TextField, 
  InputAdornment,
  Button, 
  Card, 
  CardContent,
  useMediaQuery,
  useTheme,
  Paper,
  Container,
  Alert
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { 
  Search as SearchIcon, 
  Refresh as RefreshIcon, 
  Add as AddIcon, 
  Download as DownloadIcon,
  Delete as DeleteIcon,
  Circle as CircleIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { ClientsMonitoringPanel } from '../components/monitoring';

interface DashboardData {
  // Hier kommen später die Typen für die Dashboard-Daten
  status: string;
  serverStatus: 'online' | 'offline' | 'warning';
  activeClients: number;
  totalClients: number;
  adminClients: number;
  userClients: number;
  dataTransferred: string;
  lastUpdated: string;
}

interface Client {
  id: number;
  name: string;
  isAdmin: boolean;
  isOnline: boolean;
}

export default function Dashboard() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [searchQuery, setSearchQuery] = useState('');
  const [isRealTimeUpdating, setIsRealTimeUpdating] = useState(true);

  const { data, isLoading, error, refetch } = useQuery<DashboardData>({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const response = await apiClient.get('/api/dashboard');
      return response.data;
    },
    refetchInterval: isRealTimeUpdating ? 5000 : false,
  });

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
  };

  const toggleRealTimeUpdates = () => {
    setIsRealTimeUpdating(!isRealTimeUpdating);
  };

  const handleRefresh = () => {
    refetch();
  };

  const handleAddClient = () => {
    console.log('Client hinzufügen');
    // Implementierung für das Hinzufügen eines Clients
  };

  const handleEditClient = (clientId: number) => {
    console.log(`Bearbeiten von Client ${clientId}`);
    // Implementierung für das Bearbeiten eines Clients
  };

  const handleDeleteClient = (clientId: number) => {
    console.log(`Löschen von Client ${clientId}`);
    // Implementierung für das Löschen eines Clients
  };

  const handleDownloadConfig = (clientId: number) => {
    console.log(`Herunterladen von Client ${clientId}`);
    // Implementierung für das Herunterladen der Client-Konfiguration
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <Typography variant="body1">
          Lade Dashboard...
        </Typography>
      </Box>
    );
  }

  // Mock-Daten für die Demonstration
  const mockData: DashboardData = data || {
    status: 'Aktiv',
    serverStatus: 'online',
    activeClients: 12,
    totalClients: 25,
    adminClients: 5,
    userClients: 20,
    dataTransferred: '1.2 TB',
    lastUpdated: new Date().toLocaleString()
  };

  // Mock-Clients für die Demonstration
  const adminClients: Client[] = [
    { id: 1, name: 'Admin 1', isAdmin: true, isOnline: true },
    { id: 2, name: 'Admin', isAdmin: true, isOnline: false }
  ];

  const regularClients: Client[] = [
    { id: 3, name: 'Client 1', isAdmin: false, isOnline: false },
    { id: 4, name: 'Client 2', isAdmin: false, isOnline: true }
  ];

  return (
    <Container maxWidth="xl">
      {error && (
        <Alert 
          severity="error" 
          sx={{ 
            mb: 3, 
            display: 'flex', 
            alignItems: 'center',
            bgcolor: 'rgba(240, 68, 56, 0.1)',
            color: '#d32f2f'
          }}
          icon={<ErrorIcon />}
        >
          Fehler beim Laden des Dashboards: {(error as Error).message}
        </Alert>
      )}
      
      <Paper sx={{ p: 3, borderRadius: 2, boxShadow: '0px 2px 6px rgba(0, 0, 0, 0.05)' }}>
        <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 500, textAlign: 'center', color: '#1976d2' }}>
          Wireguard Dashboard
        </Typography>
        
        <ClientsMonitoringPanel 
          onAddClient={handleAddClient}
          onEditClient={handleEditClient}
          onDeleteClient={handleDeleteClient}
          onDownloadConfig={handleDownloadConfig}
          pollingInterval={5000}
        />
      </Paper>
    </Container>
  );
} 