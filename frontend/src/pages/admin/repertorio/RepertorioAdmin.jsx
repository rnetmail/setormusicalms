import { useState } from 'react';
import { FaMusic, FaPlus, FaEdit, FaTrash, FaSearch, FaFilePdf, FaImage, FaVolumeUp, FaVideo, FaEye } from 'react-icons/fa';

const RepertorioAdmin = ({ context = 'coral' }) => {
  const [repertorio, setRepertorio] = useState([
    {
      id: 1,
      titulo: 'Ave Maria',
      compositor: 'Franz Schubert',
      arranjo: 'João Silva',
      nivel: 'Intermediário',
      vozes: ['Soprano', 'Contralto', 'Tenor', 'Baixo'],
      contexto: 'coral',
      observacoes: 'Obra clássica para apresentações especiais',
      partitura: 'https://drive.google.com/file/d/exemplo1',
      tipoPartitura: 'pdf',
      audio: 'https://drive.google.com/file/d/exemplo-audio1',
      video: 'https://youtube.com/watch?v=exemplo1'
    },
    {
      id: 2,
      titulo: 'Panis Angelicus',
      compositor: 'César Franck',
      arranjo: 'Maria Santos',
      nivel: 'Avançado',
      vozes: ['Soprano', 'Contralto'],
      contexto: 'coral',
      observacoes: 'Solo com acompanhamento coral',
      partitura: 'https://drive.google.com/file/d/exemplo2',
      tipoPartitura: 'pdf',
      audio: 'https://drive.google.com/file/d/exemplo-audio2',
      video: ''
    },
    {
      id: 3,
      titulo: 'Estudo Op. 60 No. 1',
      compositor: 'Matteo Carcassi',
      arranjo: 'Adaptação Própria',
      nivel: 'Iniciante',
      vozes: ['Violão'],
      contexto: 'orquestra',
      observacoes: 'Para grupos iniciantes',
      partitura: 'https://drive.google.com/file/d/exemplo3',
      tipoPartitura: 'pdf',
      audio: 'https://drive.google.com/file/d/exemplo-audio3',
      video: 'https://youtube.com/watch?v=exemplo3'
    }
  ]);

  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    titulo: '',
    compositor: '',
    arranjo: '',
    nivel: 'Iniciante',
    vozes: [],
    observacoes: '',
    partitura: '',
    tipoPartitura: 'pdf',
    audio: '',
    video: ''
  });

  const niveis = ['Iniciante', 'Intermediário', 'Avançado'];
  const vozesCorais = ['Soprano', 'Contralto', 'Tenor', 'Baixo'];
  const instrumentos = ['Violão', 'Violão Base', 'Violão Solo', 'Percussão'];

  const getVozesDisponiveis = () => {
    return context === 'coral' ? vozesCorais : instrumentos;
  };

  const filteredRepertorio = repertorio.filter(item => 
    item.contexto === context &&
    (item.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
     item.compositor.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingItem) {
      setRepertorio(prev => prev.map(item => 
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
      setRepertorio(prev => [...prev, newItem]);
    }
    
    resetForm();
    setShowModal(false);
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({
      titulo: item.titulo,
      compositor: item.compositor,
      arranjo: item.arranjo,
      nivel: item.nivel,
      vozes: item.vozes,
      observacoes: item.observacoes || '',
      partitura: item.partitura || '',
      tipoPartitura: item.tipoPartitura || 'pdf',
      audio: item.audio || '',
      video: item.video || ''
    });
    setShowModal(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('Tem certeza que deseja excluir este item do repertório?')) {
      setRepertorio(prev => prev.filter(item => item.id !== id));
    }
  };

  const resetForm = () => {
    setFormData({
      titulo: '',
      compositor: '',
      arranjo: '',
      nivel: 'Iniciante',
      vozes: [],
      observacoes: '',
      partitura: '',
      tipoPartitura: 'pdf',
      audio: '',
      video: ''
    });
    setEditingItem(null);
  };

  const handleVozChange = (voz) => {
    setFormData(prev => ({
      ...prev,
      vozes: prev.vozes.includes(voz)
        ? prev.vozes.filter(v => v !== voz)
        : [...prev.vozes, voz]
    }));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Repertório - {context === 'coral' ? 'Coral' : 'Orquestra'}
          </h2>
          <p className="text-gray-600">
            Gerencie o repertório do {context === 'coral' ? 'coral' : 'orquestra'}
          </p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <FaPlus /> Nova Música
        </button>
      </div>

      {/* Search */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="relative">
          <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar por título ou compositor..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Repertório List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Música
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Compositor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Arranjo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nível
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {context === 'coral' ? 'Vozes' : 'Instrumentos'}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Mídias
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredRepertorio.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <FaMusic className="text-blue-500 mr-3" />
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {item.titulo}
                        </div>
                        {item.observacoes && (
                          <div className="text-sm text-gray-500">
                            {item.observacoes}
                          </div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.compositor}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.arranjo}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      item.nivel === 'Iniciante' ? 'bg-green-100 text-green-800' :
                      item.nivel === 'Intermediário' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {item.nivel}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {item.vozes.join(', ')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div className="flex space-x-2">
                      {item.partitura && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                          {item.tipoPartitura === 'pdf' ? <FaFilePdf className="mr-1" /> : <FaImage className="mr-1" />}
                          Partitura
                        </span>
                      )}
                      {item.audio && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                          <FaVolumeUp className="mr-1" />
                          Áudio
                        </span>
                      )}
                      {item.video && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-red-100 text-red-800">
                          <FaVideo className="mr-1" />
                          Vídeo
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => alert('Visualizar conteúdo completo (em desenvolvimento)')}
                        className="text-green-600 hover:text-green-900"
                        title="Visualizar"
                      >
                        <FaEye />
                      </button>
                      <button
                        onClick={() => handleEdit(item)}
                        className="text-blue-600 hover:text-blue-900"
                        title="Editar"
                      >
                        <FaEdit />
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="text-red-600 hover:text-red-900"
                        title="Excluir"
                      >
                        <FaTrash />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingItem ? 'Editar Música' : 'Nova Música'}
              </h3>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Título da Música *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.titulo}
                      onChange={(e) => setFormData(prev => ({...prev, titulo: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Compositor *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.compositor}
                      onChange={(e) => setFormData(prev => ({...prev, compositor: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Arranjo
                    </label>
                    <input
                      type="text"
                      value={formData.arranjo}
                      onChange={(e) => setFormData(prev => ({...prev, arranjo: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nível
                    </label>
                    <select
                      value={formData.nivel}
                      onChange={(e) => setFormData(prev => ({...prev, nivel: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {niveis.map(nivel => (
                        <option key={nivel} value={nivel}>{nivel}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {context === 'coral' ? 'Vozes' : 'Instrumentos'}
                  </label>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {getVozesDisponiveis().map(voz => (
                      <label key={voz} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={formData.vozes.includes(voz)}
                          onChange={() => handleVozChange(voz)}
                          className="mr-2"
                        />
                        <span className="text-sm">{voz}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Observações
                  </label>
                  <textarea
                    rows={3}
                    value={formData.observacoes}
                    onChange={(e) => setFormData(prev => ({...prev, observacoes: e.target.value}))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Observações adicionais sobre a música..."
                  />
                </div>

                {/* Seção de Mídias */}
                <div className="border-t pt-4">
                  <h4 className="text-md font-medium text-gray-900 mb-4">Materiais de Estudo</h4>
                  
                  {/* Partitura */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Tipo de Partitura
                      </label>
                      <select
                        value={formData.tipoPartitura}
                        onChange={(e) => setFormData(prev => ({...prev, tipoPartitura: e.target.value}))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="pdf">PDF</option>
                        <option value="imagem">Imagem</option>
                      </select>
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        <FaFilePdf className="inline mr-1" />
                        Link da Partitura (Google Drive)
                      </label>
                      <input
                        type="url"
                        value={formData.partitura}
                        onChange={(e) => setFormData(prev => ({...prev, partitura: e.target.value}))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="https://drive.google.com/file/d/..."
                      />
                    </div>
                  </div>

                  {/* Áudio */}
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <FaVolumeUp className="inline mr-1" />
                      Link do Áudio (Google Drive)
                    </label>
                    <input
                      type="url"
                      value={formData.audio}
                      onChange={(e) => setFormData(prev => ({...prev, audio: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="https://drive.google.com/file/d/... ou https://drive.google.com/drive/folders/..."
                    />
                  </div>

                  {/* Vídeo */}
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <FaVideo className="inline mr-1" />
                      Link do Vídeo (YouTube ou Google Drive)
                    </label>
                    <input
                      type="url"
                      value={formData.video}
                      onChange={(e) => setFormData(prev => ({...prev, video: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="https://youtube.com/watch?v=... ou https://drive.google.com/file/d/..."
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

export default RepertorioAdmin;