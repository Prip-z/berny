import { useEffect, useState } from "react"

export function useResizible() {
    const [sidebarWidth, setSidebarWidth] = useState(270)
    const [isResizing, setIsResizing] = useState(false)

    const onMouseDownHandler = () => {
        setIsResizing(true)
    }

    useEffect (() => {
        if (!isResizing) return;

        const onMouseUpHandler = () => {
            setIsResizing(false)
        }

        const onMouseMoveHandler = (e: any) => {
            const minWidth = 200
            const maxWidth = 500
            const leftOffset = 68
            const position = Math.max(minWidth, Math.min(e.clientX - leftOffset, maxWidth))
            setSidebarWidth(position)

        }

        window.addEventListener("mousemove", onMouseMoveHandler)
        window.addEventListener("mouseup", onMouseUpHandler)


        return () => {
            window.removeEventListener("mousemove", onMouseMoveHandler)
            window.removeEventListener("mouseup", onMouseUpHandler)
        }
    }, [isResizing])
    return {sidebarWidth, onMouseDownHandler}
}