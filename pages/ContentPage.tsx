// pages/ContentPage.tsx
# Versão 20 17/07/2025 17:30
import React, { useState, useEffect, useMemo } from 'react';
import { getRepertorio, getAgenda, getRecados } from '../services/api';
import { GroupType, RepertorioItem, AgendaItem, RecadoItem, Naipe, OrquestraGrupo } from '../types';
import { MusicNoteIcon, CalendarIcon, ChatAltIcon, ChevronDownIcon, PlayIcon, XIcon } from '../components/icons';

type ContentType = 'repertorio' | 'agenda' | 'recados';

interface ContentPageProps {
    group: GroupType.Coral | GroupType.Orquestra;
    contentType: ContentType;
}

const LoadingSpinner: React.FC = () => (
    <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-brand-blue"></div>
    </div>
);

// A função getYouTubeInfo foi removida, pois esta lógica foi centralizada no backend.

const AgendaCard: React.FC<{ item: AgendaItem }> = ({ item }) => (
    <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-sm font-bold text-brand-gold">{new Date(item.date + 'T00:00:00').toLocaleDateString('pt-BR')}</p>
        <h3 className="text-xl font-bold text-brand-blue mt-1">{item.title}</h3>
        <p className="text-gray-600 mt-2">{item.description}</p>
    </div>
);

const RecadoCard: React.FC<{ item: RecadoItem }> = ({ item }) => (
    <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-sm font-bold text-brand-gold">{new Date(item.date + 'T00:00:00').toLocaleDateString('pt-BR')}</p>
        <h3 className="text-xl font-bold text-brand-blue mt-1">{item.title}</h3>
        <p className="text-gray-600 mt-2">{item.description}</p>
    </div>
);

