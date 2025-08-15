import { useState, useEffect, createContext, useContext } from 'react';

// Create modal context
const ModalContext = createContext({
  openModal: () => {},
  closeModal: () => {},
});

export const useModal = () => useContext(ModalContext);

// Modal container component
const ModalContainer = () => {
  const [modalStack, setModalStack] = useState([]);
  const [isClosing, setIsClosing] = useState(false);
  
  // Handle ESC key to close the top modal
  useEffect(() => {
    const handleEscapeKey = (e) => {
      if (e.key === 'Escape' && modalStack.length > 0) {
        closeModal();
      }
    };
    
    document.addEventListener('keydown', handleEscapeKey);
    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [modalStack]);
  
  // Prevent scrolling on the body when modals are open
  useEffect(() => {
    if (modalStack.length > 0) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    
    return () => {
      document.body.style.overflow = '';
    };
  }, [modalStack]);
  
  const openModal = (component, props = {}) => {
    const id = Date.now().toString();
    setModalStack(prev => [...prev, { id, component, props }]);
    return id;
  };
  
  const closeModal = (id) => {
    setIsClosing(true);
    
    // If no id provided, close the top modal
    if (!id) {
      setTimeout(() => {
        setModalStack(prev => prev.slice(0, -1));
        setIsClosing(false);
      }, 200); // Match the CSS transition time
    } else {
      setTimeout(() => {
        setModalStack(prev => prev.filter(modal => modal.id !== id));
        setIsClosing(false);
      }, 200); // Match the CSS transition time
    }
  };
  
  if (modalStack.length === 0) {
    return null;
  }
  
  // Get the current top modal
  const currentModal = modalStack[modalStack.length - 1];
  const ModalComponent = currentModal.component;

  return (
    <ModalContext.Provider value={{ openModal, closeModal }}>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-50 transition-opacity duration-200"
        style={{ opacity: isClosing ? 0 : 1 }}
        onClick={() => closeModal()}
      ></div>
      
      {/* Modal container */}
      <div 
        className="fixed inset-0 z-50 flex items-center justify-center p-4"
        style={{ pointerEvents: 'none' }}
      >
        <div 
          className={`bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-auto transition-all duration-200 ${
            isClosing ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
          }`}
          style={{ pointerEvents: 'auto' }}
          onClick={(e) => e.stopPropagation()}
        >
          <ModalComponent closeModal={() => closeModal()} {...currentModal.props} />
        </div>
      </div>
    </ModalContext.Provider>
  );
};

export default ModalContainer;

// Example usage:
// Create a modal component
// const SampleModal = ({ closeModal, title }) => {
//   return (
//     <div className="p-6">
//       <div className="flex justify-between items-center mb-4">
//         <h3 className="text-lg font-medium">{title}</h3>
//         <button onClick={closeModal} className="text-gray-500 hover:text-gray-700">
//           <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
//           </svg>
//         </button>
//       </div>
//       <div className="mb-4">Modal content goes here...</div>
//       <div className="flex justify-end">
//         <button 
//           onClick={closeModal}
//           className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
//         >
//           Close
//         </button>
//       </div>
//     </div>
//   );
// };
//
// In your component:
// import { useModal } from '../components/ui/ModalContainer';
//
// function MyComponent() {
//   const { openModal } = useModal();
//
//   const handleOpenModal = () => {
//     openModal(SampleModal, { title: "Example Modal" });
//   };
//
//   return (
//     <button onClick={handleOpenModal}>Open Modal</button>
//   );
// }