// pages/admin/AdminDashboard.tsx
// Versão 26 - Lógica de abas e UI corrigidas com Material-UI

import React, { useState, useEffect, useCallback } from 'react';
import * as api from '../../services/api';
import { RepertorioItem, AgendaItem, RecadoItem, User, GroupType, HistoriaItem, GaleriaItem } from '../../types';
import { useAuth } from '../../context/AuthContext';

// Importando componentes do Material-UI para uma interface bonita
import { Box, Tabs, Tab, Button, CircularProgress, Typography, Paper } from '@mui/material';

// Tipos para controlar as abas, conforme sua especificação
type MainTab = 'coral' | 'orquestra' | 'historia' | 'usuarios';
type SubTab = 'repertorio' | 'agenda' | 'recados' | 'galeria';
type Entity = RepertorioItem | AgendaItem | RecadoItem | User | HistoriaItem | GaleriaItem;

// Um componente simples para exibir o conteúdo de cada aba
const TabContent: React.FC<{ title: string; items: Entity[]; onAdd: () => void }> = ({ title, items, onAdd }) => (
    <Paper elevation={3} sx={{ p: 3, mt: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h5">{title}</Typography>
            <Button variant="contained" onClick={onAdd}>Adicionar Novo</Button>
        </Box>
        <hr style={{ margin: '16px 0' }} />
        {items.length === 0 ? (
            <Typography>Nenhum item encontrado.</Typography>
        ) : (
            <ul>
                {items.map((item, index) => (
                    <li key={index}>
                        {/* Adapte para mostrar o título ou nome do item */}
                        <Typography component="span">{(item as any).title || (item as any).name || (item as any).username}</Typography>
                        {/* Adicionar botões de editar/excluir aqui */}
                    </li>
                ))}
            </ul>
        )}
    </Paper>
);

const AdminDashboard: React.FC = () => {
    const { logout } = useAuth();
    const [mainTab, setMainTab] = useState<MainTab>('coral');
    const [subTab, setSubTab] = useState<SubTab>('repertorio');
    
    const [data, setData] = useState<{
        repertorio: RepertorioItem[]; agenda: AgendaItem[]; recados: RecadoItem[];
        historia: HistoriaItem[]; galeria: GaleriaItem[]; usuarios: User[];
    }>({ repertorio: [], agenda: [], recados: [], historia: [], galeria: [], usuarios: [] });
    
    const [loading, setLoading] = useState(true);

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const [repertorio, agenda, recados, historia, coralGaleria, orquestraGaleria, usuarios] = await Promise.all([
                api.adminGetRepertorio(), api.adminGetAgenda(), api.adminGetRecados(),
                api.getHistoria(), api.getGaleria(GroupType.Coral), api.getGaleria(GroupType.Orquestra),
                api.adminGetUsers()
            ]);
            setData({ 
                repertorio: repertorio || [], agenda: agenda || [], recados: recados || [], 
                historia: historia || [], galeria: [...(coralGaleria || []), ...(orquestraGaleria || [])], 
                usuarios: (usuarios as User[]) || [] 
            });
        } catch (error) {
            console.error("Falha ao carregar os dados:", error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { fetchData(); }, [fetchData]);

    const handleOpenModal = () => {
        // Lógica para abrir o modal de adição/edição
        alert('Abrir modal para adicionar novo item!');
    };

    const renderCurrentTab = () => {
        if (mainTab === 'usuarios') {
            return <TabContent title="Gerenciamento de Usuários" items={data.usuarios} onAdd={handleOpenModal} />;
        }
        if (mainTab === 'historia') {
            return <TabContent title="Gerenciamento da História" items={data.historia} onAdd={handleOpenModal} />;
        }

        // Lógica para Coral e Orquestra
        const groupFilter = mainTab;
        let items: Entity[] = [];
        let title = "";

        switch (subTab) {
            case 'repertorio':
                items = data.repertorio.filter(item => item.type === groupFilter);
                title = `Repertório - ${mainTab}`;
                break;
            case 'agenda':
                items = data.agenda.filter(item => item.group === groupFilter);
                title = `Agenda - ${mainTab}`;
                break;
            case 'recados':
                items = data.recados.filter(item => item.group === groupFilter);
                title = `Recados - ${mainTab}`;
                break;
            case 'galeria':
                items = data.galeria.filter(item => item.group === groupFilter);
                title = `Galeria - ${mainTab}`;
                break;
        }
        return <TabContent title={title} items={items} onAdd={handleOpenModal} />;
    };

    if (loading) {
        return <Box display="flex" justifyContent="center" alignItems="center" height="100vh"><CircularProgress /></Box>;
    }

    return (
        <Box sx={{ p: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h4">Painel de Administração</Typography>
                <Button variant="outlined" onClick={logout}>Sair</Button>
            </Box>

            <Paper elevation={1}>
                <Tabs value={mainTab} onChange={(_, newValue) => setMainTab(newValue)} centered>
                    <Tab label="Coral" value="coral" />
                    <Tab label="Orquestra" value="orquestra" />
                    <Tab label="História" value="historia" />
                    <Tab label="Usuários" value="usuarios" />
                </Tabs>
            </Paper>

            {(mainTab === 'coral' || mainTab === 'orquestra') && (
                <Box sx={{ mt: 2, borderBottom: 1, borderColor: 'divider' }}>
                    <Tabs value={subTab} onChange={(_, newValue) => setSubTab(newValue)}>
                        <Tab label="Repertório" value="repertorio" />
                        <Tab label="Agenda" value="agenda" />
                        <Tab label="Recados" value="recados" />
                        <Tab label="Galeria" value="galeria" />
                    </Tabs>
                </Box>
            )}

            <Box sx={{ mt: 3 }}>
                {renderCurrentTab()}
            </Box>
        </Box>
    );
};

export default AdminDashboard;
