import React from 'react';
import { Box, Typography, Button, Paper, Alert, AlertTitle } from '@mui/material';
import { ErrorOutline, Refresh } from '@mui/icons-material';

interface ErrorDisplayProps {
  title?: string;
  message?: string;
  error?: Error | string;
  onRetry?: () => void;
  showDetails?: boolean;
  severity?: 'error' | 'warning' | 'info';
  fullPage?: boolean;
}

const ErrorDisplay: React.FC<ErrorDisplayProps> = ({
  title = 'Ein Fehler ist aufgetreten',
  message = 'Beim Laden der Daten ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.',
  error,
  onRetry,
  showDetails = process.env.NODE_ENV === 'development',
  severity = 'error',
  fullPage = false
}) => {
  const errorMessage = typeof error === 'string' ? error : error?.message;
  const errorStack = typeof error !== 'string' ? error?.stack : undefined;

  const content = (
    <Box sx={{ width: '100%', maxWidth: fullPage ? 600 : '100%' }}>
      {fullPage ? (
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <ErrorOutline color="error" sx={{ fontSize: 60, mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            {title}
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            {message}
          </Typography>
          
          {showDetails && errorMessage && (
            <Alert severity={severity} sx={{ mt: 2, textAlign: 'left' }}>
              <AlertTitle>Fehlerdetails</AlertTitle>
              {errorMessage}
              {errorStack && (
                <Box 
                  component="pre" 
                  sx={{ 
                    mt: 1, 
                    fontSize: '0.75rem', 
                    whiteSpace: 'pre-wrap',
                    overflow: 'auto',
                    maxHeight: 200
                  }}
                >
                  {errorStack}
                </Box>
              )}
            </Alert>
          )}
          
          {onRetry && (
            <Button
              variant="contained"
              color="primary"
              startIcon={<Refresh />}
              onClick={onRetry}
              sx={{ mt: 3 }}
            >
              Erneut versuchen
            </Button>
          )}
        </Paper>
      ) : (
        <Alert 
          severity={severity}
          action={onRetry && (
            <Button 
              color="inherit" 
              size="small" 
              onClick={onRetry}
              startIcon={<Refresh />}
            >
              Wiederholen
            </Button>
          )}
          sx={{ mb: 2 }}
        >
          <AlertTitle>{title}</AlertTitle>
          {message}
          {showDetails && errorMessage && (
            <Box sx={{ mt: 1, fontSize: '0.875rem' }}>
              <strong>Details:</strong> {errorMessage}
            </Box>
          )}
        </Alert>
      )}
    </Box>
  );

  if (fullPage) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '400px',
          p: 3
        }}
      >
        {content}
      </Box>
    );
  }

  return content;
};

export default ErrorDisplay; 