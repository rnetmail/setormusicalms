import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Music, Volume2, FileText, Search, Youtube, ChevronDown, ChevronRight } from 'lucide-react';

const RepertorioPage = () => {
  const { area } = useParams();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedGrupos, setExpandedGrupos] = useState({});
  const [expandedMusicas, setExpandedMusicas] = useState({});
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [showVideoModal, setShowVideoModal] = useState(false);

  // Definir grupos baseado na área
  const grupos = area === 'orquestra' 
    ? ['Grupo Novos', 'Grupo 1', 'Grupo 2', 'Grupo 3', 'Grupo 4']
    : ['Contraltos', 'Sopranos', 'Baixos', 'Tenores'];

  // Dados de exemplo do repertório (com links do Google Drive e YouTube)
  const repertorioData = {
    orquestra: {
      'Grupo Novos': [
        {
          id: 1,
          titulo: 'Ave Maria - Schubert',
          compositor: 'Franz Schubert',
          tonalidade: 'Ré Maior',
          dificuldade: 'Iniciante',
          partitura: 'https://drive.google.com/file/d/1example-ave-maria-schubert/view',
          audio: 'https://drive.google.com/file/d/1example-ave-maria-audio/view',
          video: 'https://www.youtube.com/watch?v=example-ave-maria'
        },
        {
          id: 2,
          titulo: 'Canon em Ré',
          compositor: 'Johann Pachelbel',
          tonalidade: 'Ré Maior',
          dificuldade: 'Iniciante',
          partitura: 'https://drive.google.com/file/d/1example-canon-pachelbel/view',
          audio: 'https://drive.google.com/file/d/1example-canon-audio/view',
          video: 'https://www.youtube.com/watch?v=example-canon'
        }
      ],
      'Grupo 1': [
        {
          id: 3,
          titulo: 'Primavera - Vivaldi',
          compositor: 'Antonio Vivaldi',
          tonalidade: 'Mi Maior',
          dificuldade: 'Intermediário',
          partitura: 'https://drive.google.com/file/d/1example-primavera-vivaldi/view',
          audio: 'https://drive.google.com/file/d/1example-primavera-audio/view',
          video: 'https://www.youtube.com/watch?v=example-primavera'
        },
        {
          id: 4,
          titulo: 'Für Elise - Beethoven',
          compositor: 'Ludwig van Beethoven',
          tonalidade: 'Lá menor',
          dificuldade: 'Intermediário',
          partitura: 'https://drive.google.com/file/d/1example-fur-elise/view',
          audio: 'https://drive.google.com/file/d/1example-fur-elise-audio/view',
          video: 'https://www.youtube.com/watch?v=example-fur-elise'
        }
      ],
      'Grupo 2': [],
      'Grupo 3': [],
      'Grupo 4': []
    },
    coral: {
      'Sopranos': [
        {
          id: 5,
          titulo: 'Ave Verum Corpus',
          compositor: 'W. A. Mozart',
          tonalidade: 'Ré Maior',
          dificuldade: 'Intermediário',
          partitura: 'https://drive.google.com/file/d/1example-ave-verum-soprano/view',
          audio: 'https://drive.google.com/file/d/1example-ave-verum-soprano-audio/view',
          video: 'https://www.youtube.com/watch?v=example-ave-verum'
        }
      ],
      'Contraltos': [
        {
          id: 6,
          titulo: 'Ave Verum Corpus',
          compositor: 'W. A. Mozart',
          tonalidade: 'Ré Maior',
          dificuldade: 'Intermediário',
          partitura: 'https://drive.google.com/file/d/1example-ave-verum-contralto/view',
          audio: 'https://drive.google.com/file/d/1example-ave-verum-contralto-audio/view',
          video: 'https://www.youtube.com/watch?v=example-ave-verum'
        }
      ],
      'Baixos': [],
      'Tenores': []
    }
  };

  // Função para extrair ID do YouTube
  const getYouTubeId = (url) => {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  };

  // Função para converter Google Drive para visualização direta
  const getGoogleDriveDirectLink = (url) => {
    const fileIdMatch = url.match(/\/d\/([a-zA-Z0-9-_]+)/);
    if (fileIdMatch) {
      return `https://drive.google.com/file/d/${fileIdMatch[1]}/preview`;
    }
    return url;
  };

  const handleOpenPartitura = (partituraUrl) => {
    const directLink = getGoogleDriveDirectLink(partituraUrl);
    window.open(directLink, '_blank');
  };

  const handleOpenAudio = (audioUrl) => {
    const directLink = getGoogleDriveDirectLink(audioUrl);
    window.open(directLink, '_blank');
  };

  const handlePlayVideo = (videoUrl, musicaTitle) => {
    const videoId = getYouTubeId(videoUrl);
    if (videoId) {
      setSelectedVideo({ id: videoId, title: musicaTitle });
      setShowVideoModal(true);
    }
  };

  const closeVideoModal = () => {
    setShowVideoModal(false);
    setSelectedVideo(null);
  };

  const toggleGrupo = (grupoName) => {
    setExpandedGrupos(prev => ({
      ...prev,
      [grupoName]: !prev[grupoName]
    }));
  };

  const toggleMusica = (musicaId) => {
    setExpandedMusicas(prev => ({
      ...prev,
      [musicaId]: !prev[musicaId]
    }));
  };

  const getFilteredRepertorio = () => {
    if (!area) return {};
    
    const currentData = repertorioData[area] || {};
    if (!searchTerm) return currentData;

    const filtered = {};
    Object.keys(currentData).forEach(grupo => {
      const musicasFiltradas = currentData[grupo].filter(musica =>
        musica.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
        musica.compositor.toLowerCase().includes(searchTerm.toLowerCase())
      );
      if (musicasFiltradas.length > 0) {
        filtered[grupo] = musicasFiltradas;
      }
    });
    return filtered;
  };

  const filteredData = getFilteredRepertorio();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <button
            onClick={() => navigate('/areas')}
            className="flex items-center text-blue-600 hover:text-blue-800 font-medium mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar para seleção de áreas
          </button>
          
          <h1 className="text-4xl font-bold text-gray-800 mb-2 capitalize">
            Repertório da {area === 'orquestra' ? 'Orquestra' : 'Coral'}
          </h1>
          <p className="text-lg text-gray-600">
            Navegue pelos {area === 'orquestra' ? 'grupos' : 'naipes'} e explore o repertório disponível
          </p>
        </div>

        {/* Barra de Pesquisa */}
        <div className="mb-8">
          <div className="relative max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar música ou compositor..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-md"
            />
          </div>
        </div>

        {/* Acordeão de Grupos/Nipes */}
        <div className="space-y-4">
          {Object.keys(filteredData).length === 0 ? (
            <div className="text-center py-12">
              <Music className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">
                {searchTerm ? 'Nenhuma música encontrada' : 'Repertório em preparação'}
              </h3>
              <p className="text-gray-500">
                {searchTerm ? 'Tente uma busca diferente.' : 'O repertório ainda não foi disponibilizado.'}
              </p>
            </div>
          ) : (
            Object.entries(filteredData).map(([grupoName, musicas]) => (
              <div key={grupoName} className="bg-white rounded-xl shadow-md border border-gray-100">
                {/* Header do Grupo/Nipe */}
                <button
                  onClick={() => toggleGrupo(grupoName)}
                  className="w-full p-6 flex items-center justify-between hover:bg-gray-50 transition-colors rounded-xl"
                >
                  <div className="flex items-center space-x-4">
                    <div className="p-3 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg">
                      <Music className="w-6 h-6 text-white" />
                    </div>
                    <div className="text-left">
                      <h3 className="text-xl font-semibold text-gray-800">{grupoName}</h3>
                      <p className="text-sm text-gray-600">
                        {musicas.length} {musicas.length === 1 ? 'música' : 'músicas'} disponível{musicas.length === 1 ? '' : 'eis'}
                      </p>
                    </div>
                  </div>
                  {expandedGrupos[grupoName] ? (
                    <ChevronDown className="w-5 h-5 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-500" />
                  )}
                </button>

                {/* Conteúdo expandido - Lista de Músicas */}
                {expandedGrupos[grupoName] && (
                  <div className="px-6 pb-6 space-y-3 border-t border-gray-100">
                    {musicas.map((musica) => (
                      <div key={musica.id} className="bg-gray-50 rounded-lg border border-gray-200">
                        {/* Header da Música - Interface Acessível */}
                        <button
                          onClick={() => toggleMusica(musica.id)}
                          className="w-full p-6 flex items-center justify-between hover:bg-gray-100 transition-colors rounded-lg"
                        >
                          <div className="text-left flex-1">
                            <h4 className="text-xl font-bold text-gray-800 mb-1">{musica.titulo}</h4>
                            <p className="text-lg text-gray-600">Compositor: {musica.compositor}</p>
                            <p className="text-sm text-blue-600 mt-2 font-medium">
                              {expandedMusicas[musica.id] ? '↑ Clique para fechar' : '↓ Clique para ver opções'}
                            </p>
                          </div>
                          <div className="ml-4">
                            {expandedMusicas[musica.id] ? (
                              <ChevronDown className="w-8 h-8 text-gray-500" />
                            ) : (
                              <ChevronRight className="w-8 h-8 text-gray-500" />
                            )}
                          </div>
                        </button>

                        {/* Conteúdo expandido - Interface Acessível */}
                        {expandedMusicas[musica.id] && (
                          <div className="px-6 pb-6 border-t border-gray-200 bg-gray-50">
                            {/* Informações da Música - Layout Simplificado */}
                            <div className="mb-6 mt-4">
                              <div className="space-y-4">
                                <div className="bg-white p-4 rounded-lg shadow-sm">
                                  <h4 className="text-lg font-semibold text-gray-800 mb-2">Informações da Música</h4>
                                  <div className="space-y-3 text-base">
                                    <div>
                                      <span className="font-medium text-gray-700 block">Tonalidade:</span>
                                      <span className="text-gray-800 text-lg">{musica.tonalidade}</span>
                                    </div>
                                    <div>
                                      <span className="font-medium text-gray-700 block">Nível de Dificuldade:</span>
                                      <span className={`inline-block px-4 py-2 rounded-lg text-base font-semibold ${
                                        musica.dificuldade === 'Iniciante' ? 'bg-green-100 text-green-800' :
                                        musica.dificuldade === 'Intermediário' ? 'bg-yellow-100 text-yellow-800' :
                                        'bg-red-100 text-red-800'
                                      }`}>
                                        {musica.dificuldade}
                                      </span>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>

                            {/* Botões de Ação - Grandes e Claros */}
                            <div className="space-y-4">
                              <h4 className="text-lg font-semibold text-gray-800 mb-4">Materiais Disponíveis</h4>
                              
                              {/* Botão Partitura */}
                              <button
                                onClick={() => handleOpenPartitura(musica.partitura)}
                                className="w-full flex items-center justify-center px-8 py-6 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors text-xl font-bold shadow-lg border-2 border-blue-600"
                              >
                                <FileText className="w-8 h-8 mr-4" />
                                <div className="text-left">
                                  <div>Ver Partitura</div>
                                  <div className="text-sm font-normal opacity-90">Clique para abrir em nova aba</div>
                                </div>
                              </button>

                              {/* Botão Áudio */}
                              <button
                                onClick={() => handleOpenAudio(musica.audio)}
                                className="w-full flex items-center justify-center px-8 py-6 bg-green-500 text-white rounded-xl hover:bg-green-600 transition-colors text-xl font-bold shadow-lg border-2 border-green-600"
                              >
                                <Volume2 className="w-8 h-8 mr-4" />
                                <div className="text-left">
                                  <div>Ouvir Áudio</div>
                                  <div className="text-sm font-normal opacity-90">Clique para abrir em nova aba</div>
                                </div>
                              </button>

                              {/* Botão Vídeo */}
                              {musica.video && (
                                <button
                                  onClick={() => handlePlayVideo(musica.video, musica.titulo)}
                                  className="w-full flex items-center justify-center px-8 py-6 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-colors text-xl font-bold shadow-lg border-2 border-red-600"
                                >
                                  <Youtube className="w-8 h-8 mr-4" />
                                  <div className="text-left">
                                    <div>Assistir Vídeo</div>
                                    <div className="text-sm font-normal opacity-90">Clique para reproduzir</div>
                                  </div>
                                </button>
                              )}
                            </div>
                            
                            {/* Instruções de Ajuda */}
                            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                              <h5 className="text-base font-semibold text-blue-800 mb-2">💡 Como usar:</h5>
                              <ul className="text-sm text-blue-700 space-y-1">
                                <li>• <strong>Partitura:</strong> Abrirá o arquivo para você imprimir ou visualizar</li>
                                <li>• <strong>Áudio:</strong> Ouça a música para treinar</li>
                                <li>• <strong>Vídeo:</strong> Veja a apresentação da música</li>
                              </ul>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}
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
                  className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
                >
                  ×
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

export default RepertorioPage;