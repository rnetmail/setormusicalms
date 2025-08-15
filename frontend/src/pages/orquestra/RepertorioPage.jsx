import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Music, ArrowLeft, Search, Play, Download, Eye, ChevronDown, ChevronRight, Volume2, Video, FileText } from 'lucide-react';

const RepertorioPage = () => {
  const [repertorio, setRepertorio] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [expandedNaipe, setExpandedNaipe] = useState(null);
  const [expandedMusica, setExpandedMusica] = useState(null);

  const naipes = ['Violão Solo', 'Violão Base', 'Violão Acompanhamento', 'Percussão'];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setRepertorio([
        {
          id: 1,
          titulo: 'Estudo Op. 60 No. 1',
          compositor: 'Matteo Carcassi',
          arranjo: 'Adaptação Própria',
          nivel: 'Iniciante',
          naipe: 'Violão Solo',
          partitura: 'https://drive.google.com/file/d/exemplo1/preview',
          tipoPartitura: 'pdf',
          audio: 'https://drive.google.com/file/d/exemplo-audio1',
          video: 'https://youtube.com/watch?v=exemplo1',
          observacoes: 'Estudo técnico para desenvolvimento da digitação'
        },
        {
          id: 2,
          titulo: 'Romance Anônimo',
          compositor: 'Anônimo',
          arranjo: 'Pedro Costa',
          nivel: 'Intermediário',
          naipe: 'Violão Solo',
          partitura: 'https://drive.google.com/file/d/exemplo2/preview',
          tipoPartitura: 'pdf',
          audio: 'https://drive.google.com/file/d/exemplo-audio2',
          video: 'https://youtube.com/watch?v=exemplo2',
          observacoes: 'Peça clássica do repertório violonístico'
        },
        {
          id: 3,
          titulo: 'Acorde Base Dó Maior',
          compositor: 'Exercício Tradicional',
          arranjo: 'Carlos Silva',
          nivel: 'Iniciante',
          naipe: 'Violão Base',
          partitura: 'https://drive.google.com/file/d/exemplo3/preview',
          tipoPartitura: 'pdf',
          audio: 'https://drive.google.com/file/d/exemplo-audio3',
          video: '',
          observacoes: 'Exercício fundamental para acompanhamento'
        },
        {
          id: 4,
          titulo: 'Arpejo Em Lá Menor',
          compositor: 'Fernando Sor',
          arranjo: 'Maria Santos',
          nivel: 'Intermediário',
          naipe: 'Violão Acompanhamento',
          partitura: 'https://drive.google.com/file/d/exemplo4/preview',
          tipoPartitura: 'pdf',
          audio: 'https://drive.google.com/file/d/exemplo-audio4',
          video: 'https://youtube.com/watch?v=exemplo4',
          observacoes: 'Arpejo clássico para acompanhamento harmônico'
        },
        {
          id: 5,
          titulo: 'Ritmo Básico 4/4',
          compositor: 'Exercício Tradicional',
          arranjo: 'João Costa',
          nivel: 'Iniciante',
          naipe: 'Percussão',
          partitura: 'https://drive.google.com/file/d/exemplo5/preview',
          tipoPartitura: 'pdf',
          audio: 'https://drive.google.com/file/d/exemplo-audio5',
          video: 'https://youtube.com/watch?v=exemplo5',
          observacoes: 'Ritmo fundamental para acompanhamento'
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getMusicasByNaipe = (naipe) => {
    return repertorio.filter(musica => 
      musica.naipe === naipe &&
      (musica.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
       musica.compositor.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  };

  const toggleNaipe = (naipe) => {
    setExpandedNaipe(expandedNaipe === naipe ? null : naipe);
    setExpandedMusica(null); // Fechar música expandida ao trocar de naipe
  };

  const toggleMusica = (musicaId) => {
    setExpandedMusica(expandedMusica === musicaId ? null : musicaId);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Link to="/orquestra" className="mr-4 text-gray-600 hover:text-green-600 transition-colors">
                <ArrowLeft className="h-6 w-6" />
              </Link>
              <Music className="h-8 w-8 text-green-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">Repertório da Orquestra</h1>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search */}
        <div className="mb-8">
          <div className="relative max-w-md mx-auto">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar por título ou compositor..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Naipes Accordion */}
        {loading ? (
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg shadow-lg p-6 animate-pulse">
                <div className="h-6 bg-gray-200 rounded mb-4"></div>
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-4">
            {naipes.map((naipe) => {
              const musicasDoNaipe = getMusicasByNaipe(naipe);
              if (musicasDoNaipe.length === 0 && searchTerm) return null;

              return (
                <div key={naipe} className="bg-white rounded-lg shadow-lg overflow-hidden">
                  {/* Naipe Header */}
                  <button
                    onClick={() => toggleNaipe(naipe)}
                    className="w-full px-6 py-4 text-left bg-green-50 hover:bg-green-100 transition-colors flex items-center justify-between"
                  >
                    <div className="flex items-center">
                      <Music className="w-5 h-5 text-green-600 mr-3" />
                      <h3 className="text-lg font-semibold text-gray-900">{naipe}</h3>
                      <span className="ml-3 px-2 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                        {musicasDoNaipe.length} música{musicasDoNaipe.length !== 1 ? 's' : ''}
                      </span>
                    </div>
                    {expandedNaipe === naipe ? 
                      <ChevronDown className="w-5 h-5 text-gray-500" /> :
                      <ChevronRight className="w-5 h-5 text-gray-500" />
                    }
                  </button>

                  {/* Músicas do Naipe */}
                  {expandedNaipe === naipe && (
                    <div className="border-t">
                      {musicasDoNaipe.map((musica) => (
                        <div key={musica.id} className="border-b last:border-b-0">
                          {/* Música Header */}
                          <button
                            onClick={() => toggleMusica(musica.id)}
                            className="w-full px-6 py-4 text-left hover:bg-gray-50 transition-colors flex items-center justify-between"
                          >
                            <div className="flex-1">
                              <div className="flex items-start justify-between">
                                <div>
                                  <h4 className="text-md font-semibold text-gray-900">{musica.titulo}</h4>
                                  <p className="text-sm text-gray-600">{musica.compositor}</p>
                                  <p className="text-xs text-gray-500">Arranjo: {musica.arranjo}</p>
                                </div>
                                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                  musica.nivel === 'Iniciante' ? 'bg-green-100 text-green-800' :
                                  musica.nivel === 'Intermediário' ? 'bg-yellow-100 text-yellow-800' :
                                  'bg-red-100 text-red-800'
                                }`}>
                                  {musica.nivel}
                                </span>
                              </div>
                            </div>
                            {expandedMusica === musica.id ? 
                              <ChevronDown className="w-4 h-4 text-gray-500 ml-4" /> :
                              <ChevronRight className="w-4 h-4 text-gray-500 ml-4" />
                            }
                          </button>

                          {/* Conteúdo da Música */}
                          {expandedMusica === musica.id && (
                            <div className="px-6 pb-6">
                              {musica.observacoes && (
                                <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                                  <p className="text-sm text-gray-700">{musica.observacoes}</p>
                                </div>
                              )}

                              {/* Tela Dividida - Partitura + Mídia */}
                              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {/* Partitura */}
                                {musica.partitura && (
                                  <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="flex items-center mb-3">
                                      <FileText className="w-5 h-5 text-blue-600 mr-2" />
                                      <h5 className="font-semibold text-gray-900">Partitura</h5>
                                    </div>
                                    <div className="border rounded-lg overflow-hidden" style={{height: '400px'}}>
                                      <iframe
                                        src={musica.partitura}
                                        width="100%"
                                        height="100%"
                                        frameBorder="0"
                                        title={`Partitura - ${musica.titulo}`}
                                        className="w-full h-full"
                                      />
                                    </div>
                                  </div>
                                )}

                                {/* Mídia (Áudio/Vídeo) */}
                                <div className="space-y-4">
                                  {musica.audio && (
                                    <div className="bg-gray-50 rounded-lg p-4">
                                      <div className="flex items-center mb-3">
                                        <Volume2 className="w-5 h-5 text-green-600 mr-2" />
                                        <h5 className="font-semibold text-gray-900">Áudio de Referência</h5>
                                      </div>
                                      <div className="border rounded-lg overflow-hidden">
                                        <iframe
                                          src={musica.audio}
                                          width="100%"
                                          height="200"
                                          frameBorder="0"
                                          title={`Áudio - ${musica.titulo}`}
                                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                        />
                                      </div>
                                    </div>
                                  )}

                                  {musica.video && (
                                    <div className="bg-gray-50 rounded-lg p-4">
                                      <div className="flex items-center mb-3">
                                        <Video className="w-5 h-5 text-red-600 mr-2" />
                                        <h5 className="font-semibold text-gray-900">Vídeo de Referência</h5>
                                      </div>
                                      <div className="border rounded-lg overflow-hidden">
                                        <iframe
                                          src={musica.video.replace('watch?v=', 'embed/')}
                                          width="100%"
                                          height="250"
                                          frameBorder="0"
                                          title={`Vídeo - ${musica.titulo}`}
                                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                          allowFullScreen
                                        />
                                      </div>
                                    </div>
                                  )}

                                  {!musica.audio && !musica.video && musica.partitura && (
                                    <div className="bg-gray-50 rounded-lg p-4 text-center text-gray-500">
                                      <p>Nenhum áudio ou vídeo disponível</p>
                                      <p className="text-sm mt-1">Apenas partitura disponível para esta música</p>
                                    </div>
                                  )}
                                </div>
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {!loading && naipes.every(naipe => getMusicasByNaipe(naipe).length === 0) && searchTerm && (
          <div className="text-center py-12">
            <Music className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">Nenhuma música encontrada</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RepertorioPage;