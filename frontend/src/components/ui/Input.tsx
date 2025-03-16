import React, { forwardRef } from 'react';
import { 
  TextField, 
  TextFieldProps, 
  InputAdornment,
  FormHelperText,
  FormControl,
  InputLabel,
  styled
} from '@mui/material';

export interface InputProps extends Omit<TextFieldProps, 'variant'> {
  label?: string;
  error?: boolean;
  helperText?: React.ReactNode;
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
  fullWidth?: boolean;
  variant?: 'outlined' | 'filled' | 'standard';
}

const StyledTextField = styled(TextField)<InputProps>(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    borderRadius: theme.shape.borderRadius,
    transition: theme.transitions.create(['border-color', 'box-shadow']),
    '&:hover .MuiOutlinedInput-notchedOutline': {
      borderColor: theme.palette.primary.main,
    },
    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
      borderColor: theme.palette.primary.main,
      borderWidth: 2,
    },
  },
  '& .MuiInputLabel-root': {
    '&.Mui-focused': {
      color: theme.palette.primary.main,
    },
  },
}));

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ 
    label, 
    error, 
    helperText, 
    startIcon, 
    endIcon, 
    fullWidth = true, 
    variant = 'outlined',
    ...props 
  }, ref) => {
    return (
      <FormControl error={error} fullWidth={fullWidth}>
        {label && variant !== 'outlined' && (
          <InputLabel shrink>{label}</InputLabel>
        )}
        <StyledTextField
          ref={ref}
          label={variant === 'outlined' ? label : undefined}
          error={error}
          variant={variant}
          fullWidth={fullWidth}
          InputProps={{
            startAdornment: startIcon ? (
              <InputAdornment position="start">{startIcon}</InputAdornment>
            ) : undefined,
            endAdornment: endIcon ? (
              <InputAdornment position="end">{endIcon}</InputAdornment>
            ) : undefined,
          }}
          {...props}
        />
        {helperText && (
          <FormHelperText error={error}>{helperText}</FormHelperText>
        )}
      </FormControl>
    );
  }
);

Input.displayName = 'Input';

export default Input; 