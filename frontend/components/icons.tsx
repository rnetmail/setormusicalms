import React from 'react';

export const Icon: React.FC<{ d: string; className?: string }> = ({ d, className }) => (
    <svg className={className || "w-6 h-6"} fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
        <path fillRule="evenodd" d={d} clipRule="evenodd"></path>
    </svg>
);

export const MenuIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />;
export const XIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" />;
export const MusicNoteIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 1.343-3 3s1.343 3 3 3 3-1.343 3-3V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 1.343-3 3s1.343 3 3 3 3-1.343 3-3V3z" />;
export const CalendarIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" />;
export const ChatAltIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M10 2a8 8 0 100 16 8 8 0 000-16zM2 10a8 8 0 018-8 8 8 0 018 8v1.282A7.971 7.971 0 0010 12a7.972 7.972 0 00-8 1.282V10zM10 14a6 6 0 01-6-6h12a6 6 0 01-6 6z" />;
export const BookOpenIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M10 2a.75.75 0 01.75.75v.5a.75.75 0 01-1.5 0v-.5A.75.75 0 0110 2zM8 4.75A.75.75 0 018.75 4h2.5a.75.75 0 010 1.5h-2.5A.75.75 0 018 4.75zM8.75 6a.75.75 0 000 1.5h2.5a.75.75 0 000-1.5h-2.5zM3 6a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V6zm2-1a1 1 0 00-1 1v10a1 1 0 001 1h10a1 1 0 001-1V6a1 1 0 00-1-1H5z"/>;
export const PhotographIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828zM4 5a1 1 0 011-1h6a1 1 0 110 2H5a1 1 0 01-1-1zm-1 5a1 1 0 000 2h3a1 1 0 100-2H3zm12.293-3.293a1 1 0 011.414 0l1 1a1 1 0 010 1.414l-9 9a1 1 0 01-.39.242l-3 1a1 1 0 01-1.242-1.242l1-3A1 1 0 014.707 15H15a1 1 0 001-1v-2.293l-2.707-2.707z"/>;
export const ChevronDownIcon: React.FC<{className?: string}> = ({className}) => <Icon className={className} d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />;
export const TrashIcon: React.FC<{ className?: string }> = ({ className }) => <Icon className={className} d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm4 0a1 1 0 012 0v6a1 1 0 11-2 0V8z" />;
export const PencilIcon: React.FC<{ className?: string }> = ({ className }) => <Icon className={className} d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828zM5 12V7.172l5-5L14.828 7 10 11.828V12H5zM15 5l-1.586-1.586L12 5l1.586 1.586L15 5zM3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />;
export const PlayIcon: React.FC<{ className?: string }> = ({ className }) => (
    <svg className={className || "w-6 h-6"} fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 5v14l11-7z"></path>
    </svg>
);