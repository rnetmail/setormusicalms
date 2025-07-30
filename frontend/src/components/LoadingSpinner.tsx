// frontend/src/components/LoadingSpinner.tsx
// Versão 17 - 29/07/2025 06:00 - Componente de loading para uso em toda a aplicação

import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

interface LoadingSpinnerProps {
  message?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  message = "Carregando..." 
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '200px',
        gap: 2,
      }}
    >
      <CircularProgress size={40} />
      <Typography variant="body1" color="text.secondary">
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingSpinner;
