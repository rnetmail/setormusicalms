import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Search, Calendar, AlertCircle, Info, CheckCircle } from 'lucide-react';

const RecadosPage = () => {
  const { area } = useParams();
  const [searchTerm, setSearchTerm] = useState('');

  // Dados de exemplo dos recados por contexto
  const recadosData = {
    geral: [
      {
        id: 1,
        titulo: 'Assembleia Geral - Planejamento 2025',
        conteudo: 'Convocamos todos os integrantes do Setor Musical para assembleia geral no dia 20/08 às 19h para discussão do planejamento anual.',
        data: '2025-08-10',
        tipo: 'urgente',
        autor: 'Direção Geral do Setor Musical'
      },
      {
        id: 2,
        titulo: 'Novo Regulamento Interno',
        conteudo: 'Foi aprovado o novo regulamento interno do Setor Musical. Documento disponível na secretaria para consulta.',
        data: '2025-08-08',
        tipo: 'info',
        autor: 'Coordenação Geral'
      },
      {
        id: 3,
        titulo: 'Apresentação Conjunta - 25/08',
        conteudo: 'Apresentação especial com Coral e Orquestra no evento beneficente. Local: Centro de Convenções às 19h.',
        data: '2025-08-05',
        tipo: 'sucesso',
        autor: 'Direção Artística'
      }
    ],
    coral: [
      {
        id: 4,
        titulo: 'Ensaio Extra - Naipes Femininos',
        conteudo: 'Ensaio específico para Sopranos e Contraltos no sábado às 15h. Foco no repertório sacro.',
        data: '2025-08-12',
        tipo: 'urgente',
        autor: 'Regente do Coral'
      },
      {
        id: 5,
        titulo: 'Workshop de Técnica Vocal',
        conteudo: 'Professora convidada ministrará workshop sobre respiração e técnica vocal no dia 22/08.',
        data: '2025-08-09',
        tipo: 'info',
        autor: 'Coordenação do Coral'
      },
      {
        id: 6,
        titulo: 'Novo Repertório Coral',
        conteudo: 'Três novas peças foram adicionadas ao repertório do coral. Material disponível na área do coral.',
        data: '2025-08-07',
        tipo: 'info',
        autor: 'Regente do Coral'
      }
    ],
    orquestra: [
      {
        id: 7,
        titulo: 'Afinação dos Violões - Obrigatório',
        conteudo: 'Todos os integrantes devem trazer seus violões afinados. Haverá verificação antes do ensaio.',
        data: '2025-08-11',
        tipo: 'urgente',
        autor: 'Regente da Orquestra'
      },
      {
        id: 8,
        titulo: 'Cordas Novas Disponíveis',
        conteudo: 'Chegaram as cordas encomendadas. Interessados procurem a coordenação após o ensaio.',
        data: '2025-08-09',
        tipo: 'info',
        autor: 'Coordenação da Orquestra'
      },
      {
        id: 9,
        titulo: 'Ensaio por Grupos - Cronograma',
        conteudo: 'Grupo Novos: 14h, Grupo 1: 15h, Grupos 2-4: 16h. Cronograma da próxima semana.',
        data: '2025-08-06',
        tipo: 'info',
        autor: 'Regente da Orquestra'
      }
    ]
  };

  const getCurrentRecados = () => {
    if (area === 'coral') return recadosData.coral;
    if (area === 'orquestra') return recadosData.orquestra;
    return recadosData.geral;
  };

  const recados = getCurrentRecados();

  const filteredRecados = recados.filter(recado =>
    recado.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    recado.conteudo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    recado.autor.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getTipoIcon = (tipo) => {
    switch (tipo) {
      case 'urgente':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      case 'info':
        return <Info className="w-5 h-5 text-blue-500" />;
      case 'sucesso':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      default:
        return <Info className="w-5 h-5 text-gray-500" />;
    }
  };

  const getTipoBadgeClass = (tipo) => {
    switch (tipo) {
      case 'urgente':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'info':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'sucesso':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Recados e Comunicados
            {area && (
              <span className="block text-2xl text-blue-600 font-normal mt-2 capitalize">
                {area === 'coral' ? 'do Coral' : area === 'orquestra' ? 'da Orquestra' : ''}
              </span>
            )}
          </h1>
          <p className="text-lg text-gray-600">
            {area === 'coral' 
              ? 'Avisos específicos para os integrantes do Coral'
              : area === 'orquestra'
              ? 'Avisos específicos para os integrantes da Orquestra'
              : 'Fique por dentro dos avisos e informações importantes do Setor Musical'
            }
          </p>
        </div>

        {/* Busca */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar recados..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Lista de Recados */}
        <div className="space-y-6">
          {filteredRecados.length === 0 ? (
            <div className="bg-white rounded-lg shadow-lg p-12 text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Info className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-600 mb-2">
                Nenhum recado encontrado
              </h3>
              <p className="text-gray-500">
                Não há recados que correspondam à sua busca.
              </p>
            </div>
          ) : (
            filteredRecados.map((recado) => (
              <div key={recado.id} className="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      {getTipoIcon(recado.tipo)}
                      <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getTipoBadgeClass(recado.tipo)}`}>
                        {recado.tipo === 'urgente' ? 'Urgente' : 
                         recado.tipo === 'info' ? 'Informativo' : 'Sucesso'}
                      </span>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar className="w-4 h-4 mr-2" />
                      {formatDate(recado.data)}
                    </div>
                  </div>

                  <h2 className="text-xl font-bold text-gray-800 mb-3">
                    {recado.titulo}
                  </h2>

                  <p className="text-gray-600 mb-4 leading-relaxed">
                    {recado.conteudo}
                  </p>

                  <div className="border-t border-gray-200 pt-4">
                    <p className="text-sm text-gray-500">
                      <span className="font-medium">Publicado por:</span> {recado.autor}
                    </p>
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

export default RecadosPage;