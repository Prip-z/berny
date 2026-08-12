import { useChannelsStore } from '@/src/entities';
import { HamburgerIcon } from '@/src/shared';
import { Fetch } from '@/src/shared/api/http';
import { Dialog } from '@/src/shared/ui/dialog/Dialog';
import { useState } from 'react';

export function ChatManagment() {
  const setActiveChannelId = useChannelsStore((state) => state.setActiveChannelId)
  const [sidebarIsOpen, setSidebarIsOpen] = useState(false);
  const [createPublicIsOpen, setCreatePublicIsOpen] = useState(false);
  const [nameChannel, setNameChannel] = useState("")

  const openDialogCreatePublic = () => {
    setSidebarIsOpen(false);
    setCreatePublicIsOpen(true);
  }
  //Эт надо вынести в фичи
  const createPublicButtonHandler = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (nameChannel.trim() === "") {
      return
    }
    const response = await Fetch("/channels/", {
      method: "POST",
      body: JSON.stringify({
        name: nameChannel,
        channel_type: "public",
      }),
    })
    const result = await response.json()
    setActiveChannelId(result.channel_id)
  }

  return (
    <div className='flex flex-col w-17 h-screen shrink-0 justify-start items-center'>
      <button
        className="mt-2 p-2 rounded transition duration-100 hover:bg-neutral-800 "
        onClick={() => setSidebarIsOpen(true)}
      >
        <HamburgerIcon />
      </button>

      <Dialog isOpen={sidebarIsOpen} onClose={() => setSidebarIsOpen(false)}         
      className="
          flex flex-col m-0 h-full max-h-none w-80 max-w-full bg-neutral-900 text-white 
          transition-all duration-300 ease-in-out transition-discrete
          backdrop:transition-all backdrop:duration-300 backdrop:ease-in-out backdrop:transition-discrete
          -translate-x-full opacity-0 backdrop:opacity-0
          open:translate-x-0 open:opacity-100 open:backdrop:opacity-100 open:backdrop:bg-black/50
          starting:open:-translate-x-full starting:open:opacity-0 starting:open:backdrop:opacity-0
        ">
        <div className="flex flex-col justify-between items-center mb-4 px-6 py-1.5 gap-5">
          <div className="w-12 h-12 rounded-full bg-blue-500"></div>
          <h2 className="text-xl font-bold">Имя</h2>
        </div>
        <button 
        className='hover:bg-neutral-800 transition p-2 w-full'
        onClick={openDialogCreatePublic}
        >
          Скрафтить канал
        </button>
        <p className="text-neutral-300 p-2 text-center w-full">
          Тут могла быть ваша реклама
        </p>
      </Dialog>
      <Dialog     
      isOpen={createPublicIsOpen} onClose={() => setCreatePublicIsOpen(false)}    
      className='w-100 h-40 bg-input-authorize fixed inset-0 m-auto rounded-2xl'>
          <form className='flex flex-col h-full w-full justify-between p-4 gap-1 ' onSubmit={createPublicButtonHandler}>
            <input 
              className='w-full text-white'
              placeholder="Название группы"
              value={nameChannel}
              onChange={(e) => setNameChannel(e.target.value)}>
            </input>
            <button 
              className='flex p-2 self-end rounded text-blue-600 hover:bg-neutral-600 transition-colors '
            >
              Далее
            </button>
          </form>
      </Dialog>
    </div>
  )
}