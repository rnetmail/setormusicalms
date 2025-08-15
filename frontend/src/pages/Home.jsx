import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Music, Users, Calendar, Camera, BookOpen, ChevronLeft, ChevronRight } from 'lucide-react';

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  // Mock gallery data - in real app this would come from API
  const galleryImages = [
    {
      id: 1,
      url: 'https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=Coral+em+Apresentação',
      title: 'Coral em Apresentação',
      description: 'Apresentação especial do Coral'
    },
    {
      id: 2,
      url: 'https://via.placeholder.com/800x400/059669/FFFFFF?text=Orquestra+de+Violões',
      title: 'Orquestra de Violões',
      description: 'Orquestra durante ensaio'
    },
    {
      id: 3,
      url: 'https://via.placeholder.com/800x400/DC2626/FFFFFF?text=Evento+Musical',
      title: 'Evento Musical',
      description: 'Grande evento do Setor Musical'
    },
    {
      id: 4,
      url: 'https://via.placeholder.com/800x400/7C3AED/FFFFFF?text=Cerimônia+Especial',
      title: 'Cerimônia Especial',
      description: 'Cerimônia com participação do Setor Musical'
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % galleryImages.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [galleryImages.length]);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % galleryImages.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + galleryImages.length) % galleryImages.length);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Music className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">Setor Musical Mokiti Okada MS</h1>
            </div>
            <nav className="hidden md:flex space-x-8">
              <Link to="/historia" className="text-gray-700 hover:text-blue-600 transition-colors">História</Link>
              <Link to="/galeria" className="text-gray-700 hover:text-blue-600 transition-colors">Galeria</Link>
              <Link to="/recados" className="text-gray-700 hover:text-blue-600 transition-colors">Recados</Link>
              <Link to="/coral" className="text-gray-700 hover:text-blue-600 transition-colors">Coral</Link>
              <Link to="/orquestra" className="text-gray-700 hover:text-blue-600 transition-colors">Orquestra</Link>
              <Link to="/admin/login" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">Admin</Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Bem-vindos ao Setor Musical
          </h2>
          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
            Espaço dedicado à música sacra e ao desenvolvimento artístico-espiritual através do Coral e da Orquestra.
          </p>
          
          {/* Quick Access Buttons */}
          <div className="flex flex-col sm:flex-row justify-center gap-6 mb-16">
            <Link 
              to="/coral"
              className="bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <Users className="inline-block w-6 h-6 mr-2" />
              Acessar Coral
            </Link>
            <Link 
              to="/orquestra"
              className="bg-green-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-green-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <Music className="inline-block w-6 h-6 mr-2" />
              Acessar Orquestra
            </Link>
          </div>

          {/* Image Carousel */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold text-gray-900 mb-8">Galeria de Momentos</h3>
            <div className="relative max-w-4xl mx-auto">
              <div className="overflow-hidden rounded-lg shadow-xl">
                <div className="relative h-96">
                  <img
                    src={galleryImages[currentSlide].url}
                    alt={galleryImages[currentSlide].title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-6">
                    <h4 className="text-white text-xl font-semibold mb-2">
                      {galleryImages[currentSlide].title}
                    </h4>
                    <p className="text-white/90">
                      {galleryImages[currentSlide].description}
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Carousel Controls */}
              <button
                onClick={prevSlide}
                className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white text-gray-800 p-2 rounded-full shadow-lg transition-all"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>
              <button
                onClick={nextSlide}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white text-gray-800 p-2 rounded-full shadow-lg transition-all"
              >
                <ChevronRight className="w-6 h-6" />
              </button>

              {/* Indicators */}
              <div className="flex justify-center mt-4 space-x-2">
                {galleryImages.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentSlide(index)}
                    className={`w-3 h-3 rounded-full transition-all ${
                      index === currentSlide ? 'bg-blue-600' : 'bg-gray-300'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            <Link 
              to="/historia" 
              className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 transform hover:scale-105"
            >
              <BookOpen className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">História</h3>
              <p className="text-gray-600 text-sm">Nossa trajetória</p>
            </Link>

            <Link 
              to="/galeria" 
              className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 transform hover:scale-105"
            >
              <Camera className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Galeria</h3>
              <p className="text-gray-600 text-sm">Fotos e momentos</p>
            </Link>

            <Link 
              to="/recados" 
              className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 transform hover:scale-105"
            >
              <Calendar className="h-12 w-12 text-purple-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Recados</h3>
              <p className="text-gray-600 text-sm">Avisos importantes</p>
            </Link>

            <Link 
              to="/coral" 
              className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 transform hover:scale-105"
            >
              <Users className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Coral</h3>
              <p className="text-gray-600 text-sm">Área do Coral</p>
            </Link>

            <Link 
              to="/orquestra" 
              className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 transform hover:scale-105"
            >
              <Music className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Orquestra</h3>
              <p className="text-gray-600 text-sm">Área da Orquestra</p>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2025 Setor Musical Mokiti Okada MS. Todos os direitos reservados.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;