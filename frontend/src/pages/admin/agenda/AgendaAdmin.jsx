import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Edit, Trash2, Eye, Calendar, Clock, MapPin } from 'lucide-react';

const AgendaAdmin = ({ context = 'geral' }) => {
  const [activeTab, setActiveTab] = useState(context);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setTimeout(() => {
          const mockEvents = {
            geral: [
              {
                id: 1,
                title: 'Ensaio Geral - Coral e Orquestra',
                description: 'Ensaio preparatório conjunto para apresentação especial',
                date: '2025-08-15',
                time: '14:00',
                location: 'Salão Principal',
                type: 'ensaio'
              },
              {
                id: 2,
                title: 'Apresentação Beneficente',
                description: 'Apresentação especial em evento beneficente',
                date: '2025-08-25',
                time: '19:00',
                location: 'Centro de Convenções',
                type: 'apresentacao'
              }
            ],
            coral: [
              {
                id: 3,
                title: 'Ensaio Coral - Naipes Femininos',
                description: 'Ensaio específico para Sopranos e Contraltos',
                date: '2025-08-18',
                time: '15:30',
                location: 'Sala de Ensaios',
                type: 'ensaio'
              },
              {
                id: 4,
                title: 'Workshop de Técnica Vocal',
                description: 'Workshop com professora convidada',
                date: '2025-08-22',
                time: '09:00',
                location: 'Auditório Principal',
                type: 'workshop'
              }
            ],
            orquestra: [
              {
                id: 5,
                title: 'Ensaio Grupos Iniciantes',
                description: 'Ensaio focado nos Grupos Novos e Grupo 1',
                date: '2025-08-19',
                time: '16:00',
                location: 'Sala de Música',
                type: 'ensaio'
              },
              {
                id: 6,
                title: 'Masterclass de Violão',
                description: 'Masterclass com violonista convidado',
                date: '2025-08-23',
                time: '10:00',
                location: 'Auditório Principal',
                type: 'workshop'
              }
            ]
          };

          setEvents(mockEvents);
          setLoading(false);
        }, 500);
      } catch (error) {
        console.error('Erro ao carregar eventos:', error);
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este evento?')) {
      try {
        const updatedEvents = { ...events };
        updatedEvents[context] = updatedEvents[context].filter(item => item.id !== id);
        setEvents(updatedEvents);
      } catch (error) {
        console.error('Erro ao excluir evento:', error);
        alert('Erro ao excluir evento');
      }
    }
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR');
  };

  const getTypeColor = (type) => {
    switch(type) {
      case 'ensaio': return 'bg-blue-100 text-blue-800';
      case 'apresentacao': return 'bg-purple-100 text-purple-800';
      case 'workshop': return 'bg-green-100 text-green-800';
      case 'reuniao': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const tabs = [
    { id: 'geral', label: 'Setor Musical', icon: '🎵' },
    { id: 'coral', label: 'Coral', icon: '👥' },
    { id: 'orquestra', label: 'Orquestra', icon: '🎸' }
  ];

  const currentEvents = events[context] || [];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">
          Gerenciar Agenda - {context === 'geral' ? 'Setor Musical' : context === 'coral' ? 'Coral' : 'Orquestra'}
        </h1>
        <button
          onClick={() => alert('Modal de novo evento (em desenvolvimento)')}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors"
        >
          <Plus className="w-4 h-4 mr-2" />
          Novo Evento
        </button>
      </div>



      {loading ? (
        <div className="animate-pulse space-y-4">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Evento
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tipo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Data/Hora
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Local
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {currentEvents.map((event) => (
                  <tr key={event.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{event.title}</div>
                      <div className="text-sm text-gray-500 truncate max-w-xs">
                        {event.description}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(event.type)}`}>
                        {event.type.charAt(0).toUpperCase() + event.type.slice(1)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex items-center mb-1">
                        <Calendar className="w-4 h-4 mr-1" />
                        {formatDate(event.date)}
                      </div>
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        {event.time}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex items-center">
                        <MapPin className="w-4 h-4 mr-1" />
                        {event.location}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-3">
                        <Link
                          to={`/admin/agenda/${event.id}`}
                          className="text-blue-600 hover:text-blue-900 transition-colors"
                        >
                          <Eye className="w-4 h-4" />
                        </Link>
                        <Link
                          to={`/admin/agenda/${event.id}/editar`}
                          className="text-indigo-600 hover:text-indigo-900 transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                        </Link>
                        <button
                          onClick={() => handleDelete(event.id)}
                          className="text-red-600 hover:text-red-900 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {currentEvents.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-500">
                <Calendar className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Nenhum evento encontrado para {context === 'geral' ? 'Setor Musical' : context === 'coral' ? 'Coral' : 'Orquestra'}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AgendaAdmin;