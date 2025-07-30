// frontend/src/pages/admin/AdminDashboard.tsx
// Versão 15 - 29/07/2025 05:50 - Implementa a UI completa do painel de gestão

import React, { useState, useEffect, useCallback } from 'react';
import * as api from '../../services/api';
import { User } from '../../types'; // Importe outros tipos conforme necessário
import { useAuth } from '../../context/AuthContext';
import {
  Box,
  Button,
  Container,
  Tabs,
  Tab,
  Typography,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
} from '@mui/material';
import { Edit, Delete } from '@mui/icons-material'; // Ícones do Material-UI

// Tipos para controlar as abas
type MainTab = 'coral' | 'orquestra' | 'usuarios';
type SubTab = 'repertorio' | 'agenda' | 'recados' | 'galeria';

const AdminDashboard: React.FC = () => {
  const { logout } = useAuth();
  const [mainTab, setMainTab] = useState<MainTab>('coral');
  const [subTab, setSubTab] = useState<SubTab>('repertorio');
  const [data, setData] = useState<any>({ usuarios: [] }); // Estado para armazenar os dados da API
  const [loading, setLoading] = useState(true);

  const handleMainTabChange = (event: React.SyntheticEvent, newValue: MainTab) => {
    setMainTab(newValue);
    // Reseta a sub-aba ao trocar de aba principal, se aplicável
    if (newValue === 'coral' || newValue === 'orquestra') {
      setSubTab('repertorio');
    }
  };

  const handleSubTabChange = (event: React.SyntheticEvent, newValue: SubTab) => {
    setSubTab(newValue);
  };

  // Função para carregar todos os dados da API
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      // Exemplo: Carregando apenas usuários por enquanto
      const usersData = await api.adminGetUsers();
      setData({ usuarios: usersData });
      // Chame aqui as outras funções da API para carregar mais dados
      // Ex: const recadosData = await api.adminGetRecados();
      // setData(prev => ({ ...prev, recados: recadosData }));
    } catch (error) {
      console.error("Falha ao carregar dados do admin:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Função para renderizar o conteúdo da aba selecionada
  const renderContent = () => {
    if (loading) {
      return <CircularProgress sx={{ mt: 4 }} />;
    }

    if (mainTab === 'usuarios') {
      return (
        <TableContainer component={Paper} sx={{ mt: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.usuarios.map((user: User) => (
                <TableRow key={user.id}>
                  <TableCell>{user.id}</TableCell>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>
                    <IconButton size="small"><Edit /></IconButton>
                    <IconButton size="small"><Delete /></IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      );
    }
    
    // Renderiza o conteúdo das sub-abas para Coral e Orquestra
    if (mainTab === 'coral' || mainTab === 'orquestra') {
        return <Typography sx={{ mt: 2 }}>Conteúdo para {mainTab} - {subTab}</Typography>;
    }

    return null;
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography component="h1" variant="h4">
          Painel de Administração
        </Typography>
        <Button variant="outlined" onClick={logout}>
          Sair
        </Button>
      </Box>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2 }}>
        <Tabs value={mainTab} onChange={handleMainTabChange}>
          <Tab label="Coral" value="coral" />
          <Tab label="Orquestra" value="orquestra" />
          <Tab label="Usuários" value="usuarios" />
        </Tabs>
      </Box>

      {(mainTab === 'coral' || mainTab === 'orquestra') && (
        <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'action.hover' }}>
          <Tabs value={subTab} onChange={handleSubTabChange} centered>
            <Tab label="Repertório" value="repertorio" />
            <Tab label="Agenda" value="agenda" />
            <Tab label="Recados" value="recados" />
            <Tab label="Galeria" value="galeria" />
          </Tabs>
        </Box>
      )}

      <Box sx={{ mt: 3 }}>
        {renderContent()}
      </Box>
    </Container>
  );
};

export default AdminDashboard;
