// frontend/src/components/LoadingSpinner.tsx

import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

/**
 * Um componente reutilizável que exibe um spinner de carregamento centralizado.
 * Ideal para ser mostrado enquanto os dados estão sendo buscados da API.
 */
const LoadingSpinner: React.FC = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '80vh', // Ocupa a maior parte da altura da tela
        width: '100%',
      }}
    >
      <CircularProgress size={60} /> {/* O spinner em si */}
      <Typography variant="h6" sx={{ mt: 2 }}>
        Carregando...
      </Typography>
    </Box>
  );
};

export default LoadingSpinner;
