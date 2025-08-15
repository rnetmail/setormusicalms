import React from 'react';
import { Link } from 'react-router-dom';
import { Music, Users, ArrowRight } from 'lucide-react';

const AreaSelection = () => {
  const areas = [
    {
      id: 'coral',
      titulo: 'Coral',
      descricao: 'Acesse o repertório do seu naipe',
      naipes: ['Sopranos', 'Contraltos', 'Tenores', 'Baixos'],
      icon: Users,
      gradient: 'from-blue-500 to-purple-600',
      hoverGradient: 'from-blue-600 to-purple-700'
    },
    {
      id: 'orquestra',
      titulo: 'Orquestra de Violões',
      descricao: 'Acesse o repertório do seu grupo',
      naipes: ['Grupo Novos', 'Grupo 1', 'Grupo 2', 'Grupo 3', 'Grupo 4'],
      icon: Music,
      gradient: 'from-green-500 to-teal-600',
      hoverGradient: 'from-green-600 to-teal-700'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-6">
      <div className="max-w-4xl mx-auto">
        {/* Cabeçalho */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
            Selecione sua Área
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
            Escolha entre Coral ou Orquestra de Violões para acessar o repertório específico do seu grupo
          </p>
        </div>

        {/* Cards das Áreas */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {areas.map((area) => (
            <Link
              key={area.id}
              to={`/repertorio/${area.id}`}
              className="group block"
            >
              <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform group-hover:-translate-y-2 overflow-hidden border border-gray-100">
                {/* Header com gradiente */}
                <div className={`bg-gradient-to-r ${area.gradient} group-hover:bg-gradient-to-r group-hover:${area.hoverGradient} p-8 text-white transition-all duration-300`}>
                  <div className="flex items-center justify-between mb-4">
                    <area.icon className="w-12 h-12 group-hover:scale-110 transition-transform duration-300" />
                    <ArrowRight className="w-8 h-8 group-hover:translate-x-1 transition-transform duration-300" />
                  </div>
                  <h2 className="text-2xl md:text-3xl font-bold mb-2">
                    {area.titulo}
                  </h2>
                  <p className="text-lg opacity-90">
                    {area.descricao}
                  </p>
                </div>

                {/* Conteúdo */}
                <div className="p-8">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">
                    {area.id === 'coral' ? 'Naipes disponíveis:' : 'Grupos disponíveis:'}
                  </h3>
                  
                  <div className="space-y-3">
                    {area.naipes.map((naipe, index) => (
                      <div 
                        key={index}
                        className="flex items-center p-3 bg-gray-50 rounded-lg group-hover:bg-gray-100 transition-colors duration-300"
                      >
                        <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                        <span className="text-gray-700 font-medium">{naipe}</span>
                      </div>
                    ))}
                  </div>

                  <div className="mt-6 text-center">
                    <span className="inline-flex items-center text-blue-600 font-semibold group-hover:text-blue-700 transition-colors">
                      Acessar Repertório
                      <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Seção de Ajuda */}
        <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-100">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Music className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-2xl font-bold text-gray-800 mb-4">
              Como funciona?
            </h3>
            <div className="max-w-2xl mx-auto text-gray-600 space-y-3">
              <p>
                <strong>1.</strong> Escolha sua área (Coral ou Orquestra de Violões)
              </p>
              <p>
                <strong>2.</strong> Selecione seu naipe ou grupo específico
              </p>
              <p>
                <strong>3.</strong> Acesse partituras, áudios e vídeos do repertório
              </p>
            </div>
            
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-blue-800 text-sm">
                💡 <strong>Dica:</strong> Todos os materiais estão organizados por nível de dificuldade 
                e incluem partituras para download, áudios para treino e vídeos demonstrativos.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AreaSelection;