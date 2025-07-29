// frontend/src/pages/HomePage.tsx
// Versão Final - Página de Boas-Vindas

import React from 'react';
import { Link } from 'react-router-dom';
import { Box, Typography, Button, Container } from '@mui/material';

const HomePage: React.FC = () => {
    return (
        <Container
            component="main"
            maxWidth="sm"
            sx={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '100vh', // Ocupa a altura inteira da tela
                textAlign: 'center'
            }}
        >
            <Box>
                <Typography variant="h2" component="h1" gutterBottom>
                    Setor Musical Mokiti Okada MS
                </Typography>
                <Typography variant="h5" color="text.secondary" paragraph>
                    Bem-vindo ao portal do nosso setor musical.
                </Typography>
                <Button
                    component={Link}
                    to="/login"
                    variant="contained"
                    size="large"
                    sx={{ mt: 4 }}
                >
                    Acessar Área de Gestão
                </Button>
            </Box>
        </Container>
    );
};

export default HomePage;
