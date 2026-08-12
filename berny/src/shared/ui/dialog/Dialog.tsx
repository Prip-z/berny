import { HTMLAttributes, ReactNode, useEffect, useRef, useState } from "react";

interface DialogProps {
    isOpen: boolean
    onClose: () => void
    className?: string
    children: ReactNode
}

export function Dialog({isOpen, onClose, className, children}: DialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)    

  const handleSidebarClick = (e: React.MouseEvent<HTMLDialogElement>) => {
    e.stopPropagation();
    const dialog = dialogRef.current
    if (!dialog) return

    const rect = dialog.getBoundingClientRect();
    const isClickOutside =
      e.clientX < rect.left ||
      e.clientX > rect.right ||
      e.clientY < rect.top ||
      e.clientY > rect.bottom

    if (isClickOutside) {
      onClose()
    }
  }

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return

    if (isOpen) {
      if (!dialog.open) dialog.showModal();
    } else {
      if (dialog.open) dialog.close();
    }
  }, [isOpen])

    return (
    <dialog
        ref={dialogRef}
        onClose={onClose}
        onClick={handleSidebarClick}
        className={className}
        >
        {children}
    </dialog>
    )
}