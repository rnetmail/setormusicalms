// frontend/src/pages/HomePage.tsx
// Versão 16 - 29/07/2025 05:55 - Cria a página inicial da aplicação

import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Typography,
  AppBar,
  Toolbar,
} from '@mui/material';

const HomePage: React.FC = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Setor Musical Mokiti Okada - MS
          </Typography>
          <Button color="inherit" component={RouterLink} to="/login">
            Acessar Área de Gestão
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ mt: 8, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Bem-vindo ao Portal do Setor Musical
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Explore nossos repertórios, agendas, história e muito mais.
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button
            variant="contained"
            size="large"
            component={RouterLink}
            to="/login"
          >
            Login de Administrador
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default HomePage;
