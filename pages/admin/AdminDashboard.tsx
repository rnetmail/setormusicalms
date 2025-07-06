
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import * as api from '../../services/api';
import { RepertorioItem, AgendaItem, RecadoItem, User, GroupType, Naipe, OrquestraGrupo, UserRole } from '../../types';
import { useAuth } from '../../context/AuthContext';
import Modal from '../../components/Modal';
import { TrashIcon, PencilIcon } from '../../components/icons';

type MainTab = 'coral' | 'orquestra' | 'usuarios';
type SubTab = 'repertorio' | 'agenda' | 'recados';
type Entity = RepertorioItem | AgendaItem | RecadoItem | User;

const AdminDashboard: React.FC = () => {
    const { logout } = useAuth();
    const [mainTab, setMainTab] = useState<MainTab>('coral');
    const [subTab, setSubTab] = useState<SubTab>('repertorio');
    
    const [data, setData] = useState<{
        repertorio: RepertorioItem[];
        agenda: AgendaItem[];
        recados: RecadoItem[];
        usuarios: User[];
    }>({ repertorio: [], agenda: [], recados: [], usuarios: [] });
    
    const [loading, setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editingItem, setEditingItem] = useState<Entity | null>(null);
    const [formData, setFormData] = useState<Partial<Entity & { confirmPassword?: string }>>({});

    const fetchData = useCallback(async () => {
        setLoading(true);
        try {
            const [repertorio, agenda, recados, usuarios] = await Promise.all([
                api.adminGetRepertorio(),
                api.adminGetAgenda(),
                api.adminGetRecados(),
                api.adminGetUsers()
            ]);
            setData({ repertorio, agenda, recados, usuarios: usuarios as User[] });
        } catch (error) {
            console.error("Failed to fetch data:", error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const handleOpenModal = (item: Entity | null = null) => {
        setEditingItem(item);
        const groupType = mainTab === 'coral' ? GroupType.Coral : GroupType.Orquestra;
        
        let initialData: Partial<Entity> = { active: true };
        if (subTab === 'repertorio') initialData = { ...initialData, type: groupType, naipes: [], grupos: [] };
        if (subTab === 'agenda' || subTab === 'recados') initialData = { ...initialData, group: groupType };
        if (mainTab === 'usuarios') initialData = { ...initialData, role: UserRole.Maestro };
        
        setFormData(item || initialData);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setEditingItem(null);
        setFormData({});
    };
    
    const handleDelete = async (id: string) => {
        const currentTab = mainTab === 'usuarios' ? 'usuarios' : subTab;
        if (!window.confirm("Tem certeza que deseja excluir este item?")) return;
        
        try {
             switch (currentTab) {
                case 'repertorio': await api.adminDeleteRepertorio(id); break;
                case 'agenda': await api.adminDeleteAgenda(id); break;
                case 'recados': await api.adminDeleteRecado(id); break;
                case 'usuarios': await api.adminDeleteUser(id); break;
            }
            fetchData();
        } catch (error) {
            console.error("Failed to delete item:", error);
            alert("Falha ao excluir o item.");
        }
    }
    
    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        const currentTab = mainTab === 'usuarios' ? 'usuarios' : subTab;
        
        // User form validation
        if (currentTab === 'usuarios') {
            const userFormData = formData as Partial<User & { confirmPassword?: string }>;
            if (userFormData.password !== userFormData.confirmPassword) {
                alert("As senhas não coincidem.");
                return;
            }
            if (!editingItem && !userFormData.password) {
                alert("A senha é obrigatória para novos usuários.");
                return;
            }
            // Don't send password if it's not being changed
            if (editingItem && userFormData.password === '') {
                delete userFormData.password;
            }
            delete userFormData.confirmPassword;
        }

        try {
            if (editingItem) { // Update
                switch (currentTab) {
                    case 'repertorio': await api.adminUpdateRepertorio(formData as RepertorioItem); break;
                    case 'agenda': await api.adminUpdateAgenda(formData as AgendaItem); break;
                    case 'recados': await api.adminUpdateRecado(formData as RecadoItem); break;
                    case 'usuarios': await api.adminUpdateUser(formData as User); break;
                }
            } else { // Create
                 switch (currentTab) {
                    case 'repertorio': await api.adminCreateRepertorio(formData as Omit<RepertorioItem, 'id'>); break;
                    case 'agenda': await api.adminCreateAgenda(formData as Omit<AgendaItem, 'id'>); break;
                    case 'recados': await api.adminCreateRecado(formData as Omit<RecadoItem, 'id'>); break;
                    case 'usuarios': await api.adminCreateUser(formData as Omit<User, 'id'>); break;
                }
            }
            fetchData();
            handleCloseModal();
        } catch (error) {
             console.error("Failed to save item:", error);
            alert("Falha ao salvar o item.");
        }
    }

     const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value, type } = e.target;
        
        if (type === 'checkbox') {
            setFormData(prev => ({ ...prev, [name]: (e.target as HTMLInputElement).checked }));
        } else if (e.target.localName === 'select' && (e.target as HTMLSelectElement).multiple) {
            const selectedValues = Array.from((e.target as HTMLSelectElement).selectedOptions, option => option.value);
            setFormData(prev => ({ ...prev, [name]: selectedValues }));
        } else {
            setFormData(prev => ({ ...prev, [name]: value }));
        }
    };

    const displayedData = useMemo(() => {
        if (mainTab === 'usuarios') return data.usuarios;
        const groupFilter = mainTab === 'coral' ? GroupType.Coral : GroupType.Orquestra;
        
        switch(subTab) {
            case 'repertorio': return data.repertorio.filter(item => item.type === groupFilter);
            case 'agenda': return data.agenda.filter(item => item.group === groupFilter);
            case 'recados': return data.recados.filter(item => item.group === groupFilter);
            default: return [];
        }
    }, [data, mainTab, subTab]);


    const renderTable = () => {
        if (loading) return <p className="text-center py-4">Carregando...</p>;
        if (displayedData.length === 0) return <p className="text-center text-gray-500 py-10">Nenhum item encontrado.</p>;

        const currentTab = mainTab === 'usuarios' ? 'usuarios' : subTab;
        const headers: { key: string; label: string; render?: (item: any) => React.ReactNode }[] = {
            repertorio: [
                {key: 'title', label: 'Título'}, 
                {key: 'year', label: 'Ano'}, 
                {key: 'grupos', label: 'Grupos/Naipes', render: item => item.naipes?.join(', ') || item.grupos?.join(', ') || 'N/A'},
                {key: 'active', label: 'Ativo', render: item => item.active ? 'Sim' : 'Não'},
            ],
            agenda: [
                {key: 'title', label: 'Título'}, 
                {key: 'date', label: 'Data', render: item => new Date(item.date + 'T00:00:00').toLocaleDateString('pt-BR')},
                {key: 'active', label: 'Ativo', render: item => item.active ? 'Sim' : 'Não'},
            ],
            recados: [
                {key: 'title', label: 'Título'}, 
                {key: 'date', label: 'Data', render: item => new Date(item.date + 'T00:00:00').toLocaleDateString('pt-BR')},
                {key: 'active', label: 'Ativo', render: item => item.active ? 'Sim' : 'Não'},
            ],
            usuarios: [
                {key: 'username', label: 'Usuário'},
                {key: 'role', label: 'Função'},
                {key: 'active', label: 'Ativo', render: user => user.active ? 'Sim' : 'Não'},
            ],
        }[currentTab];

        return (
             <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                        <tr>
                            {headers.map(h => <th key={h.key} scope="col" className="px-6 py-3">{h.label}</th>)}
                            <th scope="col" className="px-6 py-3 text-right">Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {displayedData.map(item => (
                            <tr key={item.id} className="bg-white border-b hover:bg-gray-50">
                                {headers.map(h => <td key={h.key} className="px-6 py-4">{h.render ? h.render(item) : String((item as any)[h.key] ?? '')}</td>)}
                                <td className="px-6 py-4 text-right space-x-2">
                                    <button onClick={() => handleOpenModal(item)} className="font-medium text-blue-600 hover:underline"><PencilIcon className="w-5 h-5 inline"/></button>
                                    <button onClick={() => handleDelete(item.id)} className="font-medium text-red-600 hover:underline"><TrashIcon className="w-5 h-5 inline"/></button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    const renderForm = () => {
        const currentTab = mainTab === 'usuarios' ? 'usuarios' : subTab;
        const groupType = mainTab === 'coral' ? GroupType.Coral : GroupType.Orquestra;

        const commonFields = (
            <>
              <div className="grid grid-cols-2 gap-4">
                  <div>
                      <label className="block mb-2 text-sm font-medium">Título</label>
                      <input name="title" value={(formData as any).title || ''} onChange={handleFormChange} className="w-full p-2 border rounded" required/>
                  </div>
                   <div>
                       <label className="block mb-2 text-sm font-medium">Data</label>
                       <input type="date" name="date" value={(formData as any).date || ''} onChange={handleFormChange} className="w-full p-2 border rounded" required/>
                   </div>
               </div>
               <div>
                  <label className="block mb-2 text-sm font-medium">Descrição</label>
                  <textarea name="description" value={(formData as any).description || ''} onChange={handleFormChange} className="w-full p-2 border rounded" rows={4}></textarea>
               </div>
               <div className="flex items-center pt-2"><input type="checkbox" id="active" name="active" checked={(formData as any).active ?? true} onChange={handleFormChange} className="w-4 h-4 mr-2" /><label htmlFor="active">Ativo</label></div>
            </>
        );
        
        return (
            <form onSubmit={handleSave} className="space-y-4">
                {currentTab === 'repertorio' && (
                     <>
                        <div className="grid grid-cols-2 gap-4">
                           <div><label className="block mb-2 text-sm font-medium">Título</label><input name="title" value={(formData as RepertorioItem).title || ''} onChange={handleFormChange} className="w-full p-2 border rounded" required/></div>
                           <div><label className="block mb-2 text-sm font-medium">Arranjo</label><input name="arrangement" value={(formData as RepertorioItem).arrangement || ''} onChange={handleFormChange} className="w-full p-2 border rounded" /></div>
                           <div><label className="block mb-2 text-sm font-medium">Ano</label><input type="number" name="year" value={(formData as RepertorioItem).year || ''} onChange={handleFormChange} className="w-full p-2 border rounded" /></div>
                        </div>
                        <div><label className="block mb-2 text-sm font-medium">URL do Áudio</label><input name="audioUrl" value={(formData as RepertorioItem).audioUrl || ''} onChange={handleFormChange} className="w-full p-2 border rounded" placeholder="Opcional"/></div>
                        <div><label className="block mb-2 text-sm font-medium">URL do Vídeo (Youtube)</label><input name="videoUrl" value={(formData as RepertorioItem).videoUrl || ''} onChange={handleFormChange} className="w-full p-2 border rounded" placeholder="Opcional"/></div>
                        <div><label className="block mb-2 text-sm font-medium">URL da Partitura (PDF/IMG)</label><input name="sheetMusicUrl" value={(formData as RepertorioItem).sheetMusicUrl || ''} onChange={handleFormChange} className="w-full p-2 border rounded" required/></div>
                        
                        {groupType === GroupType.Coral ? (
                            <div>
                                 <label className="block mb-2 text-sm font-medium">Naipes</label>
                                 <select name="naipes" multiple value={(formData as RepertorioItem).naipes || []} onChange={handleFormChange} className="w-full p-2 border rounded h-32">
                                    {Object.values(Naipe).map(n => <option key={n} value={n}>{n}</option>)}
                                 </select>
                            </div>
                        ) : (
                            <div>
                                <label className="block mb-2 text-sm font-medium">Grupos da Orquestra</label>
                                <select name="grupos" multiple value={(formData as RepertorioItem).grupos || []} onChange={handleFormChange} className="w-full p-2 border rounded h-32">
                                   {Object.values(OrquestraGrupo).map(g => <option key={g} value={g}>{g}</option>)}
                                </select>
                            </div>
                        )}
                         <div className="flex items-center pt-2"><input type="checkbox" id="active" name="active" checked={(formData as RepertorioItem).active ?? true} onChange={handleFormChange} className="w-4 h-4 mr-2" /><label htmlFor="active">Ativo</label></div>
                    </>
                )}
                {currentTab === 'agenda' && commonFields}
                {currentTab === 'recados' && commonFields}
                {currentTab === 'usuarios' && (
                    <>
                        <div className="grid grid-cols-2 gap-4">
                            <div><label className="block mb-2 text-sm font-medium">Usuário</label><input name="username" value={(formData as User).username || ''} onChange={handleFormChange} className="w-full p-2 border rounded" required/></div>
                            <div>
                                <label className="block mb-2 text-sm font-medium">Função</label>
                                <select name="role" value={(formData as User).role || UserRole.Maestro} onChange={handleFormChange} className="w-full p-2 border rounded">
                                    {Object.values(UserRole).map(r => <option key={r} value={r}>{r}</option>)}
                                </select>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div><label className="block mb-2 text-sm font-medium">Senha</label><input type="password" name="password" onChange={handleFormChange} className="w-full p-2 border rounded" placeholder={editingItem ? "Deixe em branco para não alterar" : "Obrigatório"}/></div>
                            <div><label className="block mb-2 text-sm font-medium">Confirmar Senha</label><input type="password" name="confirmPassword" onChange={handleFormChange} className="w-full p-2 border rounded" placeholder="Confirme a senha"/></div>
                        </div>
                        <div className="flex items-center"><input type="checkbox" id="active" name="active" checked={(formData as User).active ?? true} onChange={handleFormChange} className="w-4 h-4 mr-2" /><label htmlFor="active">Ativo</label></div>
                    </>
                )}
                 <div className="flex justify-end space-x-2 pt-4">
                    <button type="button" onClick={handleCloseModal} className="px-4 py-2 bg-gray-300 rounded">Cancelar</button>
                    <button type="submit" className="px-4 py-2 bg-brand-blue text-white rounded">Salvar</button>
                 </div>
            </form>
        );
    };

    const getTabClass = (tabName: MainTab | SubTab, isMain: boolean) => {
        const active = isMain ? mainTab === tabName : subTab === tabName;
        if(isMain) {
           return `px-4 py-2 font-semibold text-sm sm:text-base rounded-t-lg transition-colors duration-200 ${active ? 'bg-white text-brand-blue border-t border-l border-r border-gray-300' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'}`;
        }
        return `px-4 py-2 text-sm ${active ? 'text-brand-blue font-bold border-b-2 border-brand-blue' : 'text-gray-500 hover:text-brand-blue'}`;
    };

    return (
        <div className="min-h-screen bg-gray-100 p-2 sm:p-8">
            <header className="flex justify-between items-center mb-6 sm:mb-8">
                <h1 className="text-2xl sm:text-3xl font-bold text-brand-dark">Painel de Gestão</h1>
                <button onClick={logout} className="bg-red-500 text-white px-3 py-2 sm:px-4 text-sm sm:text-base rounded-lg hover:bg-red-600 transition">Sair</button>
            </header>
            
            <div className="border-b border-gray-300">
                <nav className="-mb-px flex space-x-2 sm:space-x-4" aria-label="Tabs">
                    <button onClick={() => { setMainTab('coral'); setSubTab('repertorio'); }} className={getTabClass('coral', true)}>Coral</button>
                    <button onClick={() => { setMainTab('orquestra'); setSubTab('repertorio'); }} className={getTabClass('orquestra', true)}>Orquestra</button>
                    <button onClick={() => setMainTab('usuarios')} className={getTabClass('usuarios', true)}>Usuários</button>
                </nav>
            </div>
            
            <div className="bg-white p-4 sm:p-6 rounded-b-lg rounded-r-lg shadow-md">
                {mainTab !== 'usuarios' && (
                    <div className="flex items-center border-b border-gray-200 mb-4">
                        <button onClick={() => setSubTab('repertorio')} className={getTabClass('repertorio', false)}>Repertório</button>
                        <button onClick={() => setSubTab('agenda')} className={getTabClass('agenda', false)}>Agenda</button>
                        <button onClick={() => setSubTab('recados')} className={getTabClass('recados', false)}>Recados</button>
                    </div>
                )}
                
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-xl font-bold capitalize">{mainTab === 'usuarios' ? 'Usuários' : `${subTab} - ${mainTab}`}</h2>
                    <button onClick={() => handleOpenModal()} className="bg-brand-gold text-brand-dark px-4 py-2 rounded-lg hover:bg-yellow-500 transition text-sm font-semibold">Adicionar Novo</button>
                </div>
                {renderTable()}
            </div>

            <Modal isOpen={isModalOpen} onClose={handleCloseModal} title={`${editingItem ? 'Editar' : 'Adicionar'} ${mainTab === 'usuarios' ? 'Usuário' : subTab}`}>
                {isModalOpen && renderForm()}
            </Modal>
        </div>
    );
};

export default AdminDashboard;
