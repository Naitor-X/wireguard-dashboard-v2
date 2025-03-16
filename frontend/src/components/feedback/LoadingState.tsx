import React from 'react';
import { Box, CircularProgress, Typography, Fade } from '@mui/material';

interface LoadingStateProps {
  message?: string;
  fullScreen?: boolean;
  size?: 'small' | 'medium' | 'large';
  delay?: number;
}

const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Wird geladen...',
  fullScreen = false,
  size = 'medium',
  delay = 300
}) => {
  const [visible, setVisible] = React.useState(delay === 0);

  React.useEffect(() => {
    if (delay === 0) return;
    
    const timer = setTimeout(() => {
      setVisible(true);
    }, delay);

    return () => clearTimeout(timer);
  }, [delay]);

  const getSizeValue = () => {
    switch (size) {
      case 'small': return 24;
      case 'large': return 60;
      default: return 40;
    }
  };

  const content = (
    <Fade in={visible} timeout={300}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          p: 3,
          height: fullScreen ? '100%' : 'auto'
        }}
      >
        <CircularProgress size={getSizeValue()} />
        {message && (
          <Typography
            variant="body1"
            color="text.secondary"
            sx={{ mt: 2 }}
          >
            {message}
          </Typography>
        )}
      </Box>
    </Fade>
  );

  if (fullScreen) {
    return (
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          zIndex: 9999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        {content}
      </Box>
    );
  }

  return content;
};

export default LoadingState; 