// frontend/src/main.tsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // Importa estilos globais

// Encontra o elemento 'root' no seu index.html e renderiza a aplicação React dentro dele.
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
