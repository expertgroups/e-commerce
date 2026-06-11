'use client';

import React from 'react';
import { Plus, Trash2, MessageSquare } from 'lucide-react';
import { Chat } from '@/types';

interface Props {
  chats: Chat[];
  activeChatId: string | null;
  onSelectChat: (id: string) => void;
  onDeleteChat: (id: string, e: React.MouseEvent) => void;
  onNewChat: () => void;
}

export default function Sidebar({ chats, activeChatId, onSelectChat, onDeleteChat, onNewChat }: Props) {
  return (
    <aside className="w-64 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 flex flex-col hidden md:flex">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <h1 className="font-bold text-xl">TypingMind Clone</h1>
        <button 
          onClick={onNewChat} 
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          title="گفتگوی جدید"
        >
          <Plus size={20} />
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-2 space-y-2">
        {chats.map(chat => (
          <div
            key={chat.id}
            onClick={() => onSelectChat(chat.id)}
            className={`p-3 rounded-lg cursor-pointer flex justify-between group ${
              activeChatId === chat.id
                ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                : 'hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <div className="flex items-center gap-2 truncate">
              <MessageSquare size={16} className="flex-shrink-0" />
              <span className="truncate text-sm">{chat.title}</span>
            </div>
            <button
              onClick={(e) => onDeleteChat(chat.id, e)}
              className="opacity-0 group-hover:opacity-100 hover:text-red-500 transition-opacity"
            >
              <Trash2 size={14} />
            </button>
          </div>
        ))}
        {chats.length === 0 && (
          <p className="text-center text-gray-500 text-sm p-4">هیچ گفتگویی وجود ندارد</p>
        )}
      </div>
    </aside>
  );
}
