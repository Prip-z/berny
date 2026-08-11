export function formatDateHelper (isoString: string) {
    const messageDate = new Date(isoString);
    if (isNaN(messageDate.getTime())) return ""

    const today = new Date();
    const targetDate = new Date(messageDate)

    targetDate.setHours(0, 0, 0, 0)
    today.setHours(0, 0, 0, 0)

    const diffDays = Math.round((today.getTime() - targetDate.getTime()) / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return "Сегодня"
    if (diffDays === 1) return "Вчера"

    const options: Intl.DateTimeFormatOptions = { day: "numeric", month: "long" }
    if (targetDate.getFullYear() !== today.getFullYear()) {
      options.year = "numeric"
    }

    return targetDate.toLocaleDateString("ru-RU", options)
}

export function getFormattedTime (isoString: string) {
    const date = new Date(isoString)
    if (isNaN(date.getTime())) return isoString
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

export function getTimeOnMessage(created_at: string) {
  const timePattern = /^\d{2}:\d{2}$/;
  if (timePattern.test(created_at)) {
    return created_at
  }
  else {
    const dateInstance = new Date(created_at)
    const timeOnly = dateInstance.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    return timeOnly
  }
}