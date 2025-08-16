// /frontend/vite.config.ts - Versão Final Corrigida

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react( )],
  
  // --- INÍCIO DA CORREÇÃO ---
  // Define o caminho base para a aplicação.
  // Usar um caminho relativo ('./') garante que os assets (CSS, JS, imagens)
  // sejam carregados corretamente, não importa em qual subdiretório ou domínio
  // a aplicação seja implantada. Isso resolve os erros de "tela branca"
  // e falhas de carregamento de recursos após o build.
  base: './',
  // --- FIM DA CORREÇÃO ---

  server: {
    // Configuração opcional para o servidor de desenvolvimento local
    port: 3000,
    open: true, // Abre o navegador automaticamente ao iniciar
    proxy: {
      // Proxy para o backend durante o desenvolvimento local
      '/api': {
        target: 'http://localhost:8000', // Endereço do seu backend FastAPI
        changeOrigin: true,
      },
    },
  },
} );
