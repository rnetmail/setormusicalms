// frontend/src/App.tsx
// Versão 13 - 29/07/2025 05:40 - Define as rotas públicas e privadas da aplicação

import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

// Importa as páginas
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/admin/AdminDashboard';
import LoadingSpinner from './components/LoadingSpinner';

// Componente para proteger rotas que exigem autenticação
const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    // Mostra um spinner enquanto verifica o estado de autenticação
    return <LoadingSpinner />;
  }

  // Se estiver autenticado, renderiza a página solicitada.
  // Caso contrário, redireciona para a página de login.
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

const App: React.FC = () => {
  return (
    <Routes>
      {/* Rota pública principal */}
      <Route path="/" element={<HomePage />} />
      
      {/* Rota pública de login */}
      <Route path="/login" element={<LoginPage />} />

      {/* Rotas protegidas dentro de /gestao */}
      <Route path="/gestao" element={<ProtectedRoute />}>
        {/* A rota /gestao em si renderizará o AdminDashboard */}
        <Route index element={<AdminDashboard />} />
        {/* Você pode adicionar outras sub-rotas de gestão aqui se necessário */}
        {/* Ex: <Route path="outra-pagina" element={<OutraPaginaAdmin />} /> */}
      </Route>

      {/* Rota para lidar com páginas não encontradas */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;
