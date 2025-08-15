import { useState } from 'react';
import { FaBookOpen, FaPlus, FaEdit, FaTrash, FaSearch, FaEye } from 'react-icons/fa';

const HistoriaAdmin = ({ context = 'geral' }) => {
  const [historia, setHistoria] = useState([
    {
      id: 1,
      titulo: 'Fundação do Setor Musical',
      periodo: '1995',
      resumo: 'História da criação do Setor Musical Mokiti Okada MS',
      conteudo: 'Em 1995, um grupo de jovens apaixonados pela música se reuniu com o objetivo de criar um espaço dedicado à expressão musical dentro da comunidade...',
      contexto: 'geral',
      destaque: true,
      dataPublicacao: '2024-01-15'
    },
    {
      id: 2,
      titulo: 'Primeiros Passos do Coral',
      periodo: '1996-1998',
      resumo: 'Os anos iniciais do coral e suas primeiras apresentações',
      conteudo: 'Nos primeiros anos após a fundação, o coral começou suas atividades com apenas 8 integrantes...',
      contexto: 'coral',
      destaque: false,
      dataPublicacao: '2024-02-10'
    },
    {
      id: 3,
      titulo: 'Formação da Orquestra',
      periodo: '1997-2000',
      resumo: 'Como surgiu a orquestra de violões do Setor Musical',
      conteudo: 'A orquestra nasceu da necessidade de acompanhar o coral e posteriormente desenvolveu seu próprio repertório...',
      contexto: 'orquestra',
      destaque: false,
      dataPublicacao: '2024-03-05'
    }
  ]);

  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    titulo: '',
    periodo: '',
    resumo: '',
    conteudo: '',
    destaque: false
  });

  const filteredHistoria = historia.filter(item => 
    item.contexto === context &&
    (item.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
     item.resumo.toLowerCase().includes(searchTerm.toLowerCase()) ||
     item.periodo.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingItem) {
      setHistoria(prev => prev.map(item => 
        item.id === editingItem.id 
          ? { ...formData, id: editingItem.id, contexto: context, dataPublicacao: editingItem.dataPublicacao }
          : item
      ));
    } else {
      const newItem = {
        ...formData,
        id: Date.now(),
        contexto: context,
        dataPublicacao: new Date().toISOString().split('T')[0]
      };
      setHistoria(prev => [...prev, newItem]);
    }
    
    resetForm();
    setShowModal(false);
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({
      titulo: item.titulo,
      periodo: item.periodo,
      resumo: item.resumo,
      conteudo: item.conteudo,
      destaque: item.destaque
    });
    setShowModal(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('Tem certeza que deseja excluir este item da história?')) {
      setHistoria(prev => prev.filter(item => item.id !== id));
    }
  };

  const resetForm = () => {
    setFormData({
      titulo: '',
      periodo: '',
      resumo: '',
      conteudo: '',
      destaque: false
    });
    setEditingItem(null);
  };

  const getContextLabel = () => {
    switch (context) {
      case 'coral': return 'Coral';
      case 'orquestra': return 'Orquestra';
      default: return 'Setor Musical';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            História - {getContextLabel()}
          </h2>
          <p className="text-gray-600">
            Gerencie os marcos históricos do {getContextLabel().toLowerCase()}
          </p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <FaPlus /> Novo Marco
        </button>
      </div>

      {/* Search */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="relative">
          <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar na história..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* História List */}
      <div className="space-y-4">
        {filteredHistoria.map((item) => (
          <div key={item.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-bold text-gray-900">{item.titulo}</h3>
                    {item.destaque && (
                      <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
                        Destaque
                      </span>
                    )}
                  </div>
                  <p className="text-blue-600 font-medium mb-2">{item.periodo}</p>
                  <p className="text-gray-600 mb-3">{item.resumo}</p>
                  <p className="text-gray-500 text-sm line-clamp-3">{item.conteudo}</p>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <button
                    onClick={() => alert('Visualizar história completa (em desenvolvimento)')}
                    className="text-blue-600 hover:text-blue-800 p-2"
                    title="Visualizar"
                  >
                    <FaEye />
                  </button>
                  <button
                    onClick={() => handleEdit(item)}
                    className="text-green-600 hover:text-green-800 p-2"
                    title="Editar"
                  >
                    <FaEdit />
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="text-red-600 hover:text-red-800 p-2"
                    title="Excluir"
                  >
                    <FaTrash />
                  </button>
                </div>
              </div>
              
              <div className="text-xs text-gray-400">
                Publicado em: {new Date(item.dataPublicacao).toLocaleDateString('pt-BR')}
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredHistoria.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <FaBookOpen className="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-500">Nenhum marco histórico encontrado</p>
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-2/3 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingItem ? 'Editar Marco Histórico' : 'Novo Marco Histórico'}
              </h3>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Título *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.titulo}
                      onChange={(e) => setFormData(prev => ({...prev, titulo: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Fundação do Coral"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Período *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.periodo}
                      onChange={(e) => setFormData(prev => ({...prev, periodo: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: 1995 ou 1995-1998"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Resumo *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.resumo}
                    onChange={(e) => setFormData(prev => ({...prev, resumo: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Breve descrição do marco histórico"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Conteúdo Completo *
                  </label>
                  <textarea
                    required
                    rows={6}
                    value={formData.conteudo}
                    onChange={(e) => setFormData(prev => ({...prev, conteudo: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Conte a história completa deste marco..."
                  />
                </div>

                <div>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.destaque}
                      onChange={(e) => setFormData(prev => ({...prev, destaque: e.target.checked}))}
                      className="mr-2"
                    />
                    <span className="text-sm font-medium text-gray-700">
                      Marcar como destaque
                    </span>
                  </label>
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

export default HistoriaAdmin;