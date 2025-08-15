import { useState } from 'react';
import { FaUsers, FaPlus, FaEdit, FaTrash, FaSearch, FaEye, FaUserShield, FaUser } from 'react-icons/fa';

const UsuariosAdmin = () => {
  const [usuarios, setUsuarios] = useState([
    {
      id: 1,
      nome: 'João Silva',
      email: 'joao.silva@email.com',
      telefone: '(67) 99999-1234',
      papel: 'admin',
      status: 'ativo',
      contexto: ['geral', 'coral'],
      dataCadastro: '2024-01-15',
      ultimoAcesso: '2024-08-13'
    },
    {
      id: 2,
      nome: 'Maria Santos',
      email: 'maria.santos@email.com',
      telefone: '(67) 99999-5678',
      papel: 'moderador',
      status: 'ativo',
      contexto: ['coral'],
      dataCadastro: '2024-02-20',
      ultimoAcesso: '2024-08-12'
    },
    {
      id: 3,
      nome: 'Pedro Oliveira',
      email: 'pedro.oliveira@email.com',
      telefone: '(67) 99999-9012',
      papel: 'editor',
      status: 'inativo',
      contexto: ['orquestra'],
      dataCadastro: '2024-03-10',
      ultimoAcesso: '2024-07-15'
    }
  ]);

  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    telefone: '',
    papel: 'editor',
    status: 'ativo',
    contexto: [],
    senha: ''
  });

  const papeis = [
    { value: 'admin', label: 'Administrador', description: 'Acesso total ao sistema' },
    { value: 'moderador', label: 'Moderador', description: 'Pode gerenciar conteúdo específico' },
    { value: 'editor', label: 'Editor', description: 'Pode criar e editar conteúdo' }
  ];

  const contextos = [
    { value: 'geral', label: 'Setor Musical' },
    { value: 'coral', label: 'Coral' },
    { value: 'orquestra', label: 'Orquestra' }
  ];

  const filteredUsuarios = usuarios.filter(usuario => 
    usuario.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    usuario.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingItem) {
      setUsuarios(prev => prev.map(usuario => 
        usuario.id === editingItem.id 
          ? { 
              ...formData, 
              id: editingItem.id, 
              dataCadastro: editingItem.dataCadastro,
              ultimoAcesso: editingItem.ultimoAcesso
            }
          : usuario
      ));
    } else {
      const newUsuario = {
        ...formData,
        id: Date.now(),
        dataCadastro: new Date().toISOString().split('T')[0],
        ultimoAcesso: 'Nunca'
      };
      delete newUsuario.senha; // Remove senha do objeto salvo (em produção, seria hasheada)
      setUsuarios(prev => [...prev, newUsuario]);
    }
    
    resetForm();
    setShowModal(false);
  };

  const handleEdit = (usuario) => {
    setEditingItem(usuario);
    setFormData({
      nome: usuario.nome,
      email: usuario.email,
      telefone: usuario.telefone,
      papel: usuario.papel,
      status: usuario.status,
      contexto: usuario.contexto,
      senha: ''
    });
    setShowModal(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('Tem certeza que deseja excluir este usuário?')) {
      setUsuarios(prev => prev.filter(usuario => usuario.id !== id));
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      email: '',
      telefone: '',
      papel: 'editor',
      status: 'ativo',
      contexto: [],
      senha: ''
    });
    setEditingItem(null);
  };

  const handleContextoChange = (contextoValue) => {
    setFormData(prev => ({
      ...prev,
      contexto: prev.contexto.includes(contextoValue)
        ? prev.contexto.filter(c => c !== contextoValue)
        : [...prev.contexto, contextoValue]
    }));
  };

  const getPapelColor = (papel) => {
    switch (papel) {
      case 'admin':
        return 'bg-red-100 text-red-800';
      case 'moderador':
        return 'bg-yellow-100 text-yellow-800';
      case 'editor':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status) => {
    return status === 'ativo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Gerenciar Usuários</h2>
          <p className="text-gray-600">
            Gerencie os usuários e suas permissões no sistema
          </p>
        </div>
        <button
          onClick={() => {
            resetForm();
            setShowModal(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <FaPlus /> Novo Usuário
        </button>
      </div>

      {/* Search */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="relative">
          <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar usuários por nome ou email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuário
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Papel
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Contextos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Último Acesso
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredUsuarios.map((usuario) => (
                <tr key={usuario.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                          <FaUser className="text-gray-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {usuario.nome}
                        </div>
                        <div className="text-sm text-gray-500">
                          {usuario.email}
                        </div>
                        <div className="text-xs text-gray-400">
                          {usuario.telefone}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPapelColor(usuario.papel)}`}>
                      {usuario.papel === 'admin' && <FaUserShield className="mr-1" />}
                      {papeis.find(p => p.value === usuario.papel)?.label}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div className="flex flex-wrap gap-1">
                      {usuario.contexto.map(ctx => (
                        <span key={ctx} className="inline-flex px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                          {contextos.find(c => c.value === ctx)?.label}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(usuario.status)}`}>
                      {usuario.status === 'ativo' ? 'Ativo' : 'Inativo'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {usuario.ultimoAcesso === 'Nunca' ? 'Nunca' : new Date(usuario.ultimoAcesso).toLocaleDateString('pt-BR')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => alert('Visualizar perfil (em desenvolvimento)')}
                        className="text-blue-600 hover:text-blue-900"
                        title="Visualizar"
                      >
                        <FaEye />
                      </button>
                      <button
                        onClick={() => handleEdit(usuario)}
                        className="text-green-600 hover:text-green-900"
                        title="Editar"
                      >
                        <FaEdit />
                      </button>
                      <button
                        onClick={() => handleDelete(usuario.id)}
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
                {editingItem ? 'Editar Usuário' : 'Novo Usuário'}
              </h3>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nome Completo *
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.nome}
                      onChange={(e) => setFormData(prev => ({...prev, nome: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: João Silva"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email *
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData(prev => ({...prev, email: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="usuario@email.com"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Telefone
                    </label>
                    <input
                      type="tel"
                      value={formData.telefone}
                      onChange={(e) => setFormData(prev => ({...prev, telefone: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="(67) 99999-9999"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {editingItem ? 'Nova Senha (deixar vazio para manter)' : 'Senha *'}
                    </label>
                    <input
                      type="password"
                      required={!editingItem}
                      value={formData.senha}
                      onChange={(e) => setFormData(prev => ({...prev, senha: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Senha do usuário"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Papel no Sistema
                    </label>
                    <select
                      value={formData.papel}
                      onChange={(e) => setFormData(prev => ({...prev, papel: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {papeis.map(papel => (
                        <option key={papel.value} value={papel.value}>
                          {papel.label}
                        </option>
                      ))}
                    </select>
                    <p className="text-xs text-gray-500 mt-1">
                      {papeis.find(p => p.value === formData.papel)?.description}
                    </p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Status
                    </label>
                    <select
                      value={formData.status}
                      onChange={(e) => setFormData(prev => ({...prev, status: e.target.value}))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="ativo">Ativo</option>
                      <option value="inativo">Inativo</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Contextos de Acesso
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {contextos.map(contexto => (
                      <label key={contexto.value} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={formData.contexto.includes(contexto.value)}
                          onChange={() => handleContextoChange(contexto.value)}
                          className="mr-2"
                        />
                        <span className="text-sm">{contexto.label}</span>
                      </label>
                    ))}
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

export default UsuariosAdmin;