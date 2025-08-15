import React, { useState } from 'react';
import { Play, Calendar, MapPin, Users, X } from 'lucide-react';

const GaleriaPage = () => {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [showVideoModal, setShowVideoModal] = useState(false);

  // Dados de exemplo da galeria
  const apresentacoes = [
    {
      id: 1,
      titulo: 'Concerto de Natal 2024',
      data: '2024-12-15',
      local: 'Igreja Central Mokiti Okada',
      participantes: 'Coral e Orquestra',
      videoUrl: 'https://www.youtube.com/watch?v=example-natal-2024',
      thumbnail: 'https://img.youtube.com/vi/example-natal-2024/maxresdefault.jpg',
      descricao: 'Apresentação especial de Natal com repertório sacro e canções natalinas.'
    },
    {
      id: 2,
      titulo: 'Evento Beneficente - Casa da Esperança',
      data: '2024-10-20',
      local: 'Centro de Convenções',
      participantes: 'Coral completo',
      videoUrl: 'https://www.youtube.com/watch?v=example-beneficente',
      thumbnail: 'https://img.youtube.com/vi/example-beneficente/maxresdefault.jpg',
      descricao: 'Participação em evento beneficente para arrecadação de fundos.'
    },
    {
      id: 3,
      titulo: 'Apresentação de Aniversário do Setor',
      data: '2024-08-25',
      local: 'Auditório Principal',
      participantes: 'Coral e Orquestra',
      videoUrl: 'https://www.youtube.com/watch?v=example-aniversario',
      thumbnail: 'https://img.youtube.com/vi/example-aniversario/maxresdefault.jpg',
      descricao: 'Celebração dos 29 anos do Setor Musical com repertório especial.'
    },
    {
      id: 4,
      titulo: 'Concerto de Primavera',
      data: '2024-09-21',
      local: 'Teatro Glauce Rocha',
      participantes: 'Orquestra de Violões',
      videoUrl: 'https://www.youtube.com/watch?v=example-primavera',
      thumbnail: 'https://img.youtube.com/vi/example-primavera/maxresdefault.jpg',
      descricao: 'Apresentação especial da Orquestra celebrando a chegada da primavera.'
    },
    {
      id: 5,
      titulo: 'Homenagem ao Dia das Mães',
      data: '2024-05-12',
      local: 'Salão de Eventos',
      participantes: 'Coral - Naipes Femininos',
      videoUrl: 'https://www.youtube.com/watch?v=example-maes',
      thumbnail: '/images/MothersDay.jpg',
      descricao: 'Apresentação especial em homenagem às mães da comunidade.'
    },
    {
      id: 6,
      titulo: 'Recital de Páscoa',
      data: '2024-03-30',
      local: 'Igreja Central',
      participantes: 'Coral e Orquestra',
      videoUrl: 'https://www.youtube.com/watch?v=example-pascoa',
      thumbnail: 'https://img.youtube.com/vi/example-pascoa/maxresdefault.jpg',
      descricao: 'Celebração da Páscoa com músicas que transmitem renovação e esperança.'
    }
  ];

  // Função para extrair ID do YouTube
  const getYouTubeId = (url) => {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'long',
      year: 'numeric'
    });
  };

  const handlePlayVideo = (videoUrl, titulo) => {
    const videoId = getYouTubeId(videoUrl);
    if (videoId) {
      setSelectedVideo({ id: videoId, title: titulo });
      setShowVideoModal(true);
    }
  };

  const closeVideoModal = () => {
    setShowVideoModal(false);
    setSelectedVideo(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Galeria de Apresentações
          </h1>
          <p className="text-lg text-gray-600">
            Reviva os momentos especiais das nossas apresentações e celebre conosco a beleza da música
          </p>
        </div>

        {/* Grade de Vídeos */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {apresentacoes.map((apresentacao) => (
            <div key={apresentacao.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
              {/* Thumbnail do Vídeo */}
              <div className="relative group cursor-pointer" onClick={() => handlePlayVideo(apresentacao.videoUrl, apresentacao.titulo)}>
                <div className="aspect-video bg-gray-200 flex items-center justify-center">
                  <div className="w-16 h-16 bg-black bg-opacity-20 rounded-full flex items-center justify-center group-hover:bg-opacity-40 transition-all duration-300">
                    <Play className="w-8 h-8 text-white ml-1" />
                  </div>
                </div>
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300"></div>
              </div>

              {/* Informações */}
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">
                  {apresentacao.titulo}
                </h3>
                
                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-gray-600 text-sm">
                    <Calendar className="w-4 h-4 mr-2" />
                    {formatDate(apresentacao.data)}
                  </div>
                  <div className="flex items-center text-gray-600 text-sm">
                    <MapPin className="w-4 h-4 mr-2" />
                    {apresentacao.local}
                  </div>
                  <div className="flex items-center text-gray-600 text-sm">
                    <Users className="w-4 h-4 mr-2" />
                    {apresentacao.participantes}
                  </div>
                </div>

                <p className="text-gray-600 text-sm mb-4">
                  {apresentacao.descricao}
                </p>

                <button
                  onClick={() => handlePlayVideo(apresentacao.videoUrl, apresentacao.titulo)}
                  className="w-full flex items-center justify-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Assistir Apresentação
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Seção Informativa */}
        <div className="mt-16 bg-white rounded-xl shadow-lg p-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Preserve Nossos Momentos
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Nossa galeria é constantemente atualizada com as mais recentes apresentações. 
              Cada vídeo representa momentos únicos de alegria, dedicação e arte que compartilhamos 
              com nossa comunidade. Acompanhe e reviva conosco esses momentos especiais.
            </p>
          </div>
        </div>

        {/* Modal de Vídeo do YouTube */}
        {showVideoModal && selectedVideo && (
          <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
              <div className="flex items-center justify-between p-4 border-b">
                <h3 className="text-lg font-semibold text-gray-800">
                  {selectedVideo.title}
                </h3>
                <button
                  onClick={closeVideoModal}
                  className="text-gray-500 hover:text-gray-700 p-1"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              <div className="aspect-video">
                <iframe
                  width="100%"
                  height="100%"
                  src={`https://www.youtube.com/embed/${selectedVideo.id}?autoplay=1&rel=0`}
                  title={selectedVideo.title}
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="w-full h-full"
                ></iframe>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GaleriaPage;