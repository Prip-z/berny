import { useEffect, useRef, useState } from 'react';

export function ChatManagment() {
  const [isOpen, setIsOpen] = useState(false);
  const dialogRef = useRef<HTMLDialogElement>(null);

useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      if (!dialog.open) dialog.showModal();
    } else {
      if (dialog.open) dialog.close();
    }
  }, [isOpen]);

  const handleDialogClick = (e: React.MouseEvent<HTMLDialogElement>) => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    const rect = dialog.getBoundingClientRect();
    const isClickOutside =
      e.clientX < rect.left ||
      e.clientX > rect.right ||
      e.clientY < rect.top ||
      e.clientY > rect.bottom;

    if (isClickOutside) {
      setIsOpen(false);
    }
  };

  return (
    <div className='flex flex-col w-17 h-screen shrink-0 justify-start items-center'>
      <button 
        className="mt-2 p-2 rounded hover:bg-neutral-800 transition-colors"         
        onClick={() => setIsOpen(true)}
        >
            <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="w-6 h-6 stroke-current" 
                viewBox="0 0 24 24" 
                fill="none" 
                strokeWidth="2" 
                strokeLinecap="round"
            >
                <path d="M4 6h16M4 12h16M4 18h16" />
            </svg>
        </button>

      <dialog
        ref={dialogRef}
        onClose={() => setIsOpen(false)}
        onClick={handleDialogClick}
        className="
          m-0 h-full max-h-none w-80 max-w-full bg-neutral-900 text-white p-6
          backdrop:bg-black/50 backdrop:backdrop-blur-sm
          backdrop:transition-all backdrop:duration-300
          transition-all duration-150 ease-in-out
          transition-discrete
          -translate-x-full opacity-0
          open:translate-x-0 open:opacity-100
          starting:open:-translate-x-full starting:open:opacity-0
          starting:open:backdrop:opacity-0
        "
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Имя</h2>

        </div>
        
        <p className="text-neutral-300">
          Тут могла быть ваша реклама
        </p>
      </dialog>
    </div>
  )
}