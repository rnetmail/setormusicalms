
import React, { useState, useEffect } from 'react';
import { getHistoria } from '../services/api';
import { GroupType, HistoriaItem } from '../types';
import { BookOpenIcon } from '../components/icons';

const LoadingSpinner: React.FC = () => (
    <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-brand-blue"></div>
    </div>
);

const TimelineItem: React.FC<{ item: HistoriaItem, index: number }> = ({ item, index }) => {
    const isEven = index % 2 === 0;

    return (
        <div className="relative">
            {/* Dot */}
            <div className={`absolute w-4 h-4 bg-brand-gold rounded-full mt-1.5 -left-[7px] border-4 border-brand-light z-10`}></div>
            {/* Card */}
            <div className="ml-8 p-6 bg-white rounded-lg shadow-md">
                <time className="mb-1 text-lg font-semibold text-brand-blue">{item.year}</time>
                <h3 className="text-xl font-bold text-gray-900">{item.title}</h3>
                <img src={item.imageUrl} alt={item.title} className="my-4 rounded-lg shadow-sm" />
                <p className="text-base font-normal text-gray-600">{item.description}</p>
            </div>
        </div>
    );
};

const HistoriaPage: React.FC<{ group: GroupType }> = ({ group }) => {
    const [history, setHistory] = useState<HistoriaItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const result = await getHistoria();
                setHistory(result.sort((a,b) => a.year - b.year));
            } catch (error) {
                console.error("Failed to fetch history", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const groupName = group === GroupType.Coral ? 'Coral' : 'Orquestra';

    return (
        <div className="container mx-auto">
            <header className="mb-8 p-6 bg-brand-blue rounded-lg text-white shadow-lg">
                <div className="flex items-center space-x-4">
                    <div className="text-brand-gold"><BookOpenIcon className="w-8 h-8" /></div>
                    <div>
                        <h1 className="text-4xl font-bold">Nossa História</h1>
                        <p className="text-xl text-gray-300">{groupName} Mokiti Okada MS</p>
                    </div>
                </div>
            </header>
            
            {loading ? <LoadingSpinner /> : (
                <div className="relative border-l-2 border-brand-gold ml-2">                  
                    <div className="space-y-12">
                         {history.map((item, index) => (
                            <TimelineItem key={item.id} item={item} index={index} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default HistoriaPage;
