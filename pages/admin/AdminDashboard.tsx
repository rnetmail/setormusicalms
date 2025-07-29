// pages/admin/AdminDashboard.tsx
// Versão 25 - FINAL E CORRIGIDA

import React, { useState, useEffect, useCallback } from 'react';
import * as api from '../../services/api';
import { RepertorioItem, AgendaItem, RecadoItem, User, GroupType, HistoriaItem, GaleriaItem } from '../../types';
import { useAuth } from '../../context/AuthContext';
import Modal from '../../components/Modal'; // Supondo que você tenha um componente Modal
import { TrashIcon, PencilIcon } from '../../components/icons'; // Supondo que tenha ícones

// Tipos para controlar as abas
type MainTab = 'coral' | 'orquestra' | 'historia' | 'usuarios';
type SubTab = 'repertorio' | 'agenda' | 'recados' | 'galeria';
type Entity = RepertorioItem | AgendaItem | RecadoItem | User | HistoriaItem | GaleriaItem;

const AdminDashboard: React.FC = () => {
    const { logout } = useAuth();
    const [mainTab, setMainTab] = useState<MainTab>('coral');
    const [subTab, setSubTab] = useState<SubTab>('repertorio');
    
    const [data, setData] = useState<{
        repertorio: RepertorioItem[];
        agenda: AgendaItem[];
        recados: RecadoItem[];
        historia: HistoriaItem[];
        galeria: GaleriaItem[];
        usuarios: User[];
    }>({ repertorio: [], agenda: [], recados: [], historia: [], galeria: [], usuarios: [] });
    
    const [loading, setLoading] = useState(true); // Começa carregando
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingItem, setEditingItem] = useState<Entity | null>(null);
    const [formData, setFormData] = useState<Partial<Entity>>({});

    // Função para buscar todos os dados da API
    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const [repertorio, agenda, recados, historia, coralGaleria, orquestraGaleria, usuarios] = await Promise.all([
                api.adminGetRepertorio(),
                api.adminGetAgenda(),
                api.adminGetRecados(),
                api.getHistoria(),
                api.getGaleria(GroupType.Coral),
                api.getGaleria(GroupType.Orquestra),
                api.adminGetUsers()
            ]);
            setData({ 
                repertorio: repertorio || [], 
                agenda: agenda || [], 
                recados: recados || [], 
                historia: historia || [], 
                galeria: [...(coralGaleria || []), ...(orquestraGaleria || [])], 
                usuarios: (usuarios as User[]) || [] 
            });
        } catch (error) {
            console.error("Falha ao carregar os dados:", error);
            // Poderia adicionar um estado de erro aqui para mostrar uma mensagem ao usuário
        } finally {
            // Garante que o loading termine, mesmo em caso de erro
            setLoading(false);
        }
    }, []);

    // Executa a busca de dados quando o componente é montado
    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const handleOpenModal = (item: Entity | null = null) => {
        setEditingItem(item);
        setFormData(item || {}); // Inicia o formulário com os dados do item ou vazio
        setIsModalOpen(true);
    };
    
    const handleCloseModal = () => {
        setIsModalOpen(false);
        setEditingItem(null);
    };

    const handleSave = async () => {
        // Lógica para salvar (criar ou atualizar) o item.
        // Esta parte precisa ser implementada com as chamadas de API correspondentes.
        console.log("Salvando:", formData);
        await fetchData(); // Recarrega os dados após salvar
        handleCloseModal();
    };

    // Função para renderizar o conteúdo da aba selecionada
    const renderContent = () => {
        if (loading) {
            return <div>Carregando...</div>;
        }

        let items: Entity[] = [];
        let title = "";

        if (mainTab === 'usuarios') {
            items = data.usuarios;
            title = "Gerenciamento de Usuários";
        } else if (mainTab === 'historia') {
            items = data.historia;
            title = "Gerenciamento da História";
        } else {
            // Lógica para Coral e Orquestra
            const groupFilter = mainTab === 'coral' ? GroupType.Coral : GroupType.Orquestra;
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
        }

        return (
            <div>
                <h2>{title}</h2>
                <button onClick={() => handleOpenModal()}>Adicionar Novo</button>
                {items.length === 0 ? (
                    <p>Nenhum item encontrado.</p>
                ) : (
                    <ul>
                        {items.map((item, index) => (
                            <li key={index}>
                                {/* Adapte para mostrar o título ou nome do item */}
                                {(item as any).title || (item as any).name || (item as any).username}
                                <button onClick={() => handleOpenModal(item)}><PencilIcon /></button>
                                <button><TrashIcon /></button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        );
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Painel de Administração</h1>
            <button onClick={logout}>Sair</button>
            
            <div>
                <h3>Grupos</h3>
                <button onClick={() => setMainTab('coral')} disabled={mainTab === 'coral'}>Coral</button>
                <button onClick={() => setMainTab('orquestra')} disabled={mainTab === 'orquestra'}>Orquestra</button>
                <button onClick={() => setMainTab('historia')} disabled={mainTab === 'historia'}>História</button>
                <button onClick={() => setMainTab('usuarios')} disabled={mainTab === 'usuarios'}>Usuários</button>
            </div>

            {(mainTab === 'coral' || mainTab === 'orquestra') && (
                <div>
                    <h4>Seções</h4>
                    <button onClick={() => setSubTab('repertorio')} disabled={subTab === 'repertorio'}>Repertório</button>
                    <button onClick={() => setSubTab('agenda')} disabled={subTab === 'agenda'}>Agenda</button>
                    <button onClick={() => setSubTab('recados')} disabled={subTab === 'recados'}>Recados</button>
                    <button onClick={() => setSubTab('galeria')} disabled={subTab === 'galeria'}>Galeria</button>
                </div>
            )}

            <hr />

            {renderContent()}

            {isModalOpen && (
                <Modal onClose={handleCloseModal}>
                    <h2>{editingItem ? 'Editar' : 'Adicionar'} Item</h2>
                    {/* Aqui viria o formulário dinâmico baseado em formData */}
                    <p>Formulário para {JSON.stringify(formData)}</p>
                    <button onClick={handleSave}>Salvar</button>
                </Modal>
            )}
        </div>
    );
};

export default AdminDashboard;
