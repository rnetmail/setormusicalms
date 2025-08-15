import React from 'react';
import { Calendar, Users, Award, Heart } from 'lucide-react';

const HistoriaPage = () => {
  const marcos = [
    {
      ano: '1995',
      titulo: 'Fundação do Setor Musical',
      descricao: 'Criação oficial do Setor Musical Mokiti Okada em Mato Grosso do Sul, com o objetivo de elevar sentimentos através da música.',
      tipo: 'fundacao'
    },
    {
      ano: '1998',
      titulo: 'Primeiro Coral',
      descricao: 'Formação do primeiro grupo coral com 15 integrantes, focado em música sacra e canções que transmitem paz e harmonia.',
      tipo: 'coral'
    },
    {
      ano: '2003',
      titulo: 'Criação da Orquestra de Violões',
      descricao: 'Início da Orquestra de Violões, expandindo o alcance musical do setor e oferecendo nova modalidade de participação.',
      tipo: 'orquestra'
    },
    {
      ano: '2008',
      titulo: 'Primeira Grande Apresentação',
      descricao: 'Primeira apresentação conjunta do Coral e Orquestra no Teatro Glauce Rocha, marcando um novo patamar artístico.',
      tipo: 'apresentacao'
    },
    {
      ano: '2012',
      titulo: 'Estruturação por Grupos',
      descricao: 'Organização da Orquestra em grupos por níveis de habilidade e do Coral em naipes, permitindo melhor desenvolvimento técnico.',
      tipo: 'estrutura'
    },
    {
      ano: '2018',
      titulo: '100ª Apresentação',
      descricao: 'Celebração da centésima apresentação oficial do Setor Musical, consolidando sua importância na comunidade.',
      tipo: 'marco'
    },
    {
      ano: '2025',
      titulo: 'Era Digital',
      descricao: 'Lançamento da plataforma digital para facilitar o acesso ao repertório e comunicação entre os integrantes.',
      tipo: 'tecnologia'
    }
  ];

  const getIconAndStyle = (tipo) => {
    switch (tipo) {
      case 'fundacao':
        return { icon: Heart, color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' };
      case 'coral':
        return { icon: Users, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200' };
      case 'orquestra':
        return { icon: Users, color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200' };
      case 'apresentacao':
        return { icon: Award, color: 'text-purple-600', bg: 'bg-purple-50', border: 'border-purple-200' };
      default:
        return { icon: Calendar, color: 'text-gray-600', bg: 'bg-gray-50', border: 'border-gray-200' };
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Nossa História
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Conheça a trajetória do Setor Musical Mokiti Okada MS e os marcos que construíram nossa história de mais de 25 anos dedicados à música.
          </p>
        </div>

        {/* Linha do Tempo */}
        <div className="relative">
          {/* Linha vertical */}
          <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 top-0 bottom-0 w-0.5 bg-blue-200"></div>
          
          <div className="space-y-12">
            {marcos.map((marco, index) => {
              const { icon: IconComponent, color, bg, border } = getIconAndStyle(marco.tipo);
              const isEven = index % 2 === 0;
              
              return (
                <div key={marco.ano} className={`flex items-center ${isEven ? 'md:flex-row' : 'md:flex-row-reverse'}`}>
                  {/* Conteúdo */}
                  <div className={`w-full md:w-5/12 ${isEven ? 'md:pr-8' : 'md:pl-8'}`}>
                    <div className={`${bg} ${border} border rounded-xl p-6 shadow-md ml-12 md:ml-0`}>
                      <div className="flex items-center mb-3">
                        <div className={`p-2 ${bg} ${border} border rounded-lg mr-3`}>
                          <IconComponent className={`w-5 h-5 ${color}`} />
                        </div>
                        <span className="text-2xl font-bold text-gray-800">{marco.ano}</span>
                      </div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-2">
                        {marco.titulo}
                      </h3>
                      <p className="text-gray-600">
                        {marco.descricao}
                      </p>
                    </div>
                  </div>

                  {/* Marcador central */}
                  <div className="absolute left-4 md:left-1/2 transform md:-translate-x-1/2 w-8 h-8 bg-white border-4 border-blue-500 rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  </div>

                  {/* Espaço para o outro lado (apenas visível em desktop) */}
                  <div className="hidden md:block w-5/12"></div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Seção de Valores */}
        <div className="mt-16 bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
            Nossos Valores
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="p-4 bg-blue-100 rounded-full inline-flex mb-4">
                <Heart className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Amor pela Música</h3>
              <p className="text-gray-600">
                Cultivamos o amor genuíno pela arte musical como forma de expressão espiritual e emocional.
              </p>
            </div>
            
            <div className="text-center">
              <div className="p-4 bg-green-100 rounded-full inline-flex mb-4">
                <Users className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">União e Harmonia</h3>
              <p className="text-gray-600">
                Promovemos a união entre os integrantes, criando um ambiente harmonioso e colaborativo.
              </p>
            </div>
            
            <div className="text-center">
              <div className="p-4 bg-purple-100 rounded-full inline-flex mb-4">
                <Award className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Excelência Artística</h3>
              <p className="text-gray-600">
                Buscamos constantemente a melhoria técnica e artística em nossas apresentações.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HistoriaPage;