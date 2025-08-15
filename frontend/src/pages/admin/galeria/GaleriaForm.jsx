import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FaSave, FaArrowLeft, FaTimes, FaPlus, FaTrash } from 'react-icons/fa';
import FormField from '../../../components/admin/FormField';
import dataService from '../../../services/dataService';

const ImageItem = ({ index, image, onChange, onRemove, disabled }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    onChange(index, { ...image, [name]: value });
  };

  return (
    <div className="p-4 border rounded-md mb-3 relative">
      <div className="flex flex-col md:flex-row gap-4">
        <div className="md:w-1/3">
          <FormField
            label="URL da Imagem"
            name="url"
            value={image.url || ''}
            onChange={handleChange}
            placeholder="/images/ImageURL.jpg"
            required
            disabled={disabled}
          />
          <div className="mt-2">
            <img 
              src={image.url || 'https://via.placeholder.com/300x200?text=Sem+Imagem'} 
              alt="Preview" 
              className="w-full h-32 object-cover rounded border"
              onError={(e) => {
                e.target.onerror = null; 
                e.target.src = 'https://via.placeholder.com/300x200?text=Erro+de+Imagem';
              }}
            />
          </div>
        </div>
        <div className="md:w-2/3">
          <FormField
            label="Legenda"
            name="caption"
            value={image.caption || ''}
            onChange={handleChange}
            placeholder="Descrição da imagem"
            disabled={disabled}
          />
        </div>
      </div>
      {!disabled && (
        <button
          type="button"
          onClick={() => onRemove(index)}
          className="absolute top-3 right-3 text-red-500 hover:text-red-700"
        >
          <FaTrash />
        </button>
      )}
    </div>
  );
};

const GaleriaForm = () => {
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
    coverImage: '',
    images: [{ url: '', caption: '' }]
  });
  
  const [loading, setLoading] = useState(isEditMode || isViewMode);
  const [errors, setErrors] = useState({});
  
  useEffect(() => {
    const fetchItem = async () => {
      if (isEditMode || isViewMode) {
        try {
          const item = dataService.getById('galeria', id, groupType);
          
          if (item) {
            setFormData(item);
          } else {
            // Handle item not found
            navigate(`/gestao/galeria/${groupType}`);
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

  const handleImageChange = (index, updatedImage) => {
    const updatedImages = [...formData.images];
    updatedImages[index] = updatedImage;
    
    setFormData(prev => ({
      ...prev,
      images: updatedImages
    }));
  };

  const handleAddImage = () => {
    setFormData(prev => ({
      ...prev,
      images: [...prev.images, { url: '', caption: '' }]
    }));
  };

  const handleRemoveImage = (index) => {
    const updatedImages = formData.images.filter((_, i) => i !== index);
    setFormData(prev => ({
      ...prev,
      images: updatedImages
    }));
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
    
    if (!formData.coverImage.trim()) {
      newErrors.coverImage = 'Imagem de capa é obrigatória';
    }
    
    // Check if at least one image has a URL
    const hasValidImage = formData.images.some(img => img.url.trim() !== '');
    if (!hasValidImage) {
      newErrors.images = 'Adicione pelo menos uma imagem com URL válida';
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
      
      // Filter out empty images
      const filteredImages = formData.images.filter(img => img.url.trim() !== '');
      const dataToSave = {
        ...formData,
        images: filteredImages
      };
      
      if (isNewMode) {
        // Create new item
        await dataService.create('galeria', {
          ...dataToSave,
          type: groupType
        }, groupType);
      } else if (isEditMode) {
        // Update existing item
        await dataService.update('galeria', id, dataToSave, groupType);
      }
      
      // Redirect back to list
      navigate(`/gestao/galeria/${groupType}`);
    } catch (error) {
      console.error('Error saving item:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCancel = () => {
    navigate(`/gestao/galeria/${groupType}`);
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
          {isViewMode ? 'Visualizar Galeria' : isEditMode ? 'Editar Galeria' : 'Nova Galeria'}
        </h1>
      </div>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 gap-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
            
            <div>
              <FormField
                label="Imagem de Capa (URL)"
                name="coverImage"
                value={formData.coverImage}
                onChange={handleChange}
                placeholder="/images/ImageURL.jpg"
                required
                error={errors.coverImage}
                disabled={isViewMode}
              />
              
              {formData.coverImage && (
                <div className="mt-2 border rounded p-2">
                  <img 
                    src={formData.coverImage} 
                    alt="Imagem de capa" 
                    className="h-40 object-cover mx-auto"
                    onError={(e) => {
                      e.target.onerror = null; 
                      e.target.src = 'https://via.placeholder.com/300x200?text=Erro+de+Imagem';
                    }}
                  />
                </div>
              )}
            </div>
            
            <div>
              <div className="flex justify-between items-center mb-3">
                <label className="block text-sm font-medium text-gray-700">
                  Imagens da Galeria
                </label>
                {!isViewMode && (
                  <button
                    type="button"
                    onClick={handleAddImage}
                    className="bg-blue-50 text-blue-600 px-3 py-1 rounded border border-blue-200 hover:bg-blue-100 flex items-center text-sm"
                  >
                    <FaPlus className="mr-1" /> Adicionar Imagem
                  </button>
                )}
              </div>
              
              {errors.images && (
                <p className="mt-1 mb-2 text-sm text-red-500">{errors.images}</p>
              )}
              
              {formData.images.map((image, index) => (
                <ImageItem
                  key={index}
                  index={index}
                  image={image}
                  onChange={handleImageChange}
                  onRemove={handleRemoveImage}
                  disabled={isViewMode}
                />
              ))}
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
                onClick={() => navigate(`/gestao/galeria/${groupType}/edit/${id}`)}
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

export default GaleriaForm;