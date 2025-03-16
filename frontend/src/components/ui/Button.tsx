import React from 'react';
import { 
  Button as MuiButton, 
  ButtonProps as MuiButtonProps,
  CircularProgress,
  styled
} from '@mui/material';

export interface ButtonProps extends Omit<MuiButtonProps, 'color'> {
  color?: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info' | 'inherit';
  isLoading?: boolean;
  loadingText?: string;
  fullWidth?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'start' | 'end';
}

const StyledButton = styled(MuiButton, {
  shouldForwardProp: (prop) => 
    prop !== 'isLoading' && 
    prop !== 'loadingText' && 
    prop !== 'icon' && 
    prop !== 'iconPosition'
})<ButtonProps>(({ theme }) => ({
  borderRadius: theme.shape.borderRadius,
  textTransform: 'none',
  fontWeight: 500,
  boxShadow: 'none',
  '&:hover': {
    boxShadow: 'none',
  },
  '&.MuiButton-sizeLarge': {
    padding: '10px 22px',
    fontSize: '1rem',
  },
  '&.MuiButton-sizeSmall': {
    padding: '4px 10px',
    fontSize: '0.8125rem',
  },
  '&.Mui-disabled': {
    opacity: 0.7,
  }
}));

const Button: React.FC<ButtonProps> = ({
  children,
  isLoading = false,
  loadingText,
  disabled,
  icon,
  iconPosition = 'start',
  ...props
}) => {
  const buttonContent = isLoading ? (
    <>
      <CircularProgress
        size={20}
        color="inherit"
        sx={{ mr: loadingText ? 1 : 0 }}
      />
      {loadingText}
    </>
  ) : (
    <>
      {icon && iconPosition === 'start' && (
        <span style={{ marginRight: 8, display: 'flex', alignItems: 'center' }}>
          {icon}
        </span>
      )}
      {children}
      {icon && iconPosition === 'end' && (
        <span style={{ marginLeft: 8, display: 'flex', alignItems: 'center' }}>
          {icon}
        </span>
      )}
    </>
  );

  return (
    <StyledButton
      disabled={disabled || isLoading}
      {...props}
    >
      {buttonContent}
    </StyledButton>
  );
};

export default Button; 