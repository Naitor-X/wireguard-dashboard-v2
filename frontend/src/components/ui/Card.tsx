import React from 'react';
import { 
  Card as MuiCard, 
  CardProps as MuiCardProps, 
  CardContent, 
  CardHeader, 
  CardActions,
  Typography,
  Divider,
  Box,
  styled
} from '@mui/material';

// Eigene Schnittstelle für zusätzliche Props
interface CustomCardProps {
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  headerAction?: React.ReactNode;
  footer?: React.ReactNode;
  dividers?: boolean;
  noPadding?: boolean;
  contentSx?: React.CSSProperties;
}

// Kombinierte Schnittstelle für alle Props
export type CardProps = MuiCardProps & CustomCardProps;

const StyledCard = styled(MuiCard, {
  shouldForwardProp: (prop) => 
    prop !== 'noPadding' && 
    prop !== 'dividers' && 
    prop !== 'contentSx' &&
    prop !== 'title' &&
    prop !== 'subtitle' &&
    prop !== 'headerAction' &&
    prop !== 'footer'
})<CardProps>(({ theme }) => ({
  borderRadius: theme.shape.borderRadius,
  overflow: 'hidden',
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.shadows[4],
  },
}));

const Card: React.FC<CardProps> = ({
  children,
  title,
  subtitle,
  headerAction,
  footer,
  dividers = false,
  noPadding = false,
  elevation = 1,
  contentSx,
  ...props
}) => {
  return (
    <StyledCard elevation={elevation} {...props}>
      {title && (
        <>
          <CardHeader
            title={
              typeof title === 'string' ? (
                <Typography variant="h6" component="div">
                  {title}
                </Typography>
              ) : (
                title
              )
            }
            subheader={subtitle}
            action={headerAction}
            sx={{ pb: dividers ? 1 : undefined }}
          />
          {dividers && <Divider />}
        </>
      )}
      
      <CardContent 
        sx={{ 
          flexGrow: 1, 
          p: noPadding ? 0 : undefined,
          '&:last-child': { pb: noPadding ? 0 : undefined },
          ...contentSx
        }}
      >
        {children}
      </CardContent>
      
      {footer && (
        <>
          {dividers && <Divider />}
          <CardActions sx={{ p: 2 }}>
            {typeof footer === 'string' ? (
              <Typography variant="body2" color="text.secondary">
                {footer}
              </Typography>
            ) : (
              <Box sx={{ width: '100%' }}>{footer}</Box>
            )}
          </CardActions>
        </>
      )}
    </StyledCard>
  );
};

export default Card; 