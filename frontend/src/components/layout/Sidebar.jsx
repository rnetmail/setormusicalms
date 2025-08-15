import { Link, NavLink, useLocation } from 'react-router-dom';
import { FaTimes, FaHome, FaMusic, FaCalendarAlt, FaBullhorn, FaHistory, FaImages, FaChevronDown } from 'react-icons/fa';
import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';

const Sidebar = ({ isOpen }) => {
  const [expandedMenus, setExpandedMenus] = useState({ coral: false, orquestra: false });
  const location = useLocation();
  const { currentUser, logout } = useAuth();
  
  // Reset expanded menus when location changes
  useEffect(() => {
    const pathname = location.pathname;
    
    // Automatically expand the menu that matches the current path
    if (pathname.includes('/coral')) {
      setExpandedMenus({ coral: true, orquestra: false });
    } else if (pathname.includes('/orquestra')) {
      setExpandedMenus({ coral: false, orquestra: true });
    }
  }, [location]);

  const toggleMenu = (menu) => {
    setExpandedMenus(prev => ({ 
      ...prev, 
      [menu]: !prev[menu] 
    }));
  };

  // Special styling for admin section
  const isAdminRoute = location.pathname.startsWith('/gestao');

  return (
    <div 
      className={`fixed top-0 left-0 h-full w-64 bg-white shadow-lg transform ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      } transition-transform duration-300 ease-in-out z-50 flex flex-col lg:relative lg:translate-x-0 ${
        isAdminRoute ? 'lg:w-64 border-r border-gray-200' : 'lg:w-0 lg:hidden'
      }`}
    >
      {/* Mobile Close Button */}
      <div className="p-4 border-b flex items-center justify-between lg:hidden">
        <Link to="/" className="font-bold text-blue-900 text-lg">Setor Musical</Link>
        <button className="text-gray-500 hover:text-gray-700">
          <FaTimes size={24} />
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 pt-5 pb-4 overflow-y-auto">
        <div className="px-4 space-y-1">
          {isAdminRoute ? (
            // Admin Navigation
            <>
              <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                Painel Administrativo
              </h3>
              
              <NavLink 
                to="/gestao" 
                end
                className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                }`}
              >
                <FaHome className="mr-3 text-gray-500" /> Dashboard
              </NavLink>
              
              <div className="pt-2 mt-2 border-t border-gray-200">
                <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Coral
                </h3>
                
                <NavLink 
                  to="/gestao/repertorio/coral" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaMusic className="mr-3 text-gray-500" /> Repertório
                </NavLink>
                
                <NavLink 
                  to="/gestao/recados/coral" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaBullhorn className="mr-3 text-gray-500" /> Recados
                </NavLink>
                
                <NavLink 
                  to="/gestao/agenda/coral" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaCalendarAlt className="mr-3 text-gray-500" /> Agenda
                </NavLink>
                
                <NavLink 
                  to="/gestao/galeria/coral" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaImages className="mr-3 text-gray-500" /> Galeria
                </NavLink>
              </div>
              
              <div className="pt-2 mt-2 border-t border-gray-200">
                <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Orquestra de Violões
                </h3>
                
                <NavLink 
                  to="/gestao/repertorio/orquestra" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaMusic className="mr-3 text-gray-500" /> Repertório
                </NavLink>
                
                <NavLink 
                  to="/gestao/recados/orquestra" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaBullhorn className="mr-3 text-gray-500" /> Recados
                </NavLink>
                
                <NavLink 
                  to="/gestao/agenda/orquestra" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaCalendarAlt className="mr-3 text-gray-500" /> Agenda
                </NavLink>
                
                <NavLink 
                  to="/gestao/galeria/orquestra" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaImages className="mr-3 text-gray-500" /> Galeria
                </NavLink>
              </div>
              
              <div className="pt-2 mt-2 border-t border-gray-200">
                <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Administração
                </h3>
                
                <NavLink 
                  to="/gestao/usuarios" 
                  className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                    isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <FaHome className="mr-3 text-gray-500" /> Usuários
                </NavLink>
              </div>
            </>
          ) : (
            // Public Navigation
            <>
              <NavLink 
                to="/" 
                end
                className={({ isActive }) => `flex items-center px-3 py-2 text-sm font-medium rounded-md ${
                  isActive ? 'bg-blue-100 text-blue-900' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                }`}
              >
                <FaHome className="mr-3 text-gray-500" /> Início
              </NavLink>
              
              {/* Coral Section */}
              <div className="my-2">
                <button 
                  onClick={() => toggleMenu('coral')}
                  className={`w-full flex items-center justify-between px-3 py-2 text-sm font-medium rounded-md ${
                    location.pathname.includes('/coral') 
                      ? 'bg-blue-100 text-blue-900' 
                      : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <span>Coral</span>
                  <FaChevronDown 
                    className={`transition-transform transform ${expandedMenus.coral ? 'rotate-180' : ''}`} 
                    size={12} 
                  />
                </button>
                
                {expandedMenus.coral && (
                  <div className="pl-6 mt-1 space-y-1">
                    <NavLink 
                      to="/repertorio/coral" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Repertório
                    </NavLink>
                    
                    <NavLink 
                      to="/recados/coral" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Recados
                    </NavLink>
                    
                    <NavLink 
                      to="/agenda/coral" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Agenda
                    </NavLink>
                    
                    <NavLink 
                      to="/historia/coral" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      História
                    </NavLink>
                    
                    <NavLink 
                      to="/galeria/coral" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Vale a Pena Ver de Novo
                    </NavLink>
                  </div>
                )}
              </div>
              
              {/* Orquestra Section */}
              <div className="my-2">
                <button 
                  onClick={() => toggleMenu('orquestra')}
                  className={`w-full flex items-center justify-between px-3 py-2 text-sm font-medium rounded-md ${
                    location.pathname.includes('/orquestra') 
                      ? 'bg-blue-100 text-blue-900' 
                      : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                  }`}
                >
                  <span>Orquestra de Violões</span>
                  <FaChevronDown 
                    className={`transition-transform transform ${expandedMenus.orquestra ? 'rotate-180' : ''}`} 
                    size={12} 
                  />
                </button>
                
                {expandedMenus.orquestra && (
                  <div className="pl-6 mt-1 space-y-1">
                    <NavLink 
                      to="/repertorio/orquestra" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Repertório
                    </NavLink>
                    
                    <NavLink 
                      to="/recados/orquestra" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Recados
                    </NavLink>
                    
                    <NavLink 
                      to="/agenda/orquestra" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Agenda
                    </NavLink>
                    
                    <NavLink 
                      to="/historia/orquestra" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      História
                    </NavLink>
                    
                    <NavLink 
                      to="/galeria/orquestra" 
                      className={({ isActive }) => `block px-3 py-2 text-sm font-medium rounded-md ${
                        isActive ? 'bg-blue-50 text-blue-800' : 'text-gray-600 hover:bg-gray-50 hover:text-blue-800'
                      }`}
                    >
                      Vale a Pena Ver de Novo
                    </NavLink>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </nav>
      
      {/* User Section for Mobile - Only shown when not in admin section */}
      {!isAdminRoute && (
        <div className="border-t border-gray-200 p-4 lg:hidden">
          {currentUser ? (
            <div>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-medium">
                    {currentUser.name.charAt(0)}
                  </div>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-900">{currentUser.name}</p>
                  <Link to="/gestao" className="text-xs font-medium text-blue-600 hover:text-blue-800">
                    Painel de Controle
                  </Link>
                </div>
              </div>
              <div className="mt-3">
                <button
                  onClick={logout}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none"
                >
                  Sair
                </button>
              </div>
            </div>
          ) : (
            <Link 
              to="/gestao/login"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none"
            >
              Área Restrita
            </Link>
          )}
        </div>
      )}
    </div>
  );
};

export default Sidebar;