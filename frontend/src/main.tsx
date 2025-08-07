// frontend/src/main.tsx
// Versão 12 - 29/07/2025 05:35 - Configura o ponto de entrada da aplicação React
// /frontend/src/main.tsx

import React from 'react';
import ReactDOM from 'react-dom/client';

// CORREÇÃO: Garante que o caminho relativo e a extensão do arquivo estejam corretos.
import App from './App.tsx'; 

import './index.css'; // Importa o CSS global

// Renderiza a aplicação no elemento 'root' do seu index.html
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
