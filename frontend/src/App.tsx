// App.tsx
// Versão 21 17/07/2025 17:32
import React from 'react';
// ATUALIZAÇÃO: Importa BrowserRouter em vez de HashRouter.
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { GroupType } from './types';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import ContentPage from './pages/ContentPage';
import HistoriaPage from './pages/HistoriaPage';
import GaleriaPage from './pages/GaleriaPage';
import LoginPage from './pages/admin/LoginPage';
import AdminDashboard from './pages/admin/AdminDashboard';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { isAuthenticated } = useAuth();
    if (!isAuthenticated) {
        return <Navigate to="/gestao/login" replace />;
    }
    return <>{children}</>;
};

const App: React.FC = () => {
    return (
        // ATUALIZAÇÃO: Utiliza BrowserRouter para URLs limpas (ex: /coral/repertorio).
        <BrowserRouter>
            <AuthProvider>
                <Routes>
                    {/* Public Routes */}
                    <Route path="/" element={<Layout><HomePage /></Layout>} />
                    <Route path="/coral/repertorio" element={<Layout><ContentPage group={GroupType.Coral} contentType="repertorio" /></Layout>} />
                    <Route path="/coral/agenda" element={<Layout><ContentPage group={GroupType.Coral} contentType="agenda" /></Layout>} />
                    <Route path="/coral/recados" element={<Layout><ContentPage group={GroupType.Coral} contentType="recados" /></Layout>} />
                    <Route path="/coral/historia" element={<Layout><HistoriaPage group={GroupType.Coral} /></Layout>} />
                    <Route path="/coral/galeria" element={<Layout><GaleriaPage group={GroupType.Coral} /></Layout>} />

                    <Route path="/orquestra/repertorio" element={<Layout><ContentPage group={GroupType.Orquestra} contentType="repertorio" /></Layout>} />
                    <Route path="/orquestra/agenda" element={<Layout><ContentPage group={GroupType.Orquestra} contentType="agenda" /></Layout>} />
                    <Route path="/orquestra/recados" element={<Layout><ContentPage group={GroupType.Orquestra} contentType="recados" /></Layout>} />
                    <Route path="/orquestra/historia" element={<Layout><HistoriaPage group={GroupType.Orquestra} /></Layout>} />
                    <Route path="/orquestra/galeria" element={<Layout><GaleriaPage group={GroupType.Orquestra} /></Layout>} />

                    {/* Admin Routes */}
                    <Route path="/gestao/login" element={<LoginPage />} />
                    <Route path="/gestao" element={
                        <ProtectedRoute>
                            <AdminDashboard />
                        </ProtectedRoute>
                    } />
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    );
};

export default App;
