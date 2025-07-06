import React, { createContext, useState, useContext, ReactNode } from 'react';
import { login as apiLogin, logout as apiLogout } from '../services/api';
import { useNavigate } from 'react-router-dom';

interface AuthContextType {
    isAuthenticated: boolean;
    login: (user: string, pass: string) => Promise<{ success: boolean; message: string }>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => !!sessionStorage.getItem('authToken'));
    const navigate = useNavigate();

    const login = async (user: string, pass: string) => {
        const response = await apiLogin(user, pass);
        if (response.success) {
            setIsAuthenticated(true);
        }
        return response;
    };

    const logout = async () => {
        await apiLogout();
        setIsAuthenticated(false);
        navigate('/gestao/login');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
