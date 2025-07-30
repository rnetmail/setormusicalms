// frontend/src/context/AuthContext.tsx
// Versão 09 - 29/07/2025 05:20 - Simplifica o contexto e alinha com a api.ts

import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import * as api from '../services/api';
import { LoginCredentials, User } from '../types'; // Supondo que você tenha um tipo User

interface AuthContextType {
    isAuthenticated: boolean;
    user: User | null;
    login: (credentials: LoginCredentials) => Promise<void>;
    logout: () => void;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true); // Inicia como true para verificar o token inicial

    useEffect(() => {
        // Verifica se existe um token no localStorage ao carregar a aplicação
        const token = localStorage.getItem('authToken');
        if (token) {
            // Aqui você poderia decodificar o token para obter dados do usuário
            // ou fazer uma chamada a um endpoint /api/users/me para validar o token
            // e obter os dados do usuário.
            setIsAuthenticated(true);
            // Exemplo: setUser({ id: 1, username: 'admin', ... });
        }
        setLoading(false);
    }, []);

    const login = async (credentials: LoginCredentials) => {
        try {
            const data = await api.login(credentials);
            if (data.access_token) {
                setIsAuthenticated(true);
                // Opcional: decodificar token ou buscar dados do usuário
                // setUser(decodedUserData);
            }
        } catch (error) {
            console.error("Falha no login:", error);
            throw error; // Lança o erro para que o componente de login possa tratá-lo
        }
    };

    const logout = () => {
        api.logout();
        setUser(null);
        setIsAuthenticated(false);
        // Redireciona para a página de login
        window.location.href = '/login';
    };

    const value = {
        isAuthenticated,
        user,
        login,
        logout,
        loading,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth deve ser usado dentro de um AuthProvider');
    }
    return context;
};
