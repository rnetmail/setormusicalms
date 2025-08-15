// API service for interacting with the backend
// This is a mock service for now, in a real app this would connect to a Django backend

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Ocorreu um erro ao processar a solicitação');
  }
  return response.json();
};

// Authentication services
export const authService = {
  // Login user
  login: async (username, password) => {
    try {
      // In a real app, this would call the API
      // For now, simulate a successful login with mock data
      if (username === 'admin' && password === 'admin') {
        return { 
          success: true, 
          user: {
            id: 1,
            username: 'admin',
            name: 'Administrador',
            email: 'admin@example.com',
            roles: ['admin'],
            token: 'fake-jwt-token'
          }
        };
      }
      throw new Error('Credenciais inválidas');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('user');
    return { success: true };
  },

  // Get current user from localStorage
  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
};

// Repertoire services
export const repertoireService = {
  // Get all repertoires for a group
  getAll: async (group) => {
    try {
      // In a real app, this would fetch from the API
      // For now, return mock data
      return {
        success: true,
        data: [
          {
            id: 1,
            title: 'Ave Maria',
            composer: 'Franz Schubert',
            arranger: 'N/A',
            category: 'Sacra',
            group,
            dateAdded: '2023-01-15',
            notes: 'Peça tradicional do repertório',
            sheetMusicUrl: '/files/ave_maria.pdf',
            audioUrl: '/files/ave_maria.mp3',
          },
          {
            id: 2,
            title: 'Hallelujah',
            composer: 'Leonard Cohen',
            arranger: 'João Silva',
            category: 'Popular',
            group,
            dateAdded: '2023-02-10',
            notes: 'Arranjo a 4 vozes',
            sheetMusicUrl: '/files/hallelujah.pdf',
            audioUrl: '/files/hallelujah.mp3',
          },
          {
            id: 3,
            title: 'Ode à Alegria',
            composer: 'Ludwig van Beethoven',
            arranger: 'N/A',
            category: 'Clássica',
            group,
            dateAdded: '2023-03-05',
            notes: '9ª Sinfonia, 4º movimento',
            sheetMusicUrl: '/files/ode_a_alegria.pdf',
            audioUrl: '/files/ode_a_alegria.mp3',
          },
        ]
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Get a single repertoire item
  getById: async (id) => {
    try {
      // Mock implementation
      return {
        success: true,
        data: {
          id: parseInt(id),
          title: 'Ave Maria',
          composer: 'Franz Schubert',
          arranger: 'N/A',
          category: 'Sacra',
          group: 'coral',
          dateAdded: '2023-01-15',
          notes: 'Peça tradicional do repertório',
          sheetMusicUrl: '/files/ave_maria.pdf',
          audioUrl: '/files/ave_maria.mp3',
        }
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Create a new repertoire item
  create: async (repertoireData) => {
    try {
      // Mock implementation
      return {
        success: true,
        data: {
          id: Math.floor(Math.random() * 1000) + 10,
          ...repertoireData,
          dateAdded: new Date().toISOString().split('T')[0]
        }
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Update a repertoire item
  update: async (id, repertoireData) => {
    try {
      // Mock implementation
      return {
        success: true,
        data: {
          id: parseInt(id),
          ...repertoireData
        }
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Delete a repertoire item
  delete: async (id) => {
    try {
      // Mock implementation
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
};

// Announcements (Recados) services
export const announcementService = {
  // Get all announcements for a group
  getAll: async (group) => {
    try {
      // Mock implementation
      return {
        success: true,
        data: [
          {
            id: 1,
            title: 'Ensaio Geral',
            content: 'Ensaio geral neste sábado às 14h no salão principal.',
            group,
            publishedAt: '2023-06-20',
            importance: 'alta',
            author: 'Maria Coordenação'
          },
          {
            id: 2,
            title: 'Partituras Atualizadas',
            content: 'As novas partituras estão disponíveis para download na área de repertório.',
            group,
            publishedAt: '2023-06-18',
            importance: 'média',
            author: 'João Regente'
          },
          {
            id: 3,
            title: 'Uniforme para Apresentação',
            content: 'Uniforme para a apresentação do dia 30: roupa preta e lenço azul.',
            group,
            publishedAt: '2023-06-15',
            importance: 'alta',
            author: 'Pedro Coordenação'
          },
        ]
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Other announcement methods (getById, create, update, delete) would follow the same pattern as repertoireService
};

// Events (Agenda) services
export const eventService = {
  // Get all events for a group
  getAll: async (group) => {
    try {
      // Mock implementation
      return {
        success: true,
        data: [
          {
            id: 1,
            title: 'Ensaio Regular',
            description: 'Ensaio semanal com foco no repertório para a próxima apresentação.',
            location: 'Sala de Ensaios',
            startDate: '2023-07-01T14:00:00',
            endDate: '2023-07-01T16:00:00',
            group,
            type: 'ensaio'
          },
          {
            id: 2,
            title: 'Apresentação na Igreja',
            description: 'Apresentação durante a celebração dominical.',
            location: 'Igreja Central',
            startDate: '2023-07-09T10:00:00',
            endDate: '2023-07-09T11:30:00',
            group,
            type: 'apresentação'
          },
          {
            id: 3,
            title: 'Workshop de Técnica Vocal',
            description: 'Workshop especial com a professora Ana Luísa.',
            location: 'Auditório Principal',
            startDate: '2023-07-15T09:00:00',
            endDate: '2023-07-15T12:00:00',
            group,
            type: 'workshop'
          },
        ]
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Other event methods (getById, create, update, delete) would follow the same pattern as repertoireService
};

// Gallery services
export const galleryService = {
  // Get all gallery items for a group
  getAll: async (group) => {
    try {
      // Mock implementation
      return {
        success: true,
        data: [
          {
            id: 1,
            title: 'Apresentação de Natal 2022',
            description: 'Apresentação especial de Natal no Teatro Municipal.',
            date: '2022-12-20',
            type: 'video',
            url: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
            thumbnailUrl: '/assets/images/natal_2022_thumbnail.jpg',
            group
          },
          {
            id: 2,
            title: 'Festival de Música Sacra',
            description: 'Participação no Festival Internacional de Música Sacra.',
            date: '2023-03-15',
            type: 'album',
            photos: [
              '/assets/images/festival_1.jpg',
              '/assets/images/festival_2.jpg',
              '/assets/images/festival_3.jpg',
            ],
            group
          },
          {
            id: 3,
            title: 'Concerto de Aniversário',
            description: 'Concerto comemorativo dos 15 anos do grupo.',
            date: '2023-05-10',
            type: 'video',
            url: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
            thumbnailUrl: '/assets/images/aniversario_thumbnail.jpg',
            group
          },
        ]
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Other gallery methods (getById, create, update, delete) would follow the same pattern as repertoireService
};

// User management services
export const userService = {
  // Get all users
  getAll: async () => {
    try {
      // Mock implementation
      return {
        success: true,
        data: [
          {
            id: 1,
            username: 'admin',
            name: 'Administrador',
            email: 'admin@example.com',
            roles: ['admin'],
            active: true,
            lastLogin: '2023-06-20T08:30:45'
          },
          {
            id: 2,
            username: 'maria',
            name: 'Maria Silva',
            email: 'maria@example.com',
            roles: ['coordinator'],
            active: true,
            lastLogin: '2023-06-19T14:22:10'
          },
          {
            id: 3,
            username: 'joao',
            name: 'João Santos',
            email: 'joao@example.com',
            roles: ['manager'],
            active: true,
            lastLogin: '2023-06-18T09:15:33'
          },
        ]
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  // Other user methods (getById, create, update, delete) would follow the same pattern as repertoireService
};

// Export default object with all services
export default {
  auth: authService,
  repertoire: repertoireService,
  announcements: announcementService,
  events: eventService,
  gallery: galleryService,
  users: userService
};