const ContentPage: React.FC<ContentPageProps> = ({ group, contentType }) => {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState({ year: '', month: '' });
    const [openState, setOpenState] = useState<Record<string, boolean>>({});
    const [modalVideoUrl, setModalVideoUrl] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                let result;
                if (contentType === 'repertorio') {
                    result = await getRepertorio(group);
                } else if (contentType === 'agenda') {
                    result = await getAgenda(group);
                } else {
                    result = await getRecados(group);
                }
                setData(result);
            } catch (error) {
                console.error("Failed to fetch data", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [group, contentType]);
    
    const toggleAccordion = (id: string) => {
        setOpenState(prev => ({...prev, [id]: !prev[id]}));
    };

    const filteredData = useMemo(() => {
        if (contentType !== 'agenda') return data;
        return data.filter(item => {
            const date = new Date(item.date + 'T00:00:00');
            const yearMatch = filter.year ? date.getFullYear().toString() === filter.year : true;
            const monthMatch = filter.month ? (date.getMonth() + 1).toString() === filter.month : true;
            return yearMatch && monthMatch;
        });
    }, [data, filter, contentType]);

    const pageConfig = {
        repertorio: { title: 'Repertório', icon: <MusicNoteIcon className="w-8 h-8" /> },
        agenda: { title: 'Agenda', icon: <CalendarIcon className="w-8 h-8" /> },
        recados: { title: 'Recados', icon: <ChatAltIcon className="w-8 h-8" /> },
    };
    
    const { title, icon } = pageConfig[contentType];
    const groupName = group === GroupType.Coral ? 'Coral' : 'Orquestra';
    
    const AccordionItem: React.FC<{
        id: string;
        title: React.ReactNode;
        children: React.ReactNode;
        containerClass?: string;
        headerClass?: string;
        contentClass?: string;
    }> = ({ id, title, children, containerClass, headerClass, contentClass }) => {
        const isOpen = !!openState[id];
        return (
            <div className={`overflow-hidden ${containerClass}`}>
                <button
                    onClick={() => toggleAccordion(id)}
                    className={`w-full flex justify-between items-center p-4 text-left transition ${headerClass}`}
                >
                    <div className="font-semibold text-brand-dark">{title}</div>
                    <ChevronDownIcon className={`w-6 h-6 transform transition-transform text-brand-blue ${isOpen ? 'rotate-180' : ''}`} />
                </button>
                {isOpen && <div className={contentClass}>{children}</div>}
            </div>
        );
    };

    const renderRepertorio = () => {
        const renderMusicDetails = (item: RepertorioItem) => {
            // Lógica simplificada: usa diretamente as URLs fornecidas pelo backend.
            const isPdf = item.sheet_music_url && item.sheet_music_url.toLowerCase().includes('preview');
            return (
                 <div className="space-y-4">
                    {item.audio_url && (
                        <div>
                            <h4 className="font-bold mb-2 text-gray-700">Áudio para Estudo:</h4>
                            <audio controls className="w-full"><source src={item.audio_url} type="audio/mpeg" /></audio>
                        </div>
                    )}
                    {item.video_url && item.video_thumbnail_url && (
                        <div>
                            <h4 className="font-bold mb-2 text-gray-700">Vídeo de Referência:</h4>
                            <div className="relative cursor-pointer group w-full md:w-80" onClick={() => setModalVideoUrl(item.video_url!)}>
                                <img src={item.video_thumbnail_url} alt={`Thumbnail for ${item.title}`} className="rounded-lg shadow-md w-full" />
                                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 rounded-lg flex items-center justify-center transition-all duration-300">
                                    <PlayIcon className="w-16 h-16 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                                </div>
                            </div>
                        </div>
                    )}
                    {item.sheet_music_url && (
                        <div>
                            <h4 className="font-bold mb-2 text-gray-700">Partitura:</h4>
                            {isPdf ? (
                                <a href={item.sheet_music_url} target="_blank" rel="noopener noreferrer" className="inline-block bg-brand-gold text-brand-dark font-bold py-2 px-4 rounded-full hover:bg-yellow-500 transition-colors duration-300">
                                    Abrir Partitura (PDF)
                                </a>
                            ) : (
                                <img src={item.sheet_music_url} alt={`Partitura de ${item.title}`} className="w-full h-auto rounded border" />
                            )}
                        </div>
                    )}
                </div>
            );
        };

        if (group === GroupType.Coral) {
            const naipesOrdenados = [Naipe.Soprano, Naipe.Contralto, Naipe.Tenor, Naipe.Baixo];
            const groupedByNaipe: { [key in Naipe]?: RepertorioItem[] } = (data as RepertorioItem[]).reduce((acc, item) => {
                item.naipes?.forEach(naipe => {
                    if (!acc[naipe]) acc[naipe] = [];
                    acc[naipe]!.push(item);
                });
                return acc;
            }, {} as { [key in Naipe]?: RepertorioItem[] });

            return (
                 <div className="space-y-4">
                    {naipesOrdenados
                        .filter(naipe => groupedByNaipe[naipe]?.length)
                        .map(naipe => (
                            <AccordionItem
                                key={`group-${naipe}`}
                                id={`group-${naipe}`}
                                title={<span className="text-xl font-bold text-brand-blue">{naipe}</span>}
                                containerClass="border border-brand-blue/20 rounded-lg shadow-lg"
                                headerClass="bg-brand-blue/5 hover:bg-brand-blue/10"
                                contentClass="p-2 bg-white border-t border-brand-blue/20"
                            >
                                <div className="space-y-2">
                                    {groupedByNaipe[naipe]!.map(item => (
                                        <AccordionItem
                                            key={`music-${item.id}`}
                                            id={`music-${item.id}`}
                                            title={
                                                <div>
                                                    <p className="text-lg font-bold text-brand-dark">{item.title}</p>
                                                    <p className="text-sm text-gray-500">{item.arrangement} - {item.year}</p>
                                                </div>
                                            }
                                            containerClass="bg-white rounded-lg border border-gray-200"
                                            headerClass="hover:bg-gray-50"
                                            contentClass="p-4 border-t border-gray-200"
                                        >
                                            {renderMusicDetails(item)}
                                        </AccordionItem>
                                    ))}
                                </div>
                            </AccordionItem>
                        ))}
                </div>
            );
        }

        if (group === GroupType.Orquestra) {
            const gruposOrdenados = Object.values(OrquestraGrupo);
            const groupedByGrupo: { [key in OrquestraGrupo]?: RepertorioItem[] } = (data as RepertorioItem[]).reduce((acc, item) => {
                item.grupos?.forEach(grupo => {
                    if (!acc[grupo]) acc[grupo] = [];
                    acc[grupo]!.push(item);
                });
                return acc;
            }, {} as { [key in OrquestraGrupo]?: RepertorioItem[] });
            
            return (
                <div className="space-y-4">
                    {gruposOrdenados
                        .filter(grupo => groupedByGrupo[grupo]?.length)
                        .map(grupo => (
                            <AccordionItem
                                key={`group-${grupo}`}
                                id={`group-${grupo}`}
                                title={<span className="text-xl font-bold text-brand-blue">{grupo}</span>}
                                containerClass="border border-brand-blue/20 rounded-lg shadow-lg"
                                headerClass="bg-brand-blue/5 hover:bg-brand-blue/10"
                                contentClass="p-2 bg-white border-t border-brand-blue/20"
                            >
                                <div className="space-y-2">
                                    {groupedByGrupo[grupo]!.map(item => (
                                        <AccordionItem
                                            key={`music-${item.id}`}
                                            id={`music-${item.id}`}
                                            title={
                                                <div>
                                                    <p className="text-lg font-bold text-brand-dark">{item.title}</p>
                                                    <p className="text-sm text-gray-500">{item.arrangement} - {item.year}</p>
                                                </div>
                                            }
                                            containerClass="bg-white rounded-lg border border-gray-200"
                                            headerClass="hover:bg-gray-50"
                                            contentClass="p-4 border-t border-gray-200"
                                        >
                                            {renderMusicDetails(item)}
                                        </AccordionItem>
                                    ))}
                                </div>
                            </AccordionItem>
                        ))}
                </div>
            );
        }
        return null;
    };

    const renderContent = () => {
        if (loading) return <LoadingSpinner />;
        const sourceData = contentType === 'agenda' ? filteredData : data;
        if (sourceData.length === 0) return <p className="text-center text-gray-500 py-10">Nenhum item encontrado.</p>;
        if (contentType === 'repertorio') return renderRepertorio();
        return (
            <div className="space-y-6">
                {sourceData.map(item => {
                    if (contentType === 'agenda') return <AgendaCard key={item.id} item={item as AgendaItem} />;
                    if (contentType === 'recados') return <RecadoCard key={item.id} item={item as RecadoItem} />;
                    return null;
                })}
            </div>
        );
    }
    
    const VideoModal = () => (
        <div className="fixed inset-0 bg-black bg-opacity-80 z-50 flex items-center justify-center p-4" onClick={() => setModalVideoUrl(null)}>
            <button className="absolute top-4 right-4 text-white text-4xl z-50" onClick={() => setModalVideoUrl(null)}>
                <XIcon className="w-8 h-8"/>
            </button>
            <div className="relative w-full max-w-4xl" onClick={e => e.stopPropagation()}>
                <div style={{paddingTop: '56.25%', position: 'relative'}}>
                     <iframe
                        src={modalVideoUrl!}
                        title="Video Player"
                        frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                        className="absolute top-0 left-0 w-full h-full rounded-lg shadow-2xl"
                    ></iframe>
                </div>
            </div>
        </div>
    );

    return (
        <div className="container mx-auto">
            <header className="mb-8 p-6 bg-brand-blue rounded-lg text-white shadow-lg">
                <div className="flex items-center space-x-4">
                    <div className="text-brand-gold">{icon}</div>
                    <div>
                        <h1 className="text-4xl font-bold">{title}</h1>
                        <p className="text-xl text-gray-300">{groupName} Mokiti Okada MS</p>
                    </div>
                </div>
            </header>

            {contentType === 'agenda' && (
                <div className="mb-6 bg-white p-4 rounded-lg shadow-md flex flex-wrap items-center gap-4">
                    <span className="font-semibold">Filtrar por:</span>
                    <select value={filter.year} onChange={e => setFilter({...filter, year: e.target.value})} className="p-2 border rounded">
                        <option value="">Todo Ano</option>
                        {[2025, 2024, 2023].map(y => <option key={y} value={y}>{y}</option>)}
                    </select>
                    <select value={filter.month} onChange={e => setFilter({...filter, month: e.target.value})} className="p-2 border rounded">
                        <option value="">Todo Mês</option>
                        {Array.from({length: 12}, (_, i) => <option key={i+1} value={i+1}>{new Date(0, i).toLocaleString('pt-BR', { month: 'long' })}</option>)}
                    </select>
                </div>
            )}

            {renderContent()}

            {modalVideoUrl && <VideoModal />}
        </div>
    );
};

export default ContentPage;
