import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { FaMusic, FaBullhorn, FaCalendarAlt, FaImages, FaBookOpen, FaUsers, FaCog } from 'react-icons/fa';

// Import dashboard components
import SetorMusicalDashboard from './dashboards/SetorMusicalDashboard';
import CoralDashboard from './dashboards/CoralDashboard';
import OrquestraDashboard from './dashboards/OrquestraDashboard';
import GeralDashboard from './dashboards/GeralDashboard';

// Import CRUD components
import RecadosAdmin from './recados/RecadosAdmin';
import AgendaAdmin from './agenda/AgendaAdmin';
import GaleriaAdmin from './galeria/GaleriaAdmin';
import HistoriaAdmin from './historia/HistoriaAdmin';
import RepertorioAdmin from './repertorio/RepertorioAdmin';
import UsuariosAdmin from './usuarios/UsuariosAdmin';

const Admin = () => {
  const { isAuthenticated, loading, user } = useAuth();
  const [activeTab, setActiveTab] = useState('setor-musical');
  const [activeSubTab, setActiveSubTab] = useState('dashboard');

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/admin/login" replace />;
  }

  const tabs = [
    { id: 'setor-musical', label: 'Setor Musical', icon: FaMusic },
    { id: 'coral', label: 'Coral', icon: FaMusic },
    { id: 'orquestra', label: 'Orquestra', icon: FaMusic },
    { id: 'geral', label: 'Geral', icon: FaCog }
  ];

  const getSubTabs = (tabId) => {
    const commonTabs = [
      { id: 'dashboard', label: 'Dashboard', icon: null },
      { id: 'recados', label: 'Recados', icon: FaBullhorn },
      { id: 'agenda', label: 'Agenda', icon: FaCalendarAlt },
      { id: 'galeria', label: 'Galeria', icon: FaImages },
      { id: 'historia', label: 'História', icon: FaBookOpen }
    ];

    switch (tabId) {
      case 'setor-musical':
        return commonTabs;
      case 'coral':
      case 'orquestra':
        return [
          { id: 'dashboard', label: 'Dashboard', icon: null },
          { id: 'repertorio', label: 'Repertório', icon: FaMusic },
          ...commonTabs.slice(1)
        ];
      case 'geral':
        return [
          { id: 'dashboard', label: 'Dashboard', icon: null },
          { id: 'usuarios', label: 'Usuários', icon: FaUsers }
        ];
      default:
        return [];
    }
  };

  const renderContent = () => {
    const context = activeTab === 'setor-musical' ? 'geral' : activeTab;
    
    if (activeSubTab === 'dashboard') {
      switch (activeTab) {
        case 'setor-musical':
          return <SetorMusicalDashboard />;
        case 'coral':
          return <CoralDashboard />;
        case 'orquestra':
          return <OrquestraDashboard />;
        case 'geral':
          return <GeralDashboard />;
        default:
          return <SetorMusicalDashboard />;
      }
    }

    switch (activeSubTab) {
      case 'repertorio':
        return <RepertorioAdmin context={context} />;
      case 'recados':
        return <RecadosAdmin context={context} />;
      case 'agenda':
        return <AgendaAdmin context={context} />;
      case 'galeria':
        return <GaleriaAdmin context={context} />;
      case 'historia':
        return <HistoriaAdmin context={context} />;
      case 'usuarios':
        return <UsuariosAdmin />;
      default:
        return <SetorMusicalDashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Área de Gestão</h1>
              <p className="text-sm text-gray-600">Setor Musical Mokiti Okada MS</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Bem-vindo, {user?.username}</span>
              <a 
                href="/" 
                className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
              >
                Voltar ao Site
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id);
                    setActiveSubTab('dashboard');
                  }}
                  className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Sub Tabs */}
      <div className="bg-gray-50 border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-6">
            {getSubTabs(activeTab).map((subTab) => {
              const Icon = subTab.icon;
              return (
                <button
                  key={subTab.id}
                  onClick={() => setActiveSubTab(subTab.id)}
                  className={`flex items-center py-3 px-1 text-sm font-medium transition-colors ${
                    activeSubTab === subTab.id
                      ? 'text-blue-600 border-b-2 border-blue-500'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {Icon && <Icon className="w-4 h-4 mr-1" />}
                  {subTab.label}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        {renderContent()}
      </main>
    </div>
  );
};

export default Admin;