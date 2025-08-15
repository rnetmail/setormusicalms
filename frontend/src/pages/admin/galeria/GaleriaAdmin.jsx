import { useState } from 'react';
import { FaImages, FaPlus, FaEdit, FaTrash, FaSearch, FaEye } from 'react-icons/fa';

const GaleriaAdmin = ({ context = 'geral' }) => {
  const [galeria, setGaleria] = useState([
    {
      id: 1,
      titulo: 'Apresentação de Natal 2024',
      descricao: 'Fotos da apresentação especial de Natal no auditório principal',
      data: '2024-12-15',
      contexto: 'geral',
      imagens: [
        'apresentacao-natal-1.jpg',
        'apresentacao-natal-2.jpg',
        'apresentacao-natal-3.jpg'
      ],
      destaque: true
    },
    {
      id: 2,
      titulo: 'Ensaio do Coral - Outubro',
      descricao: 'Registros do ensaio preparatório para a apresentação de fim de ano',
      data: '2024-10-20',
      contexto: 'coral',
      imagens: [
        'ensaio-coral-1.jpg',
        'ensaio-coral-2.jpg'
      ],
      destaque: false
    },
    {
      id: 3,
      titulo: 'Workshop de Violão',
      descricao: 'Momentos do workshop de técnicas avançadas de violão',
      data: '2024-09-15',
      contexto: 'orquestra',
      imagens: [
        'workshop-violao-1.jpg',
        'workshop-violao-2.jpg',
        'workshop-violao-3.jpg',
        'workshop-violao-4.jpg'
      ],
      destaque: false
    }
  ]);

  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    titulo: '',
    descricao: '',
    data: '',
    imagens: [],
    destaque: false
  });

  const filteredGaleria = galeria.filter(item => 
    item.contexto === context &&
    (item.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
     item.descricao.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingItem) {
      setGaleria(prev => prev.map(item => 
        item.id === editingItem.id 
          ? { ...formData, id: editingItem.id, contexto: context }
          : item
      ));
    } else {
      const newItem = {
        ...formData,
        id: Date.now(),
        contexto: context
      };
      setGaleria(prev => [...prev, newItem]);
    }
    
    resetForm();
    setShowModal(false);
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({
      titulo: item.titulo,
      descricao: item.descricao,
      data: item.data,
      imagens: item.imagens,
      destaque: item.destaque
    });
    setShowModal(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta galeria?')) {
      setGaleria(prev => prev.filter(item => item.id !== id));
    }
  };

  const resetForm = () => {
    setFormData({
      titulo: '',
      descricao: '',
      data: '',
      imagens: [],
      destaque: false
    });
    setEditingItem(null);
  };

  const handleImageAdd = () => {
    const imageName = prompt('Nome da imagem (ex: /images/image.jpg):');
    if (imageName) {
      setFormData(prev => ({
        ...prev,
        imagens: [...prev.imagens, imageName]
      }));
    }
  };

  const handleImageRemove = (index) => {
    setFormData(prev => ({
      ...prev,
      imagens: prev.imagens.filter((_, i) => i !== index)
    }));
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
            Galeria - {getContextLabel()}
          </h2>
          <p className="text-gray-600">
            Gerencie as galerias de fotos do {getContextLabel().toLowerCase()}
          </p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <FaPlus /> Nova Galeria
        </button>
      </div>

      {/* Search */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="relative">
          <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar galerias..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Galeria Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredGaleria.map((item) => (
          <div key={item.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
            <div className="p-4">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-semibold text-gray-900">{item.titulo}</h3>
                {item.destaque && (
                  <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
                    Destaque
                  </span>
                )}
              </div>
              
              <p className="text-gray-600 text-sm mb-3">{item.descricao}</p>
              
              <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                <span>{new Date(item.data).toLocaleDateString('pt-BR')}</span>
                <span className="flex items-center gap-1">
                  <FaImages />
                  {item.imagens.length} {item.imagens.length === 1 ? 'foto' : 'fotos'}
                </span>
              </div>

              {/* Preview das imagens */}
              <div className="grid grid-cols-4 gap-2 mb-4">
                {item.imagens.slice(0, 4).map((img, index) => (
                  <div key={index} className="aspect-square bg-gray-200 rounded flex items-center justify-center">
                    <FaImages className="text-gray-400" />
                  </div>
                ))}
              </div>

              <div className="flex justify-between">
                <button
                  onClick={() => alert('Visualizar galeria (em desenvolvimento)')}
                  className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
                >
                  <FaEye /> Visualizar
                </button>
                <div className="space-x-2">
                  <button
                    onClick={() => handleEdit(item)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    <FaEdit />
                  </button>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <FaTrash />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingItem ? 'Editar Galeria' : 'Nova Galeria'}
              </h3>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Título da Galeria *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.titulo}
                    onChange={(e) => setFormData(prev => ({...prev, titulo: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Ex: Apresentação de Natal 2024"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Descrição *
                  </label>
                  <textarea
                    required
                    rows={3}
                    value={formData.descricao}
                    onChange={(e) => setFormData(prev => ({...prev, descricao: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Descreva o evento ou ocasião..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Data do Evento *
                  </label>
                  <input
                    type="date"
                    required
                    value={formData.data}
                    onChange={(e) => setFormData(prev => ({...prev, data: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Imagens
                  </label>
                  <div className="space-y-2">
                    {formData.imagens.map((img, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                        <span className="text-sm">{img}</span>
                        <button
                          type="button"
                          onClick={() => handleImageRemove(index)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={handleImageAdd}
                      className="w-full p-2 border-2 border-dashed border-gray-300 rounded-md text-gray-600 hover:border-gray-400 hover:text-gray-800"
                    >
                      + Adicionar Imagem
                    </button>
                  </div>
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

export default GaleriaAdmin;