import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaMusic, FaBullhorn, FaCalendarAlt, FaImages, FaUser, FaFileAlt } from 'react-icons/fa';
import { useAuth } from '../../context/AuthContext';

const StatCard = ({ title, value, icon: Icon, color, linkTo }) => {
  return (
    <Link to={linkTo} className="block bg-white rounded-lg shadow hover:shadow-md transition-shadow">
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
    </Link>
  );
};

const RecentActivity = ({ activities }) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="px-6 py-4 border-b">
        <h3 className="text-lg font-medium text-gray-900">Atividade Recente</h3>
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
      <div className="bg-gray-50 px-6 py-3">
        <Link to="#" className="text-sm font-medium text-blue-600 hover:text-blue-800">
          Ver todas as atividades
        </Link>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    repertorio: { coral: 0, orquestra: 0 },
    recados: { coral: 0, orquestra: 0 },
    eventos: { coral: 0, orquestra: 0 },
    galerias: { coral: 0, orquestra: 0 },
    usuarios: 0
  });
  
  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // In a real application, this would fetch data from an API
    const loadData = async () => {
      // Simulating API request delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Mock data
      setStats({
        repertorio: { coral: 24, orquestra: 18 },
        recados: { coral: 8, orquestra: 5 },
        eventos: { coral: 6, orquestra: 4 },
        galerias: { coral: 12, orquestra: 9 },
        usuarios: 15
      });
      
      setActivities([
        {
          icon: <FaMusic className="text-white" />,
          iconBg: 'bg-blue-500',
          title: 'Nova música adicionada',
          description: 'A música "Ave Maria" foi adicionada ao repertório do Coral.',
          time: 'Hoje, 09:45'
        },
        {
          icon: <FaBullhorn className="text-white" />,
          iconBg: 'bg-yellow-500',
          title: 'Novo recado publicado',
          description: 'O recado sobre o ensaio geral foi publicado para a Orquestra.',
          time: 'Ontem, 16:30'
        },
        {
          icon: <FaCalendarAlt className="text-white" />,
          iconBg: 'bg-green-500',
          title: 'Novo evento agendado',
          description: 'Apresentação no Teatro foi agendada para 15/12/2023.',
          time: '2 dias atrás, 10:15'
        },
        {
          icon: <FaFileAlt className="text-white" />,
          iconBg: 'bg-purple-500',
          title: 'Documento atualizado',
          description: 'A lista de contatos dos membros foi atualizada.',
          time: '3 dias atrás, 14:20'
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
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Bem-vindo, {user?.username}! Confira as estatísticas e atividades recentes.
        </p>
      </div>
      
      {/* Stats Grid */}
      <div className="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard 
          title="Repertório Coral" 
          value={stats.repertorio.coral} 
          icon={FaMusic} 
          color="bg-blue-500" 
          linkTo="/gestao/repertorio/coral" 
        />
        <StatCard 
          title="Repertório Orquestra" 
          value={stats.repertorio.orquestra} 
          icon={FaMusic} 
          color="bg-blue-700" 
          linkTo="/gestao/repertorio/orquestra" 
        />
        <StatCard 
          title="Recados Coral" 
          value={stats.recados.coral} 
          icon={FaBullhorn} 
          color="bg-yellow-500" 
          linkTo="/gestao/recados/coral" 
        />
        <StatCard 
          title="Recados Orquestra" 
          value={stats.recados.orquestra} 
          icon={FaBullhorn} 
          color="bg-yellow-700" 
          linkTo="/gestao/recados/orquestra" 
        />
        <StatCard 
          title="Eventos Coral" 
          value={stats.eventos.coral} 
          icon={FaCalendarAlt} 
          color="bg-green-500" 
          linkTo="/gestao/agenda/coral" 
        />
        <StatCard 
          title="Eventos Orquestra" 
          value={stats.eventos.orquestra} 
          icon={FaCalendarAlt} 
          color="bg-green-700" 
          linkTo="/gestao/agenda/orquestra" 
        />
        <StatCard 
          title="Galeria Coral" 
          value={stats.galerias.coral} 
          icon={FaImages} 
          color="bg-pink-500" 
          linkTo="/gestao/galeria/coral" 
        />
        <StatCard 
          title="Galeria Orquestra" 
          value={stats.galerias.orquestra} 
          icon={FaImages} 
          color="bg-pink-700" 
          linkTo="/gestao/galeria/orquestra" 
        />
        <StatCard 
          title="Usuários" 
          value={stats.usuarios} 
          icon={FaUser} 
          color="bg-purple-500" 
          linkTo="/gestao/usuarios" 
        />
      </div>
      
      {/* Recent Activity */}
      <div className="mb-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Atividade Recente</h2>
        <RecentActivity activities={activities} />
      </div>
      
      {/* Quick Actions */}
      <div className="mb-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Ações Rápidas</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Link 
            to="/gestao/repertorio/coral" 
            className="block p-4 bg-blue-50 border border-blue-100 rounded-lg text-blue-700 hover:bg-blue-100 transition"
          >
            <FaMusic className="mb-2" size={20} />
            <span className="font-medium">Adicionar Música</span>
          </Link>
          <Link 
            to="/gestao/recados/coral" 
            className="block p-4 bg-yellow-50 border border-yellow-100 rounded-lg text-yellow-700 hover:bg-yellow-100 transition"
          >
            <FaBullhorn className="mb-2" size={20} />
            <span className="font-medium">Publicar Recado</span>
          </Link>
          <Link 
            to="/gestao/agenda/coral" 
            className="block p-4 bg-green-50 border border-green-100 rounded-lg text-green-700 hover:bg-green-100 transition"
          >
            <FaCalendarAlt className="mb-2" size={20} />
            <span className="font-medium">Agendar Evento</span>
          </Link>
          <Link 
            to="/gestao/galeria/coral" 
            className="block p-4 bg-pink-50 border border-pink-100 rounded-lg text-pink-700 hover:bg-pink-100 transition"
          >
            <FaImages className="mb-2" size={20} />
            <span className="font-medium">Gerenciar Galeria</span>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;