
import React from 'react';
import { Link } from 'react-router-dom';
import { MusicNoteIcon, CalendarIcon, BookOpenIcon } from '../components/icons';

const FeatureCard: React.FC<{ icon: React.ReactNode, title: string, description: string, linkTo: string, linkText: string }> = ({ icon, title, description, linkTo, linkText }) => (
    <div className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col items-center text-center">
        <div className="text-brand-gold bg-brand-blue rounded-full p-4 mb-4">
            {icon}
        </div>
        <h3 className="text-xl font-bold text-brand-blue mb-2">{title}</h3>
        <p className="text-gray-600 mb-4 flex-grow">{description}</p>
        <Link to={linkTo} className="mt-auto bg-brand-gold text-brand-dark font-bold py-2 px-4 rounded-full hover:bg-yellow-500 transition-colors duration-300">
            {linkText}
        </Link>
    </div>
);

const HomePage: React.FC = () => {
    return (
        <div className="container mx-auto px-4 py-8">
            <div className="text-center bg-white p-10 rounded-xl shadow-lg mb-12" style={{ backgroundImage: `url('https://picsum.photos/1200/400?blur=5&grayscale')`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
                <div className="bg-black/50 p-8 rounded-lg">
                    <h1 className="text-5xl font-extrabold text-white mb-2">Setor Musical Mokiti Okada MS</h1>
                    <p className="text-xl text-brand-gold">Harmonia, Arte e Dedicação</p>
                </div>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-md mb-12">
                <h2 className="text-3xl font-bold text-brand-blue mb-4 text-center">Bem-vindo ao nosso Portal</h2>
                <p className="text-lg text-gray-700 leading-relaxed text-center max-w-3xl mx-auto">
                    Este é o espaço dedicado aos membros e amigos do Coral e da Orquestra de Violões Mokiti Okada de Mato Grosso do Sul. Aqui você encontrará tudo o que precisa para seus estudos e para se manter informado sobre nossas atividades: repertórios, agendas, recados importantes, e um pouco da nossa trajetória. Navegue e sinta-se em casa!
                </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <FeatureCard 
                    icon={<MusicNoteIcon className="w-8 h-8"/>}
                    title="Repertório do Coral"
                    description="Acesse partituras, áudios e vídeos de referência para estudo do nosso repertório coral."
                    linkTo="/coral/repertorio"
                    linkText="Ver Repertório"
                />
                <FeatureCard 
                    icon={<MusicNoteIcon className="w-8 h-8"/>}
                    title="Repertório da Orquestra"
                    description="Material de estudo completo para os violonistas da nossa orquestra."
                    linkTo="/orquestra/repertorio"
                    linkText="Ver Repertório"
                />
                 <FeatureCard 
                    icon={<CalendarIcon className="w-8 h-8"/>}
                    title="Nossa Agenda"
                    description="Fique por dentro de todos os nossos ensaios, apresentações e eventos."
                    linkTo="/coral/agenda"
                    linkText="Ver Agenda"
                />
                 <FeatureCard 
                    icon={<BookOpenIcon className="w-8 h-8"/>}
                    title="Nossa História"
                    description="Conheça os marcos e momentos que construíram a nossa trajetória musical."
                    linkTo="/coral/historia"
                    linkText="Ler História"
                />
                 <FeatureCard 
                    icon={<span className="w-8 h-8 flex items-center justify-center text-2xl">🎶</span>}
                    title="Coral Mokiti Okada"
                    description="Explore a página dedicada ao nosso coral, com sua história e galeria de momentos."
                    linkTo="/coral/historia"
                    linkText="Saber Mais"
                />
                 <FeatureCard 
                    icon={<span className="w-8 h-8 flex items-center justify-center text-2xl">🎸</span>}
                    title="Orquestra de Violões"
                    description="Descubra o universo da nossa orquestra de violões, suas músicas e memórias."
                    linkTo="/orquestra/historia"
                    linkText="Saber Mais"
                />
            </div>
        </div>
    );
};

export default HomePage;
