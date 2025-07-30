// frontend/src/services/api.ts
// Versão 08 - 29/07/2025 05:15 - Alinha todos os endpoints com o backend (/api/...) e corrige o header de autenticação

import axios from 'axios';
import { LoginCredentials, User } from '../types';

// Configura a URL base da API. Em produção, será uma rota relativa.
const API_URL = '/api';

// Cria uma instância do Axios para fazer as requisições
const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para adicionar o token de autenticação em todas as requisições
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            // CORREÇÃO: Usa o formato "Bearer" esperado pelo FastAPI
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// --- Funções da API ---

// Autenticação
export const login = async (credentials: LoginCredentials) => {
    // CORREÇÃO: Usa 'application/x-www-form-urlencoded' para o OAuth2PasswordRequestForm do FastAPI
    const params = new URLSearchParams();
    params.append('username', credentials.username);
    params.append('password', credentials.password);

    // CORREÇÃO: Endpoint ajustado para /auth/login
    const response = await apiClient.post('/auth/login', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
    
    // Armazena o token e retorna os dados
    if (response.data.access_token) {
        localStorage.setItem('authToken', response.data.access_token);
    }
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('authToken');
    // Não há necessidade de chamada à API para logout baseado em token JWT
};

// Funções de Admin (exemplo para usuários)
// Adicione aqui as outras chamadas de API para agenda, repertorio, etc.
export const adminGetUsers = async (): Promise<User[]> => {
    // CORREÇÃO: Endpoint ajustado para /users
    const response = await apiClient.get('/users/');
    return response.data;
};

// Adicione outras funções conforme necessário, por exemplo:
// export const adminGetRecados = async () => { ... }
// export const getGaleria = async (group: GroupType) => { ... }
