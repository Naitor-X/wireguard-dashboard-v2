import React, { useMemo } from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  Button, 
  Divider,
  Chip,
  CardActions,
  Tooltip
} from '@mui/material';
import { 
  Download as DownloadIcon, 
  Delete as DeleteIcon,
  Edit as EditIcon,
  ContentCopy as CopyIcon
} from '@mui/icons-material';
import { ClientData } from '../../hooks/useClientStatus';
import { StatusIndicator } from './StatusIndicator';
import { LastActivityDisplay } from './LastActivityDisplay';
import { TrafficStatistics } from './TrafficStatistics';

interface ClientStatusCardProps {
  client: ClientData;
  onDownload?: (clientId: number) => void;
  onDelete?: (clientId: number) => void;
  onEdit?: (clientId: number) => void;
  onCopyConfig?: (clientId: number) => void;
  elevation?: number;
}

export const ClientStatusCard: React.FC<ClientStatusCardProps> = ({
  client,
  onDownload,
  onDelete,
  onEdit,
  onCopyConfig,
  elevation = 1,
}) => {
  // Bestimme den Status basierend auf last_handshake
  const status = useMemo(() => {
    if (!client.is_active) return 'offline';
    
    if (client.last_handshake) {
      const lastHandshake = new Date(client.last_handshake);
      const now = new Date();
      const diffMinutes = (now.getTime() - lastHandshake.getTime()) / (1000 * 60);
      
      // Wenn der letzte Handshake weniger als 5 Minuten her ist, ist der Client online
      if (diffMinutes < 5) return 'online';
      
      // Wenn der letzte Handshake zwischen 5 und 30 Minuten her ist, ist der Client im Warnzustand
      if (diffMinutes < 30) return 'warning';
    }
    
    return 'offline';
  }, [client.is_active, client.last_handshake]);

  // Formatiere die erlaubten IPs für die Anzeige
  const formattedIPs = useMemo(() => {
    if (!client.allowed_ips || client.allowed_ips.length === 0) {
      return 'Keine IPs zugewiesen';
    }
    
    return client.allowed_ips.join(', ');
  }, [client.allowed_ips]);

  // Kopiere den Public Key in die Zwischenablage
  const handleCopyPublicKey = () => {
    navigator.clipboard.writeText(client.public_key);
  };

  return (
    <Card 
      elevation={elevation} 
      sx={{ 
        borderRadius: 2, 
        position: 'relative',
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)',
          transform: 'translateY(-2px)'
        }
      }}
    >
      <Box 
        sx={{ 
          position: 'absolute', 
          top: 16, 
          right: 16,
          zIndex: 1
        }}
      >
        <StatusIndicator status={status} />
      </Box>
      
      <CardContent sx={{ pt: 3, pb: 1 }}>
        <Typography variant="h6" gutterBottom sx={{ pr: 3, fontWeight: 500 }}>
          {client.name}
        </Typography>
        
        {client.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {client.description}
          </Typography>
        )}
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Letzte Aktivität:
          </Typography>
          <LastActivityDisplay lastHandshake={client.last_handshake} />
        </Box>
        
        <Divider sx={{ my: 2 }} />
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Traffic:
          </Typography>
          <TrafficStatistics 
            transferRx={client.transfer_rx} 
            transferTx={client.transfer_tx}
            variant="compact"
          />
        </Box>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Erlaubte IPs:
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {client.allowed_ips && client.allowed_ips.map((ip, index) => (
              <Chip 
                key={index} 
                label={ip} 
                size="small" 
                sx={{ 
                  bgcolor: 'rgba(25, 118, 210, 0.1)',
                  color: 'primary.main',
                  fontSize: '0.75rem'
                }} 
              />
            ))}
          </Box>
        </Box>
        
        <Box sx={{ mb: 1 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Public Key:
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Tooltip title="Kopieren">
              <Button 
                size="small" 
                onClick={handleCopyPublicKey}
                sx={{ p: 0, minWidth: 'auto', mr: 1 }}
              >
                <CopyIcon fontSize="small" />
              </Button>
            </Tooltip>
            <Typography 
              variant="body2" 
              sx={{ 
                fontFamily: 'monospace', 
                fontSize: '0.75rem',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
              }}
            >
              {client.public_key}
            </Typography>
          </Box>
        </Box>
      </CardContent>
      
      <CardActions sx={{ px: 2, pb: 2 }}>
        {onDownload && (
          <Button
            size="small"
            startIcon={<DownloadIcon />}
            onClick={() => onDownload(client.id)}
            sx={{ 
              textTransform: 'none', 
              color: 'primary.main',
            }}
          >
            Herunterladen
          </Button>
        )}
        
        {onEdit && (
          <Button
            size="small"
            startIcon={<EditIcon />}
            onClick={() => onEdit(client.id)}
            sx={{ 
              textTransform: 'none', 
              color: 'info.main',
            }}
          >
            Bearbeiten
          </Button>
        )}
        
        {onDelete && (
          <Button
            size="small"
            startIcon={<DeleteIcon />}
            onClick={() => onDelete(client.id)}
            sx={{ 
              textTransform: 'none', 
              color: 'error.main',
              ml: 'auto'
            }}
          >
            Löschen
          </Button>
        )}
      </CardActions>
    </Card>
  );
}; 