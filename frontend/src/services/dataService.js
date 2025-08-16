// A simple service for CRUD operations using localStorage
const PREFIX = 'setor_musical_';

const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
};

const getStorageKey = (entityName, group = null) => {
  let key = `${PREFIX}${entityName}`;
  if (group) {
    key += `_${group}`;
  }
  return key;
};

// Initialize data in localStorage if it doesn't exist
const initializeData = (entityName, group = null, initialData = []) => {
  const key = getStorageKey(entityName, group);
  if (!localStorage.getItem(key)) {
    localStorage.setItem(key, JSON.stringify(initialData));
  }
  return getAll(entityName, group);
};

// Get all items
const getAll = (entityName, group = null) => {
  const key = getStorageKey(entityName, group);
  try {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error(`Error getting ${entityName}:`, error);
    return [];
  }
};

// Get single item by ID
const getById = (entityName, id, group = null) => {
  const items = getAll(entityName, group);
  return items.find(item => item.id === id) || null;
};

// Create new item
const create = (entityName, item, group = null) => {
  const items = getAll(entityName, group);
  const newItem = {
    ...item,
    id: generateId(),
    createdAt: new Date().toISOString()
  };
  
  const updatedItems = [...items, newItem];
  const key = getStorageKey(entityName, group);
  
  localStorage.setItem(key, JSON.stringify(updatedItems));
  return newItem;
};

// Update existing item
const update = (entityName, id, updates, group = null) => {
  const items = getAll(entityName, group);
  const itemIndex = items.findIndex(item => item.id === id);
  
  if (itemIndex === -1) {
    throw new Error(`Item with ID ${id} not found`);
  }
  
  const updatedItem = {
    ...items[itemIndex],
    ...updates,
    updatedAt: new Date().toISOString()
  };
  
  const updatedItems = [
    ...items.slice(0, itemIndex),
    updatedItem,
    ...items.slice(itemIndex + 1)
  ];
  
  const key = getStorageKey(entityName, group);
  localStorage.setItem(key, JSON.stringify(updatedItems));
  
  return updatedItem;
};

// Delete item by ID
const remove = (entityName, id, group = null) => {
  const items = getAll(entityName, group);
  const filteredItems = items.filter(item => item.id !== id);
  
  if (filteredItems.length === items.length) {
    throw new Error(`Item with ID ${id} not found`);
  }
  
  const key = getStorageKey(entityName, group);
  localStorage.setItem(key, JSON.stringify(filteredItems));
  
  return id;
};

// Search items by text in specified fields
const search = (entityName, query, fields, group = null) => {
  if (!query) return getAll(entityName, group);
  
  const items = getAll(entityName, group);
  const normalizedQuery = query.toLowerCase();
  
  return items.filter(item => {
    return fields.some(field => {
      const value = item[field];
      if (!value) return false;
      return value.toString().toLowerCase().includes(normalizedQuery);
    });
  });
};

const dataService = {
  initializeData,
  getAll,
  getById,
  create,
  update,
  remove,
  search
};

export default dataService;