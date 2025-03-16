import React from 'react';
import { Box, Typography, Tooltip } from '@mui/material';
import { AccessTime as AccessTimeIcon } from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';
import { de } from 'date-fns/locale';

interface LastActivityDisplayProps {
  lastHandshake?: string;
  showIcon?: boolean;
  variant?: 'short' | 'full';
  color?: string;
}

export const LastActivityDisplay: React.FC<LastActivityDisplayProps> = ({
  lastHandshake,
  showIcon = true,
  variant = 'short',
  color = 'text.secondary',
}) => {
  if (!lastHandshake) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {showIcon && <AccessTimeIcon fontSize="small" sx={{ mr: 0.5, color }} />}
        <Typography variant="body2" color={color}>
          Keine Aktivität
        </Typography>
      </Box>
    );
  }

  const handshakeDate = new Date(lastHandshake);
  const isValid = !isNaN(handshakeDate.getTime());

  if (!isValid) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {showIcon && <AccessTimeIcon fontSize="small" sx={{ mr: 0.5, color }} />}
        <Typography variant="body2" color={color}>
          Ungültiges Datum
        </Typography>
      </Box>
    );
  }

  const formattedTime = formatDistanceToNow(handshakeDate, { 
    addSuffix: true,
    locale: de 
  });

  const fullDateTime = handshakeDate.toLocaleString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });

  return (
    <Tooltip title={fullDateTime}>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {showIcon && <AccessTimeIcon fontSize="small" sx={{ mr: 0.5, color }} />}
        <Typography variant="body2" color={color}>
          {variant === 'short' ? formattedTime : fullDateTime}
        </Typography>
      </Box>
    </Tooltip>
  );
}; 