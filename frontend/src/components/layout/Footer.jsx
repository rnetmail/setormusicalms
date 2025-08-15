import React from 'react';
import { Music, Mail, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Logo e Descrição */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg">
                <Music className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold">Setor Musical</h3>
                <p className="text-sm text-gray-300">Mokiti Okada MS</p>
              </div>
            </div>
            <p className="text-gray-300 text-sm">
              Elevando sentimentos através da música, promovendo harmonia, beleza e espiritualidade.
            </p>
          </div>

          {/* Contato */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contato</h4>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4 text-blue-400" />
                <span className="text-sm text-gray-300">contato@setormusicalms.art.br</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4 text-blue-400" />
                <span className="text-sm text-gray-300">Campo Grande - MS</span>
              </div>
            </div>
          </div>

          {/* Links Rápidos */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Acesso Rápido</h4>
            <div className="space-y-2">
              <a href="/recados" className="block text-sm text-gray-300 hover:text-blue-400 transition-colors">
                Recados
              </a>
              <a href="/agenda" className="block text-sm text-gray-300 hover:text-blue-400 transition-colors">
                Agenda
              </a>
              <a href="/galeria" className="block text-sm text-gray-300 hover:text-blue-400 transition-colors">
                Galeria
              </a>
              <a href="/historia" className="block text-sm text-gray-300 hover:text-blue-400 transition-colors">
                História
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-sm text-gray-400">
            © {new Date().getFullYear()} Setor Musical Mokiti Okada MS. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;