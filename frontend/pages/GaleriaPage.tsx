
import React, { useState, useEffect } from 'react';
import { getGaleria } from '../services/api';
import { GroupType, GaleriaItem } from '../types';
import { PhotographIcon, XIcon } from '../components/icons';

const LoadingSpinner: React.FC = () => (
    <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-brand-blue"></div>
    </div>
);

const Lightbox: React.FC<{ item: GaleriaItem; onClose: () => void }> = ({ item, onClose }) => {
    return (
        <div className="fixed inset-0 bg-black bg-opacity-80 z-50 flex items-center justify-center" onClick={onClose}>
            <button className="absolute top-4 right-4 text-white text-3xl" onClick={onClose}>
                <XIcon className="w-8 h-8" />
            </button>
            <div className="relative w-full max-w-4xl max-h-[90vh] p-4" onClick={(e) => e.stopPropagation()}>
                {item.type === 'image' ? (
                    <img src={item.url} alt={item.title} className="max-w-full max-h-full mx-auto rounded-lg" />
                ) : (
                    <div className="aspect-w-16 aspect-h-9">
                        <iframe
                            src={item.url}
                            title={item.title}
                            frameBorder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            className="w-full h-full rounded"
                        ></iframe>
                    </div>
                )}
                 <p className="text-white text-center mt-4 text-lg">{item.title}</p>
            </div>
        </div>
    );
};


const GaleriaPage: React.FC<{ group: GroupType }> = ({ group }) => {
    const [items, setItems] = useState<GaleriaItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedItem, setSelectedItem] = useState<GaleriaItem | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const result = await getGaleria(group);
                setItems(result);
            } catch (error) {
                console.error("Failed to fetch gallery", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [group]);

    const groupName = group === GroupType.Coral ? 'Coral' : 'Orquestra';

    return (
        <div className="container mx-auto">
            <header className="mb-8 p-6 bg-brand-blue rounded-lg text-white shadow-lg">
                <div className="flex items-center space-x-4">
                    <div className="text-brand-gold"><PhotographIcon className="w-8 h-8" /></div>
                    <div>
                        <h1 className="text-4xl font-bold">Vale a pena ver de novo</h1>
                        <p className="text-xl text-gray-300">Galeria de Memórias - {groupName}</p>
                    </div>
                </div>
            </header>
            
            {loading ? <LoadingSpinner /> : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {items.map(item => (
                        <div key={item.id} className="group relative cursor-pointer" onClick={() => setSelectedItem(item)}>
                            <img src={item.thumbnailUrl} alt={item.title} className="w-full h-full object-cover rounded-lg shadow-md" />
                            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-300 flex items-center justify-center">
                                {item.type === 'video' && <div className="text-white text-5xl opacity-0 group-hover:opacity-100 transition-opacity">▶</div>}
                            </div>
                            <div className="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/70 to-transparent text-white rounded-b-lg">
                                <p className="text-sm font-semibold truncate">{item.title}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {selectedItem && <Lightbox item={selectedItem} onClose={() => setSelectedItem(null)} />}
        </div>
    );
};

export default GaleriaPage;
