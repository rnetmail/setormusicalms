import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Search, Calendar, Clock, MapPin, Users } from 'lucide-react';

const AgendaPage = () => {
  const { area } = useParams();
  const [searchTerm, setSearchTerm] = useState('');

  // Dados de exemplo da agenda por contexto
  const agendaData = {
    geral: [
      {
        id: 1,
        titulo: 'Ensaio Geral - Coral e Orquestra',
        data: '2025-08-15',
        horario: '14:00',
        local: 'Salão Principal',
        tipo: 'ensaio',
        descricao: 'Ensaio preparatório conjunto para a apresentação especial. Comparecimento obrigatório.',
        participantes: 'Coral e Orquestra'
      },
      {
        id: 2,
        titulo: 'Apresentação Beneficente',
        data: '2025-08-25',
        horario: '19:00',
        local: 'Centro de Convenções - Campo Grande',
        tipo: 'apresentacao',
        descricao: 'Apresentação especial em evento beneficente com repertório completo.',
        participantes: 'Coral e Orquestra'
      },
      {
        id: 3,
        titulo: 'Assembleia do Setor Musical',
        data: '2025-08-20',
        horario: '19:00',
        local: 'Auditório Principal',
        tipo: 'reuniao',
        descricao: 'Assembleia para discussão do planejamento anual e votação de propostas.',
        participantes: 'Todos os integrantes'
      }
    ],
    coral: [
      {
        id: 4,
        titulo: 'Ensaio Coral - Naipes Femininos',
        data: '2025-08-18',
        horario: '15:30',
        local: 'Sala de Ensaios',
        tipo: 'ensaio',
        descricao: 'Ensaio específico para Sopranos e Contraltos. Foco no repertório sacro.',
        participantes: 'Sopranos e Contraltos'
      },
      {
        id: 5,
        titulo: 'Workshop de Técnica Vocal',
        data: '2025-08-22',
        horario: '09:00',
        local: 'Auditório Principal',
        tipo: 'workshop',
        descricao: 'Workshop com professora convidada sobre técnicas avançadas de canto coral.',
        participantes: 'Todo o Coral'
      },
      {
        id: 6,
        titulo: 'Ensaio Naipes Masculinos',
        data: '2025-08-24',
        horario: '16:00',
        local: 'Sala de Ensaios',
        tipo: 'ensaio',
        descricao: 'Ensaio específico para Tenores e Baixos. Trabalho de harmonização.',
        participantes: 'Tenores e Baixos'
      }
    ],
    orquestra: [
      {
        id: 7,
        titulo: 'Ensaio Grupos Iniciantes',
        data: '2025-08-19',
        horario: '16:00',
        local: 'Sala de Música',
        tipo: 'ensaio',
        descricao: 'Ensaio focado nos Grupos Novos e Grupo 1 para aperfeiçoamento técnico.',
        participantes: 'Grupo Novos e Grupo 1'
      },
      {
        id: 8,
        titulo: 'Masterclass de Violão',
        data: '2025-08-23',
        horario: '10:00',
        local: 'Auditório Principal',
        tipo: 'workshop',
        descricao: 'Masterclass com violonista convidado sobre técnicas avançadas.',
        participantes: 'Toda a Orquestra'
      },
      {
        id: 9,
        titulo: 'Ensaio Grupos Avançados',
        data: '2025-08-26',
        horario: '17:00',
        local: 'Sala de Música',
        tipo: 'ensaio',
        descricao: 'Ensaio específico para Grupos 2, 3 e 4. Repertório de alta complexidade.',
        participantes: 'Grupos 2, 3 e 4'
      }
    ]
  };

  const getCurrentEventos = () => {
    if (area === 'coral') return agendaData.coral;
    if (area === 'orquestra') return agendaData.orquestra;
    return agendaData.geral;
  };

  const eventos = getCurrentEventos();

  const filteredEventos = eventos.filter(evento =>
    evento.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    evento.descricao.toLowerCase().includes(searchTerm.toLowerCase()) ||
    evento.local.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getTipoClass = (tipo) => {
    switch (tipo) {
      case 'ensaio':
        return 'bg-blue-500 text-white';
      case 'apresentacao':
        return 'bg-purple-500 text-white';
      case 'workshop':
        return 'bg-green-500 text-white';
      case 'reuniao':
        return 'bg-orange-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getDayOfWeek = (dateString) => {
    const days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
    return days[new Date(dateString).getDay()];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Agenda de Eventos
            {area && (
              <span className="block text-2xl text-blue-600 font-normal mt-2 capitalize">
                {area === 'coral' ? 'do Coral' : area === 'orquestra' ? 'da Orquestra' : ''}
              </span>
            )}
          </h1>
          <p className="text-lg text-gray-600">
            {area === 'coral' 
              ? 'Ensaios e atividades específicas do Coral'
              : area === 'orquestra'
              ? 'Ensaios e atividades específicas da Orquestra'
              : 'Confira os próximos ensaios, apresentações e atividades do Setor Musical'
            }
          </p>
        </div>

        {/* Busca */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar eventos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Lista de Eventos */}
        <div className="space-y-6">
          {filteredEventos.length === 0 ? (
            <div className="bg-white rounded-lg shadow-lg p-12 text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Calendar className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-600 mb-2">
                Nenhum evento encontrado
              </h3>
              <p className="text-gray-500">
                Não há eventos que correspondam à sua busca.
              </p>
            </div>
          ) : (
            filteredEventos.map((evento) => (
              <div key={evento.id} className="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <span className={`px-4 py-2 rounded-full text-sm font-semibold ${getTipoClass(evento.tipo)}`}>
                        {evento.tipo.charAt(0).toUpperCase() + evento.tipo.slice(1)}
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">
                        {new Date(evento.data).getDate()}
                      </div>
                      <div className="text-sm text-gray-500">
                        {new Date(evento.data).toLocaleDateString('pt-BR', { month: 'short' })}
                      </div>
                    </div>
                  </div>

                  <h2 className="text-xl font-bold text-gray-800 mb-3">
                    {evento.titulo}
                  </h2>

                  <p className="text-gray-600 mb-4 leading-relaxed">
                    {evento.descricao}
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="flex items-center text-sm text-gray-600">
                      <Calendar className="w-4 h-4 mr-2 text-blue-500" />
                      <div>
                        <div className="font-medium">{formatDate(evento.data)}</div>
                        <div className="text-xs text-gray-500">{getDayOfWeek(evento.data)}</div>
                      </div>
                    </div>

                    <div className="flex items-center text-sm text-gray-600">
                      <Clock className="w-4 h-4 mr-2 text-blue-500" />
                      <span className="font-medium">{evento.horario}</span>
                    </div>

                    <div className="flex items-center text-sm text-gray-600">
                      <MapPin className="w-4 h-4 mr-2 text-blue-500" />
                      <span className="font-medium">{evento.local}</span>
                    </div>
                  </div>

                  <div className="border-t border-gray-200 pt-4">
                    <div className="flex items-center text-sm text-gray-600">
                      <Users className="w-4 h-4 mr-2 text-green-500" />
                      <span>
                        <span className="font-medium">Participantes:</span> {evento.participantes}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default AgendaPage;