import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaSave, FaArrowLeft, FaTimes } from 'react-icons/fa';
import FormField from '../../../components/admin/FormField';
import dataService from '../../../services/dataService';

const AgendaForm = () => {
  const { group, id, action } = useParams();
  const navigate = useNavigate();
  const isViewMode = action === 'view';
  const isEditMode = action === 'edit';
  const isNewMode = action === 'new' || !action;
  
  const groupType = group === 'coral' ? 'coral' : 'orquestra';
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    date: new Date().toISOString().split('T')[0],
    startTime: '19:00',
    endTime: '21:00',
    location: '',
    isRecurring: false
  });
  
  const [loading, setLoading] = useState(isEditMode || isViewMode);
  const [errors, setErrors] = useState({});
  
  useEffect(() => {
    const fetchItem = async () => {
      if (isEditMode || isViewMode) {
        try {
          const item = dataService.getById('agenda', id, groupType);
          
          if (item) {
            setFormData(item);
          } else {
            // Handle item not found
            navigate(`/gestao/agenda/${groupType}`);
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
    
    if (!formData.title.trim()) {
      newErrors.title = 'Título é obrigatório';
    }
    
    if (!formData.description.trim()) {
      newErrors.description = 'Descrição é obrigatória';
    }
    
    if (!formData.date) {
      newErrors.date = 'Data é obrigatória';
    }
    
    if (!formData.startTime) {
      newErrors.startTime = 'Horário de início é obrigatório';
    }
    
    if (!formData.endTime) {
      newErrors.endTime = 'Horário de término é obrigatório';
    }
    
    if (!formData.location.trim()) {
      newErrors.location = 'Local é obrigatório';
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
        await dataService.create('agenda', {
          ...formData,
          type: groupType
        }, groupType);
      } else if (isEditMode) {
        // Update existing item
        await dataService.update('agenda', id, formData, groupType);
      }
      
      // Redirect back to list
      navigate(`/gestao/agenda/${groupType}`);
    } catch (error) {
      console.error('Error saving item:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCancel = () => {
    navigate(`/gestao/agenda/${groupType}`);
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
          {isViewMode ? 'Visualizar Evento' : isEditMode ? 'Editar Evento' : 'Novo Evento'}
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
              label="Descrição"
              name="description"
              type="textarea"
              value={formData.description}
              onChange={handleChange}
              required
              error={errors.description}
              rows={3}
              disabled={isViewMode}
            />
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
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
              
              <FormField
                label="Hora de Início"
                name="startTime"
                type="time"
                value={formData.startTime}
                onChange={handleChange}
                required
                error={errors.startTime}
                disabled={isViewMode}
              />
              
              <FormField
                label="Hora de Término"
                name="endTime"
                type="time"
                value={formData.endTime}
                onChange={handleChange}
                required
                error={errors.endTime}
                disabled={isViewMode}
              />
            </div>
            
            <FormField
              label="Local"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              error={errors.location}
              disabled={isViewMode}
            />
            
            <div className="flex items-center">
              <input
                id="isRecurring"
                name="isRecurring"
                type="checkbox"
                checked={formData.isRecurring}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                disabled={isViewMode}
              />
              <label htmlFor="isRecurring" className="ml-2 block text-sm text-gray-900">
                Evento recorrente
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
                onClick={() => navigate(`/gestao/agenda/${groupType}/edit/${id}`)}
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

export default AgendaForm;