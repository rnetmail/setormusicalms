
import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { MenuIcon, XIcon, MusicNoteIcon, CalendarIcon, ChatAltIcon, BookOpenIcon, PhotographIcon, ChevronDownIcon } from './icons';

const NavItem: React.FC<{ to: string; icon: React.ReactNode; children: React.ReactNode; onClick?: () => void }> = ({ to, icon, children, onClick }) => (
    <NavLink
        to={to}
        onClick={onClick}
        className={({ isActive }) =>
            `flex items-center p-3 text-base font-normal rounded-lg transition duration-75 group ${
            isActive ? 'bg-brand-gold text-brand-dark' : 'text-brand-light hover:bg-brand-blue/60'
            }`
        }
    >
        {icon}
        <span className="ml-3 flex-1 whitespace-nowrap">{children}</span>
    </NavLink>
);

const Accordion: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <li>
            <button
                type="button"
                className="flex items-center w-full p-3 text-base font-normal text-brand-light rounded-lg group hover:bg-brand-blue/60 transition duration-75"
                onClick={() => setIsOpen(!isOpen)}
            >
                <span className="flex-1 ml-3 text-left whitespace-nowrap">{title}</span>
                <ChevronDownIcon className={`w-6 h-6 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
            </button>
            <ul className={`py-2 space-y-2 transition-all duration-300 ease-in-out overflow-hidden ${isOpen ? 'max-h-96' : 'max-h-0'}`}>
                {children}
            </ul>
        </li>
    );
};

const Sidebar: React.FC<{ onClose: () => void }> = ({ onClose }) => {
    const handleItemClick = () => {
        if (window.innerWidth < 768) {
            onClose();
        }
    }
    
    return (
        <aside className="w-64 h-full" aria-label="Sidebar">
            <div className="overflow-y-auto py-4 px-3 h-full bg-brand-blue">
                <Link to="/" className="flex items-center pl-2.5 mb-5" onClick={handleItemClick}>
                    <img src="https://img.icons8.com/plasticine/100/null/musical-notes.png" className="h-8 w-8 mr-3" alt="Logo" />
                    <span className="self-center text-xl font-semibold whitespace-nowrap text-brand-gold">Setor Musical MS</span>
                </Link>
                <ul className="space-y-2">
                    <Accordion title="Coral Mokiti Okada MS">
                       <li><NavItem to="/coral/repertorio" icon={<MusicNoteIcon />} onClick={handleItemClick}>Repertório</NavItem></li>
                       <li><NavItem to="/coral/agenda" icon={<CalendarIcon />} onClick={handleItemClick}>Agenda</NavItem></li>
                       <li><NavItem to="/coral/recados" icon={<ChatAltIcon />} onClick={handleItemClick}>Recados</NavItem></li>
                       <li><NavItem to="/coral/historia" icon={<BookOpenIcon />} onClick={handleItemClick}>História</NavItem></li>
                       <li><NavItem to="/coral/galeria" icon={<PhotographIcon />} onClick={handleItemClick}>Vale a pena ver de novo</NavItem></li>
                    </Accordion>
                    <Accordion title="Orquestra de Violões">
                        <li><NavItem to="/orquestra/repertorio" icon={<MusicNoteIcon />} onClick={handleItemClick}>Repertório</NavItem></li>
                        <li><NavItem to="/orquestra/agenda" icon={<CalendarIcon />} onClick={handleItemClick}>Agenda</NavItem></li>
                        <li><NavItem to="/orquestra/recados" icon={<ChatAltIcon />} onClick={handleItemClick}>Recados</NavItem></li>
                        <li><NavItem to="/orquestra/historia" icon={<BookOpenIcon />} onClick={handleItemClick}>História</NavItem></li>
                        <li><NavItem to="/orquestra/galeria" icon={<PhotographIcon />} onClick={handleItemClick}>Vale a pena ver de novo</NavItem></li>
                    </Accordion>
                     <li>
                        <hr className="my-2 border-brand-blue/60" />
                    </li>
                     <li>
                       <NavItem to="/gestao" icon={<span className="w-6 h-6 flex items-center justify-center">⚙️</span>} onClick={handleItemClick}>
                           Área de Gestão
                       </NavItem>
                    </li>
                </ul>
            </div>
        </aside>
    );
};


const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    return (
        <div className="min-h-screen flex bg-brand-light text-brand-dark">
            {/* Mobile Sidebar */}
            <div className={`fixed inset-0 z-40 flex md:hidden transition-opacity ${sidebarOpen ? 'pointer-events-auto' : 'pointer-events-none'}`}>
                 <div className={`fixed inset-0 bg-gray-600 bg-opacity-75 transition-opacity ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`} onClick={() => setSidebarOpen(false)}></div>
                 <div className={`relative flex-1 flex flex-col max-w-xs w-full bg-brand-blue transition-transform transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                     <div className="absolute top-0 right-0 -mr-12 pt-2">
                        <button onClick={() => setSidebarOpen(false)} className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
                           <span className="sr-only">Close sidebar</span>
                           <XIcon className="h-6 w-6 text-white" />
                        </button>
                    </div>
                     <Sidebar onClose={() => setSidebarOpen(false)} />
                 </div>
            </div>

            {/* Desktop Sidebar */}
            <div className="hidden md:flex md:flex-shrink-0">
                <div className="flex flex-col w-64">
                    <Sidebar onClose={() => {}} />
                </div>
            </div>

            <div className="flex flex-col w-0 flex-1 overflow-hidden">
                <div className="md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3">
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="inline-flex items-center justify-center p-2 rounded-md text-brand-dark hover:bg-brand-gold/50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-brand-gold"
                    >
                        <span className="sr-only">Open sidebar</span>
                        <MenuIcon className="h-6 w-6" />
                    </button>
                </div>
                <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none p-4 md:p-6">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default Layout;