// frontend/src/main.tsx
// Versão 12 - 29/07/2025 05:35 - Configura o ponto de entrada da aplicação React

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

// Cria um tema básico para o Material-UI
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Um azul padrão
    },
    secondary: {
      main: '#dc004e', // Um rosa padrão
    },
  },
});

// Busca o elemento root no HTML
const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Elemento 'root' não encontrado no DOM.");
}

const root = ReactDOM.createRoot(rootElement);

// Renderiza a aplicação
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Normaliza o CSS entre navegadores */}
      <BrowserRouter>
        <AuthProvider>
          <App />
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);
