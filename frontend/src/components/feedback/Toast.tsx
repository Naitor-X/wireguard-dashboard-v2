import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { 
  Snackbar, 
  Alert, 
  AlertProps, 
  Slide, 
  SlideProps, 
  Typography,
  Box,
  IconButton
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';

type ToastType = 'success' | 'error' | 'warning' | 'info';

interface ToastOptions {
  message: string;
  description?: string;
  type?: ToastType;
  duration?: number;
  position?: 'top' | 'bottom';
  horizontal?: 'left' | 'center' | 'right';
}

interface ToastContextType {
  showToast: (options: ToastOptions) => void;
  hideToast: () => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

const SlideTransition = (props: SlideProps) => {
  return <Slide {...props} direction="down" />;
};

export const ToastProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [description, setDescription] = useState<string | undefined>(undefined);
  const [type, setType] = useState<ToastType>('info');
  const [duration, setDuration] = useState(5000);
  const [position, setPosition] = useState<'top' | 'bottom'>('top');
  const [horizontal, setHorizontal] = useState<'left' | 'center' | 'right'>('center');

  const showToast = useCallback(({
    message,
    description,
    type = 'info',
    duration = 5000,
    position = 'top',
    horizontal = 'center'
  }: ToastOptions) => {
    setMessage(message);
    setDescription(description);
    setType(type);
    setDuration(duration);
    setPosition(position);
    setHorizontal(horizontal);
    setOpen(true);
  }, []);

  const hideToast = useCallback(() => {
    setOpen(false);
  }, []);

  const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  const getAlertSeverity = (): AlertProps['severity'] => {
    return type;
  };

  return (
    <ToastContext.Provider value={{ showToast, hideToast }}>
      {children}
      <Snackbar
        open={open}
        autoHideDuration={duration}
        onClose={handleClose}
        anchorOrigin={{ vertical: position, horizontal }}
        TransitionComponent={SlideTransition}
      >
        <Alert
          severity={getAlertSeverity()}
          variant="filled"
          sx={{ 
            width: '100%', 
            minWidth: '300px',
            alignItems: 'flex-start'
          }}
          action={
            <IconButton
              size="small"
              aria-label="close"
              color="inherit"
              onClick={handleClose}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          }
        >
          <Box>
            <Typography variant="subtitle2">{message}</Typography>
            {description && (
              <Typography variant="body2" sx={{ mt: 0.5, opacity: 0.9 }}>
                {description}
              </Typography>
            )}
          </Box>
        </Alert>
      </Snackbar>
    </ToastContext.Provider>
  );
};

export const useToast = (): ToastContextType => {
  const context = useContext(ToastContext);
  if (context === undefined) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

// Beispielverwendung:
// const { showToast } = useToast();
// showToast({
//   message: 'Erfolgreich gespeichert',
//   type: 'success',
//   duration: 3000
// });