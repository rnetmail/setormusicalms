// Conteúdo corrigido para services/api.ts

import { RepertorioItem, AgendaItem, RecadoItem, User, GroupType } from './types';

const API_BASE_URL = '/api';

const getAuthToken = () => sessionStorage.getItem('authToken');

const apiFetch = async (url: string, options: RequestInit = {}) => {
    const token = getAuthToken();
    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers,
    });

    if (response.status === 204) {
        return null;
    }

    const responseData = await response.json();

    if (!response.ok) {
        const errorMessage = responseData.detail || JSON.stringify(responseData);
        throw new Error(errorMessage || 'Ocorreu um erro na chamada da API');
    }

    return responseData;
};

// --- Autenticação ---
export const login = async (username: string, pass: string) => {
    // FastAPI/OAuth2 espera os dados de login em um formato 'form-data'.
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', pass);

    try {
        // CORREÇÃO: O endpoint correto é /auth/token
        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData.toString(),
        });

        const responseData = await response.json();
        if (!response.ok) {
             throw new Error(responseData.detail || 'Usuário ou senha inválidos.');
        }

        if (responseData.access_token) {
            sessionStorage.setItem('authToken', responseData.access_token);
            return { success: true, message: 'Login bem-sucedido!' };
        }
        return { success: false, message: 'Token de acesso não recebido.' };
    } catch (error: any) {
        return { success: false, message: error.message };
    }
};

export const logout = () => {
    // Com JWT, o logout é feito apenas no lado do cliente.
    sessionStorage.removeItem('authToken');
};

// --- As outras funções da API permanecem as mesmas ---

// Rotas Públicas
export const getRepertorio = (type: GroupType) => apiFetch(`/repertorio?type_filter=${type}`);
export const getAgenda = (group: GroupType) => apiFetch(`/agenda?group_filter=${group}`);
// Adicione aqui as funções para Recados, História e Galeria quando o backend estiver pronto

// CRUD Genérico
const createItem = <T,>(endpoint: string, item: Omit<T, 'id'>) => apiFetch(endpoint, { method: 'POST', body: JSON.stringify(item) });
const updateItem = <T extends { id: any }>(endpoint: string, item: Partial<T> & { id: any }) => apiFetch(`${endpoint}/${item.id}`, { method: 'PATCH', body: JSON.stringify(item) });
const deleteItem = (endpoint: string, id: string | number) => apiFetch(`${endpoint}/${id}`, { method: 'DELETE' });

// CRUDs Específicos
export const adminGetRepertorio = () => apiFetch('/repertorio');
// ... e assim por diante para as outras funções de admin.


// Generic CRUD functions for Admin
const createItem = <T,>(endpoint: string, item: T) => apiFetch(endpoint, { method: 'POST', body: JSON.stringify(item) });
const updateItem = <T extends {id: any}>(endpoint: string, item: T) => apiFetch(`${endpoint}${item.id}/`, { method: 'PUT', body: JSON.stringify(item) });
const partialUpdateItem = <T extends {id: any}>(endpoint: string, item: Partial<T>) => apiFetch(`${endpoint}${item.id}/`, { method: 'PATCH', body: JSON.stringify(item) });
const deleteItem = (endpoint: string, id: string | number) => apiFetch(`${endpoint}${id}/`, { method: 'DELETE' });

// Admin CRUD API
export const adminGetRepertorio = () => apiFetch('/repertorio/');
export const adminCreateRepertorio = (item: Omit<RepertorioItem, 'id'>) => createItem('/repertorio/', item);
export const adminUpdateRepertorio = (item: RepertorioItem) => updateItem('/repertorio/', item);
export const adminDeleteRepertorio = (id: string) => deleteItem('/repertorio/', id);

export const adminGetAgenda = () => apiFetch('/agenda/');
export const adminCreateAgenda = (item: Omit<AgendaItem, 'id'>) => createItem('/agenda/', item);
export const adminUpdateAgenda = (item: AgendaItem) => updateItem('/agenda/', item);
export const adminDeleteAgenda = (id: string) => deleteItem('/agenda/', id);

export const adminGetRecados = () => apiFetch('/recados/');
export const adminCreateRecado = (item: Omit<RecadoItem, 'id'>) => createItem('/recados/', item);
export const adminUpdateRecado = (item: RecadoItem) => updateItem('/recados/', item);
export const adminDeleteRecado = (id: string) => deleteItem('/recados/', id);

export const adminGetUsers = () => apiFetch('/users/');
export const adminCreateUser = (item: Omit<User, 'id'>) => createItem('/users/', item);
export const adminUpdateUser = (item: Partial<User> & { id: string }) => {
    // Use PATCH to avoid needing the full user object, especially the password
    return partialUpdateItem('/users/', item);
};
export const adminDeleteUser = (id: string) => deleteItem('/users/', id);
