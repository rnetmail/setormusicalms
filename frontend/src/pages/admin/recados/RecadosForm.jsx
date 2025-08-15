import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaSave, FaArrowLeft, FaTimes } from 'react-icons/fa';
import FormField from '../../../components/admin/FormField';
import dataService from '../../../services/dataService';

const RecadosForm = () => {
  const { group, id, action } = useParams();
  const navigate = useNavigate();
  const isViewMode = action === 'view';
  const isEditMode = action === 'edit';
  const isNewMode = action === 'new' || !action;
  
  const groupType = group === 'coral' ? 'coral' : 'orquestra';
  
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    author: '',
    date: new Date().toISOString().split('T')[0]
  });
  
  const [loading, setLoading] = useState(isEditMode || isViewMode);
  const [errors, setErrors] = useState({});
  
  useEffect(() => {
    const fetchItem = async () => {
      if (isEditMode || isViewMode) {
        try {
          const item = dataService.getById('recados', id, groupType);
          
          if (item) {
            setFormData(item);
          } else {
            // Handle item not found
            navigate(`/gestao/recados/${groupType}`);
          }
        } catch (error) {
          console.error('Error fetching item:', error);
        } finally {
          setLoading(false);
        }
      }
    };
    
    fetchItem();
  }, [id, isEditMode, isViewMode, groupType, navigate]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
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
    
    if (!formData.title.trim()) {
      newErrors.title = 'Título é obrigatório';
    }
    
    if (!formData.content.trim()) {
      newErrors.content = 'Conteúdo é obrigatório';
    }
    
    if (!formData.author.trim()) {
      newErrors.author = 'Autor é obrigatório';
    }
    
    if (!formData.date) {
      newErrors.date = 'Data é obrigatória';
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
      
      if (isNewMode) {
        // Create new item
        await dataService.create('recados', {
          ...formData,
          type: groupType
        }, groupType);
      } else if (isEditMode) {
        // Update existing item
        await dataService.update('recados', id, formData, groupType);
      }
      
      // Redirect back to list
      navigate(`/gestao/recados/${groupType}`);
    } catch (error) {
      console.error('Error saving item:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCancel = () => {
    navigate(`/gestao/recados/${groupType}`);
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
          {isViewMode ? 'Visualizar Recado' : isEditMode ? 'Editar Recado' : 'Novo Recado'}
        </h1>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 gap-6">
            <FormField
              label="Título"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              error={errors.title}
              disabled={isViewMode}
            />
            
            <FormField
              label="Conteúdo"
              name="content"
              type="textarea"
              value={formData.content}
              onChange={handleChange}
              required
              error={errors.content}
              rows={6}
              disabled={isViewMode}
            />
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormField
                label="Autor"
                name="author"
                value={formData.author}
                onChange={handleChange}
                required
                error={errors.author}
                disabled={isViewMode}
              />
              
              <FormField
                label="Data"
                name="date"
                type="date"
                value={formData.date}
                onChange={handleChange}
                required
                error={errors.date}
                disabled={isViewMode}
              />
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
                onClick={() => navigate(`/gestao/recados/${groupType}/edit/${id}`)}
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

export default RecadosForm;