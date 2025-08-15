import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaSave, FaArrowLeft, FaTimes } from 'react-icons/fa';
import FormField from '../../../components/admin/FormField';
import dataService from '../../../services/dataService';

const UsuariosForm = () => {
  const { id, action } = useParams();
  const navigate = useNavigate();
  const isViewMode = action === 'view';
  const isEditMode = action === 'edit';
  const isNewMode = action === 'new' || !action;
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'viewer',
    isActive: true
  });
  
  const [loading, setLoading] = useState(isEditMode || isViewMode);
  const [errors, setErrors] = useState({});
  
  useEffect(() => {
    const fetchItem = async () => {
      if (isEditMode || isViewMode) {
        try {
          const item = dataService.getById('usuarios', id);
          
          if (item) {
            // Don't include password in edit or view mode
            const { password, ...rest } = item;
            setFormData(rest);
          } else {
            // Handle item not found
            navigate('/gestao/usuarios');
          }
        } catch (error) {
          console.error('Error fetching user:', error);
        } finally {
          setLoading(false);
        }
      }
    };
    
    fetchItem();
  }, [id, isEditMode, isViewMode, navigate]);
  
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error when field is edited
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };
  
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email é obrigatório';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }
    
    // Password is required only for new users
    if (isNewMode) {
      if (!formData.password) {
        newErrors.password = 'Senha é obrigatória';
      } else if (formData.password.length < 6) {
        newErrors.password = 'Senha deve ter pelo menos 6 caracteres';
      }
      
      if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'As senhas não coincidem';
      }
    } else if (formData.password) {
      // If changing password in edit mode
      if (formData.password.length < 6) {
        newErrors.password = 'Senha deve ter pelo menos 6 caracteres';
      }
      
      if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'As senhas não coincidem';
      }
    }
    
    if (!formData.role) {
      newErrors.role = 'Função é obrigatória';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    try {
      setLoading(true);
      
      // Remove confirmPassword field before saving
      const { confirmPassword, ...dataToSave } = formData;
      
      // If editing and no password provided, remove password field
      if (isEditMode && !dataToSave.password) {
        delete dataToSave.password;
      }
      
      if (isNewMode) {
        // Create new user
        dataToSave.lastLogin = null;
        await dataService.create('usuarios', dataToSave);
      } else if (isEditMode) {
        // Update existing user
        await dataService.update('usuarios', id, dataToSave);
      }
      
      // Redirect back to list
      navigate('/gestao/usuarios');
    } catch (error) {
      console.error('Error saving user:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCancel = () => {
    navigate('/gestao/usuarios');
  };
  
  if (loading) {
    return (
      <div className="p-6 flex justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  return (
    <div className="p-6">
      <div className="flex items-center mb-6">
        <button
          onClick={handleCancel}
          className="mr-4 text-gray-500 hover:text-gray-700"
          title="Voltar"
        >
          <FaArrowLeft size={20} />
        </button>
        <h1 className="text-2xl font-bold">
          {isViewMode ? 'Visualizar Usuário' : isEditMode ? 'Editar Usuário' : 'Novo Usuário'}
        </h1>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FormField
              label="Nome"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              error={errors.name}
              disabled={isViewMode}
            />
            
            <FormField
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              error={errors.email}
              disabled={isViewMode}
            />
            
            {/* Password fields only shown in new mode or edit mode */}
            {!isViewMode && (
              <>
                <FormField
                  label={isEditMode ? "Nova Senha (deixe em branco para não alterar)" : "Senha"}
                  name="password"
                  type="password"
                  value={formData.password || ''}
                  onChange={handleChange}
                  required={isNewMode}
                  error={errors.password}
                  disabled={isViewMode}
                />
                
                <FormField
                  label="Confirmar Senha"
                  name="confirmPassword"
                  type="password"
                  value={formData.confirmPassword || ''}
                  onChange={handleChange}
                  required={isNewMode || formData.password}
                  error={errors.confirmPassword}
                  disabled={isViewMode}
                />
              </>
            )}
            
            <FormField
              label="Função"
              name="role"
              type="select"
              value={formData.role}
              onChange={handleChange}
              required
              error={errors.role}
              options={[
                { value: 'admin', label: 'Administrador' },
                { value: 'editor', label: 'Editor' },
                { value: 'viewer', label: 'Visualizador' }
              ]}
              disabled={isViewMode}
            />
            
            <div className="flex items-center">
              <input
                id="isActive"
                name="isActive"
                type="checkbox"
                checked={formData.isActive}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                disabled={isViewMode}
              />
              <label htmlFor="isActive" className="ml-2 block text-sm text-gray-900">
                Usuário ativo
              </label>
            </div>
          </div>
          
          <div className="mt-6 flex justify-end space-x-3">
            {!isViewMode && (
              <>
                <button
                  type="button"
                  onClick={handleCancel}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 flex items-center"
                  disabled={loading}
                >
                  <FaTimes className="mr-2" /> Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center"
                  disabled={loading}
                >
                  <FaSave className="mr-2" /> Salvar
                </button>
              </>
            )}
            {isViewMode && (
              <button
                type="button"
                onClick={() => navigate(`/gestao/usuarios/edit/${id}`)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Editar
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default UsuariosForm;