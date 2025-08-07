// /frontend/index.tsx

import React from 'react';
import ReactDOM from 'react-dom/client';

// CORREÇÃO: O caminho para App.tsx deve incluir o diretório 'src'.
import App from './src/App.tsx';

// O resto do arquivo permanece o mesmo...
// (Pode haver outras importações aqui, como o seu CSS)

const rootElement = document.getElementById('root');
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("Elemento com id 'root' não encontrado no DOM.");
}
