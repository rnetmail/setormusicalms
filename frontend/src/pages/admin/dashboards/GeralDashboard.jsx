import { useState, useEffect } from 'react';
import { FaUsers, FaCog, FaChartBar, FaDatabase } from 'react-icons/fa';

const StatCard = ({ title, value, icon: Icon, color, linkAction }) => {
  return (
    <div 
      onClick={linkAction}
      className="block bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="p-5">
        <div className="flex items-center">
          <div className={`flex-shrink-0 rounded-full p-3 ${color}`}>
            <Icon className="text-white" size={20} />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-500">{title}</p>
            <p className="text-2xl font-semibold text-gray-900">{value}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const GeralDashboard = () => {
  const [stats, setStats] = useState({
    usuarios: 15,
    configuracoes: 8,
    backups: 5,
    relatorios: 12
  });

  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setActivities([
        {
          icon: <FaUsers className="text-white" />,
          iconBg: 'bg-purple-500',
          title: 'Novo usuário cadastrado',
          description: 'Administrador regional foi adicionado ao sistema.',
          time: 'Hoje, 13:15'
        },
        {
          icon: <FaCog className="text-white" />,
          iconBg: 'bg-gray-500',
          title: 'Configuração atualizada',
          description: 'Parâmetros de backup automático foram modificados.',
          time: 'Ontem, 09:30'
        },
        {
          icon: <FaDatabase className="text-white" />,
          iconBg: 'bg-green-500',
          title: 'Backup realizado',
          description: 'Backup automático do sistema executado com sucesso.',
          time: '2 dias atrás, 03:00'
        }
      ]);
      
      setIsLoading(false);
    };
    
    loadData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Dashboard - Configurações Gerais</h2>
        <p className="mt-1 text-sm text-gray-500">
          Painel de controle e configurações do sistema
        </p>
      </div>

      {/* Stats Grid */}
      <div className="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard 
          title="Usuários" 
          value={stats.usuarios} 
          icon={FaUsers} 
          color="bg-purple-500" 
          linkAction={() => {}}
        />
        <StatCard 
          title="Configurações" 
          value={stats.configuracoes} 
          icon={FaCog} 
          color="bg-gray-500" 
          linkAction={() => {}}
        />
        <StatCard 
          title="Backups" 
          value={stats.backups} 
          icon={FaDatabase} 
          color="bg-green-500" 
          linkAction={() => {}}
        />
        <StatCard 
          title="Relatórios" 
          value={stats.relatorios} 
          icon={FaChartBar} 
          color="bg-blue-500" 
          linkAction={() => {}}
        />
      </div>

      {/* System Status */}
      <div className="mb-8 bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-medium text-gray-900">Status do Sistema</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mx-auto mb-2"></div>
              <p className="text-sm font-medium text-gray-900">Sistema Online</p>
              <p className="text-xs text-gray-500">Funcionando normalmente</p>
            </div>
            <div className="text-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mx-auto mb-2"></div>
              <p className="text-sm font-medium text-gray-900">Backup Automático</p>
              <p className="text-xs text-gray-500">Último: 2 dias atrás</p>
            </div>
            <div className="text-center">
              <div className="w-3 h-3 bg-yellow-500 rounded-full mx-auto mb-2"></div>
              <p className="text-sm font-medium text-gray-900">Atualizações</p>
              <p className="text-xs text-gray-500">1 pendente</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h3 className="text-lg font-medium text-gray-900">Atividade Recente - Sistema</h3>
        </div>
        <ul className="divide-y divide-gray-200">
          {activities.map((activity, index) => (
            <li key={index} className="px-6 py-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <span className={`inline-flex items-center justify-center h-8 w-8 rounded-full ${activity.iconBg}`}>
                    {activity.icon}
                  </span>
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                  <p className="text-sm text-gray-500">{activity.description}</p>
                  <p className="mt-1 text-xs text-gray-400">{activity.time}</p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default GeralDashboard;