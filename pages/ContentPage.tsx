// pages/ContentPage.tsx
// Versão 18 17/07/2025 17:25
import React, { useState, useEffect, useMemo } from 'react';
import { getRepertorio, getAgenda, getRecados } from '../services/api';
import { GroupType, RepertorioItem, AgendaItem, RecadoItem, Naipe, OrquestraGrupo } from '../types';
import { MusicNoteIcon, CalendarIcon, ChatAltIcon, ChevronDownIcon, PlayIcon, XIcon } from '../components/icons';

type ContentType = 'repertorio' | 'agenda' | 'recados';

const LoadingSpinner: React.FC = () => (
    <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-brand-blue"></div>
    </div>
);

// A função getYouTubeInfo foi removida. O backend agora fornece as URLs prontas.

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
    const
