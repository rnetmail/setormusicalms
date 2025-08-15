import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Eye, Calendar } from 'lucide-react';

const RecadosAdmin = ({ context = 'geral' }) => {
  const [activeTab, setActiveTab] = useState(context);
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    type: 'info',
    author: ''
  });

  useEffect(() => {
    const fetchAnnouncements = async () => {
      try {
        setTimeout(() => {
          const mockAnnouncements = {
            geral: [
              {
                id: 1,
                title: 'Assembleia Geral - Planejamento 2025',
                content: 'Convocamos todos os integrantes do Setor Musical para assembleia geral...',
                date: '2025-08-10',
                author: 'Direção Geral',
                type: 'urgente'
              },
              {
                id: 2,
                title: 'Novo Regulamento Interno',
                content: 'Foi aprovado o novo regulamento interno do Setor Musical...',
                date: '2025-08-08',
                author: 'Coordenação Geral',
                type: 'info'
              }
            ],
            coral: [
              {
                id: 3,
                title: 'Ensaio Extra - Naipes Femininos',
                content: 'Ensaio específico para Sopranos e Contraltos no sábado às 15h...',
                date: '2025-08-12',
                author: 'Regente do Coral',
                type: 'urgente'
              },
              {
                id: 4,
                title: 'Workshop de Técnica Vocal',
                content: 'Professora convidada ministrará workshop sobre respiração...',
                date: '2025-08-09',
                author: 'Coordenação do Coral',
                type: 'info'
              }
            ],
            orquestra: [
              {
                id: 5,
                title: 'Afinação dos Violões - Obrigatório',
                content: 'Todos os integrantes devem trazer seus violões afinados...',
                date: '2025-08-11',
                author: 'Regente da Orquestra',
                type: 'urgente'
              },
              {
                id: 6,
                title: 'Cordas Novas Disponíveis',
                content: 'Chegaram as cordas encomendadas...',
                date: '2025-08-09',
                author: 'Coordenação da Orquestra',
                type: 'info'
              }
            ]
          };

          setAnnouncements(mockAnnouncements);
          setLoading(false);
        }, 500);
      } catch (error) {
        console.error('Erro ao carregar recados:', error);
        setLoading(false);
      }
    };

    fetchAnnouncements();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingItem) {
      const updatedAnnouncements = { ...announcements };
      updatedAnnouncements[context] = updatedAnnouncements[context].map(item => 
        item.id === editingItem.id 
          ? { 
              ...formData, 
              id: editingItem.id, 
              date: editingItem.date 
            }
          : item
      );
      setAnnouncements(updatedAnnouncements);
    } else {
      const newAnnouncement = {
        ...formData,
        id: Date.now(),
        date: new Date().toISOString().split('T')[0]
      };
      const updatedAnnouncements = { ...announcements };
      if (!updatedAnnouncements[context]) {
        updatedAnnouncements[context] = [];
      }
      updatedAnnouncements[context].unshift(newAnnouncement);
      setAnnouncements(updatedAnnouncements);
    }
    
    resetForm();
    setShowModal(false);
  };

  const handleEdit = (announcement) => {
    setEditingItem(announcement);
    setFormData({
      title: announcement.title,
      content: announcement.content,
      type: announcement.type,
      author: announcement.author
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este recado?')) {
      try {
        const updatedAnnouncements = { ...announcements };
        updatedAnnouncements[context] = updatedAnnouncements[context].filter(item => item.id !== id);
        setAnnouncements(updatedAnnouncements);
      } catch (error) {
        console.error('Erro ao excluir recado:', error);
        alert('Erro ao excluir recado');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      content: '',
      type: 'info',
      author: ''
    });
    setEditingItem(null);
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR');
  };

  const getTypeColor = (type) => {
    switch(type) {
      case 'urgente': return 'bg-red-100 text-red-800';
      case 'info': return 'bg-blue-100 text-blue-800';
      case 'sucesso': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const currentAnnouncements = announcements[context] || [];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">
          Gerenciar Recados - {context === 'geral' ? 'Setor Musical' : context === 'coral' ? 'Coral' : 'Orquestra'}
        </h1>
        <button
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center transition-colors"
        >
          <Plus className="w-4 h-4 mr-2" />
          Novo Recado
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
                    Título
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tipo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Data
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Autor
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ações
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {currentAnnouncements.map((announcement) => (
                  <tr key={announcement.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{announcement.title}</div>
                      <div className="text-sm text-gray-500 truncate max-w-xs">
                        {announcement.content.substring(0, 100)}...
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(announcement.type)}`}>
                        {announcement.type === 'urgente' ? 'Urgente' : 
                         announcement.type === 'info' ? 'Informativo' : 'Sucesso'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {formatDate(announcement.date)}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {announcement.author}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-3">
                        <button
                          onClick={() => alert('Visualizar recado completo (em desenvolvimento)')}
                          className="text-blue-600 hover:text-blue-900 transition-colors"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleEdit(announcement)}
                          className="text-indigo-600 hover:text-indigo-900 transition-colors"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(announcement.id)}
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
          
          {currentAnnouncements.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-500">
                <Calendar className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Nenhum recado encontrado para {context === 'geral' ? 'Setor Musical' : context === 'coral' ? 'Coral' : 'Orquestra'}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingItem ? 'Editar Recado' : 'Novo Recado'}
              </h3>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Título *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.title}
                    onChange={(e) => setFormData(prev => ({...prev, title: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Ex: Assembleia Geral - Planejamento 2025"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Conteúdo *
                  </label>
                  <textarea
                    required
                    rows={6}
                    value={formData.content}
                    onChange={(e) => setFormData(prev => ({...prev, content: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Digite o conteúdo completo do recado..."
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tipo do Recado
                    </label>
                    <select
                      value={formData.type}
                      onChange={(e) => setFormData(prev => ({...prev, type: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="info">Informativo</option>
                      <option value="urgente">Urgente</option>
                      <option value="sucesso">Sucesso</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Autor *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.author}
                      onChange={(e) => setFormData(prev => ({...prev, author: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Direção Geral"
                    />
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    {editingItem ? 'Atualizar' : 'Salvar'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecadosAdmin;