import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import MainLayout from './components/layout/MainLayout';
import Home from './pages/Home';
import AreaSelection from './pages/AreaSelection';
import RepertorioPage from './pages/repertorio/RepertorioPage';
import RecadosPage from './pages/recados/RecadosPage';
import AgendaPage from './pages/agenda/AgendaPage';
import HistoriaPage from './pages/historia/HistoriaPage';
import GaleriaPage from './pages/galeria/GaleriaPage';
import Login from './pages/admin/Login';
import Admin from './pages/admin/Admin';
import CoralHome from './pages/coral/CoralHome';
import OrquestraHome from './pages/orquestra/OrquestraHome';
import CoralRepertorio from './pages/coral/RepertorioPage';
import OrquestraRepertorio from './pages/orquestra/RepertorioPage';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Home />} />
            <Route path="areas" element={<AreaSelection />} />
            <Route path="coral" element={<CoralHome />} />
            <Route path="coral/repertorio" element={<CoralRepertorio />} />
            <Route path="orquestra" element={<OrquestraHome />} />
            <Route path="orquestra/repertorio" element={<OrquestraRepertorio />} />
            <Route path="repertorio/:area" element={<RepertorioPage />} />
            <Route path="repertorio/:area/:grupo" element={<RepertorioPage />} />
            <Route path="recados" element={<RecadosPage />} />
            <Route path="recados/:area" element={<RecadosPage />} />
            <Route path="agenda" element={<AgendaPage />} />
            <Route path="agenda/:area" element={<AgendaPage />} />
            <Route path="historia" element={<HistoriaPage />} />
            <Route path="historia/:area" element={<HistoriaPage />} />
            <Route path="galeria" element={<GaleriaPage />} />
            <Route path="galeria/:area" element={<GaleriaPage />} />
          </Route>
          <Route path="/admin/login" element={<Login />} />
          <Route path="/admin/*" element={<Admin />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;