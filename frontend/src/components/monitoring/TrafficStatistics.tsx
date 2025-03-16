import React from 'react';
import { Box, Typography, Paper, Grid, Tooltip } from '@mui/material';
import { 
  TrendingUp as UploadIcon, 
  TrendingDown as DownloadIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';

interface TrafficStatisticsProps {
  transferRx?: number;
  transferTx?: number;
  variant?: 'compact' | 'detailed';
  showLabels?: boolean;
  elevation?: number;
}

// Hilfsfunktion zur Formatierung der Datengrößen
const formatBytes = (bytes?: number, decimals = 2): string => {
  if (bytes === undefined || bytes === 0) return '0 B';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

export const TrafficStatistics: React.FC<TrafficStatisticsProps> = ({
  transferRx,
  transferTx,
  variant = 'compact',
  showLabels = true,
  elevation = 0,
}) => {
  const totalTransfer = (transferRx || 0) + (transferTx || 0);
  
  // Kompakte Variante (für Client-Karten)
  if (variant === 'compact') {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Tooltip title="Download">
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <DownloadIcon fontSize="small" sx={{ color: 'success.main', mr: 0.5 }} />
            <Typography variant="body2">{formatBytes(transferRx)}</Typography>
          </Box>
        </Tooltip>
        
        <Tooltip title="Upload">
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <UploadIcon fontSize="small" sx={{ color: 'info.main', mr: 0.5 }} />
            <Typography variant="body2">{formatBytes(transferTx)}</Typography>
          </Box>
        </Tooltip>
      </Box>
    );
  }
  
  // Detaillierte Variante (für Dashboard-Übersicht)
  return (
    <Paper 
      elevation={elevation} 
      sx={{ 
        p: 2, 
        borderRadius: 2,
        bgcolor: 'background.paper'
      }}
    >
      <Typography variant="h6" gutterBottom>
        <SpeedIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        Traffic-Statistiken
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={12} sm={4}>
          <Box sx={{ textAlign: 'center', p: 1 }}>
            <DownloadIcon sx={{ color: 'success.main', fontSize: 32, mb: 1 }} />
            <Typography variant="h6">{formatBytes(transferRx)}</Typography>
            {showLabels && (
              <Typography variant="body2" color="text.secondary">
                Download
              </Typography>
            )}
          </Box>
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <Box sx={{ textAlign: 'center', p: 1 }}>
            <UploadIcon sx={{ color: 'info.main', fontSize: 32, mb: 1 }} />
            <Typography variant="h6">{formatBytes(transferTx)}</Typography>
            {showLabels && (
              <Typography variant="body2" color="text.secondary">
                Upload
              </Typography>
            )}
          </Box>
        </Grid>
        
        <Grid item xs={12} sm={4}>
          <Box sx={{ textAlign: 'center', p: 1 }}>
            <SpeedIcon sx={{ color: 'primary.main', fontSize: 32, mb: 1 }} />
            <Typography variant="h6">{formatBytes(totalTransfer)}</Typography>
            {showLabels && (
              <Typography variant="body2" color="text.secondary">
                Gesamt
              </Typography>
            )}
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
}; 