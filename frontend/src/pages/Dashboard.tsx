import { Grid, Paper, Typography } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';

interface DashboardData {
  // Hier kommen später die Typen für die Dashboard-Daten
  status: string;
}

export default function Dashboard() {
  const { data, isLoading, error } = useQuery<DashboardData>({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const response = await apiClient.get('/api/dashboard');
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <Typography variant="body1">
        Lade Dashboard...
      </Typography>
    );
  }

  if (error) {
    return (
      <Typography variant="body1" color="error">
        Fehler beim Laden des Dashboards
      </Typography>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
      </Grid>
      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Status
          </Typography>
          <Typography variant="body1">
            {data?.status}
          </Typography>
        </Paper>
      </Grid>
    </Grid>
  );
} 