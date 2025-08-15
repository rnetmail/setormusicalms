import { useState, useEffect } from 'react';
import { FaBullhorn, FaCalendarAlt, FaImages, FaBookOpen } from 'react-icons/fa';

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

const SetorMusicalDashboard = () => {
  const [stats, setStats] = useState({
    recados: 12,
    eventos: 8,
    galerias: 15,
    historias: 5
  });

  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setActivities([
        {
          icon: <FaBullhorn className="text-white" />,
          iconBg: 'bg-yellow-500',
          title: 'Novo recado publicado',
          description: 'Comunicado sobre mudanças no cronograma de ensaios.',
          time: 'Hoje, 14:30'
        },
        {
          icon: <FaCalendarAlt className="text-white" />,
          iconBg: 'bg-green-500',
          title: 'Evento agendado',
          description: 'Apresentação especial no próximo domingo.',
          time: 'Ontem, 16:15'
        },
        {
          icon: <FaImages className="text-white" />,
          iconBg: 'bg-pink-500',
          title: 'Fotos adicionadas',
          description: 'Nova galeria da apresentação de dezembro.',
          time: '2 dias atrás, 10:45'
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
        <h2 className="text-2xl font-bold text-gray-900">Dashboard - Setor Musical</h2>
        <p className="mt-1 text-sm text-gray-500">
          Visão geral das atividades do Setor Musical
        </p>
      </div>

      {/* Stats Grid */}
      <div className="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard 
          title="Recados" 
          value={stats.recados} 
          icon={FaBullhorn} 
          color="bg-yellow-500" 
          linkAction={() => {}}
        />
        <StatCard 
          title="Eventos" 
          value={stats.eventos} 
          icon={FaCalendarAlt} 
          color="bg-green-500" 
          linkAction={() => {}}
        />
        <StatCard 
          title="Galeria" 
          value={stats.galerias} 
          icon={FaImages} 
          color="bg-pink-500" 
          linkAction={() => {}}
        />
        <StatCard 
          title="História" 
          value={stats.historias} 
          icon={FaBookOpen} 
          color="bg-purple-500" 
          linkAction={() => {}}
        />
      </div>

      {/* Recent Activity */}
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
      </div>
    </div>
  );
};

export default SetorMusicalDashboard;