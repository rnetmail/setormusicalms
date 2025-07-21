// services/api.ts
// Versão 03 21/07/2025 18:20
import { RepertorioItem, AgendaItem, RecadoItem, User, GroupType, HistoriaItem, GaleriaItem } from '../types';

const API_BASE_URL = '/api';

const getAuthToken = () => sessionStorage.getItem('authToken');

// Função base para todas as requisições à API
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

    if (response.status === 204) { // No Content
        return null;
    }

    const responseData = await response.json();

    if (!response.ok) {
        const errorMessage = responseData.detail || JSON.stringify(responseData);
        throw new Error(errorMessage || 'Ocorreu um erro na API');
    }

    return responseData;
};

// --- Funções Públicas ---
export const getRepertorio = (type: GroupType): Promise<RepertorioItem[]> => apiFetch(`/repertorio?type_filter=${type}`);
export const getAgenda = (group: GroupType): Promise<AgendaItem[]> => apiFetch(`/agenda?group_filter=${group}`);
export const getRecados = (group: GroupType): Promise<RecadoItem[]> => apiFetch(`/recados?group_filter=${group}`);
// ATUALIZADO: Funções agora fazem chamadas reais à API
export const getHistoria = (): Promise<HistoriaItem[]> => apiFetch('/historia/');
export const getGaleria = (group: GroupType): Promise<GaleriaItem[]> => apiFetch(`/galeria/${group}`);


// --- Funções de Autenticação ---
export const login = async (username: string, pass: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', pass);

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
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
    sessionStorage.removeItem('authToken');
};

// --- Funções Genéricas de Admin (CRUD) ---
const createItem = <T,>(endpoint: string, item: T) => apiFetch(endpoint, { method: 'POST', body: JSON.stringify(item) });
const updateItem = <T extends { id: any }>(endpoint: string, item: Partial<T>) => apiFetch(`${endpoint}/${item.id}`, { method: 'PUT', body: JSON.stringify(item) });
const deleteItem = (endpoint: string, id: string | number) => apiFetch(`${endpoint}/${id}`, { method: 'DELETE' });

// --- Funções Específicas para cada Módulo do Admin ---

// Repertório
export const adminGetRepertorio = () => apiFetch('/repertorio/');
export const adminCreateRepertorio = (item: Omit<RepertorioItem, 'id'>) => createItem('/repertorio/', item);
export const adminUpdateRepertorio = (item: Partial<RepertorioItem> & { id: string }) => updateItem('/repertorio', item);
export const adminDeleteRepertorio = (id: string) => deleteItem('/repertorio', id);

// Agenda
export const adminGetAgenda = () => apiFetch('/agenda/');
export const adminCreateAgenda = (item: Omit<AgendaItem, 'id'>) => createItem('/agenda/', item);
export const adminUpdateAgenda = (item: Partial<AgendaItem> & { id: string }) => updateItem('/agenda', item);
export const adminDeleteAgenda = (id: string) => deleteItem('/agenda', id);

// Recados
export const adminGetRecados = () => apiFetch('/recados/');
export const adminCreateRecado = (item: Omit<RecadoItem, 'id'>) => createItem('/recados/', item);
export const adminUpdateRecado = (item: Partial<RecadoItem> & { id: string }) => updateItem('/recados', item);
export const adminDeleteRecado = (id: string) => deleteItem('/recados', id);

// Usuários
export const adminGetUsers = () => apiFetch('/users/');
export const adminCreateUser = (item: Omit<User, 'id'>) => createItem('/users/', item);
export const adminUpdateUser = (item: Partial<User> & { id: string }) => updateItem('/users', item);
export const adminDeleteUser = (id: string) => deleteItem('/users', id);
