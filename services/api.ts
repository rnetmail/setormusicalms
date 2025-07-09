import { RepertorioItem, AgendaItem, RecadoItem, User, GroupType } from '../types';

const API_BASE_URL = '/api';

const getAuthToken = () => sessionStorage.getItem('authToken');

const apiFetch = async (url: string, options: RequestInit = {}) => {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Token ${token}`;
        console.log('Sending token:', token.substring(0, 10) + '...');
    } else {
        console.log('No token found in sessionStorage');
    }

    console.log('Making request to:', `${API_BASE_URL}${url}`);
    console.log('Headers:', headers);

    const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers,
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
            console.error('Error response:', errorData);
        } catch (e) {
            errorData = { message: response.statusText };
            console.error('Error parsing response:', e);
        }
        throw new Error(errorData.detail || errorData.message || errorData.error || 'Ocorreu um erro na API');
    }

    if (response.status === 204) { // No Content
        return null;
    }

    return response.json();
};


// Public API
export const getRepertorio = (type: GroupType) => apiFetch(`/repertorio/?type=${type}`);
export const getAgenda = (group: GroupType) => apiFetch(`/agenda/?group=${group}`);
export const getRecados = (group: GroupType) => apiFetch(`/recados/?group=${group}`);
export const getHistoria = () => apiFetch('/historia/');
export const getGaleria = (group: GroupType) => apiFetch(`/galeria/?group=${group}`);

// Auth API
export const login = async (username: string, pass: string) => {
    try {
        const response = await apiFetch('/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password: pass }),
        });
        if (response.token) {
            sessionStorage.setItem('authToken', response.token);
            return { success: true, message: 'Login bem-sucedido!' };
        }
        return { success: false, message: 'Token não recebido.' };
    } catch (error: any) {
        return { success: false, message: error.message || 'Usuário ou senha inválidos.' };
    }
};

export const logout = async () => {
    try {
        await apiFetch('/logout/', { method: 'POST' });
    } catch (error) {
        console.error("Logout failed on server, but proceeding.", error);
    } finally {
        sessionStorage.removeItem('authToken');
    }
};


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
