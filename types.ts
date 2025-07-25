// types.ts
// Versão 17 17/07/2025 17:22

export enum GroupType {
  Coral = 'Coral',
  Orquestra = 'Orquestra',
  Setor = 'Setor',
}

export enum Naipe {
  Tenor = 'Tenor',
  Baixo = 'Baixo',
  Soprano = 'Soprano',
  Contralto = 'Contralto',
}

export enum OrquestraGrupo {
    Novos = 'Novos',
    Grupo1 = 'Grupo 1',
    Grupo2 = 'Grupo 2',
    Grupo3 = 'Grupo 3',
    Grupo4 = 'Grupo 4',
}

export enum UserRole {
  Admin = 'Admin',
  Maestro = 'Maestro',
}

export interface RepertorioItem {
  id: string;
  type: GroupType.Coral | GroupType.Orquestra;
  title: string;
  arrangement: string;
  year: number;
  audio_url?: string;
  video_url?: string;
  // NOVO CAMPO: Adicionado para corresponder ao que a API agora fornece.
  video_thumbnail_url?: string;
  sheet_music_url: string;
  naipes?: Naipe[];
  grupos?: OrquestraGrupo[];
  active: boolean;
}

export interface AgendaItem {
  id: string;
  group: GroupType;
  date: string;
  title: string;
  description: string;
  active: boolean;
}

export interface RecadoItem {
  id: string;
  group: GroupType;
  date: string;
  title: string;
  description: string;
  active: boolean;
}

export interface User {
  id: string;
  username: string;
  password?: string;
  active: boolean;
  role: UserRole;
}

export interface HistoriaItem {
    id: string;
    year: number;
    title: string;
    description: string;
    imageUrl: string;
}

export interface GaleriaItem {
    id: string;
    type: 'image' | 'video';
    url: string;
    thumbnailUrl: string;
    title: string;
}
