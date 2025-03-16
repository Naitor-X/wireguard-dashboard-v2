import React from 'react';
import { Box, Tooltip, Typography } from '@mui/material';
import { Circle as CircleIcon } from '@mui/icons-material';

export type StatusType = 'online' | 'offline' | 'warning' | 'unknown';

interface StatusIndicatorProps {
  status: StatusType;
  label?: string;
  showLabel?: boolean;
  size?: 'small' | 'medium' | 'large';
  tooltipPlacement?: 'top' | 'bottom' | 'left' | 'right';
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  label,
  showLabel = false,
  size = 'medium',
  tooltipPlacement = 'top',
}) => {
  // Status-spezifische Konfigurationen
  const statusConfig = {
    online: {
      color: '#12B76A',
      shadowColor: 'rgba(18, 183, 106, 0.5)',
      label: label || 'Online',
    },
    offline: {
      color: '#F04438',
      shadowColor: 'rgba(240, 68, 56, 0.5)',
      label: label || 'Offline',
    },
    warning: {
      color: '#F79009',
      shadowColor: 'rgba(247, 144, 9, 0.5)',
      label: label || 'Warnung',
    },
    unknown: {
      color: '#98A2B3',
      shadowColor: 'rgba(152, 162, 179, 0.5)',
      label: label || 'Unbekannt',
    },
  };

  // Größenkonfiguration
  const sizeConfig = {
    small: {
      iconSize: 8,
      textVariant: 'caption' as const,
      spacing: 0.5,
    },
    medium: {
      iconSize: 12,
      textVariant: 'body2' as const,
      spacing: 1,
    },
    large: {
      iconSize: 16,
      textVariant: 'body1' as const,
      spacing: 1.5,
    },
  };

  const config = statusConfig[status];
  const sizeProps = sizeConfig[size];

  const indicator = (
    <CircleIcon
      sx={{
        fontSize: sizeProps.iconSize,
        color: config.color,
        filter: `drop-shadow(0px 0px 4px ${config.shadowColor})`,
      }}
    />
  );

  return (
    <Tooltip title={config.label} placement={tooltipPlacement}>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        {indicator}
        {showLabel && (
          <Typography
            variant={sizeProps.textVariant}
            sx={{ ml: sizeProps.spacing, color: config.color }}
          >
            {config.label}
          </Typography>
        )}
      </Box>
    </Tooltip>
  );
}; 