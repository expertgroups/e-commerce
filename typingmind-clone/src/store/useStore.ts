import { create } from 'zustand';
import { Chat, Message, Settings } from '@/types';
import { saveChat, getAllChats, deleteChat as deleteChatDb } from '@/lib/db/chat-db';

interface AppState {
  chats: Chat[];
  activeChatId: string | null;
  settings: Settings;
  isLoading: boolean;
  
  // Actions
  loadChats: () => Promise<void>;
  createChat: (model?: string, provider?: string) => Promise<Chat>;
  deleteChat: (id: string) => Promise<void>;
  setActiveChat: (id: string | null) => void;
  addMessage: (chatId: string, message: Message) => Promise<void>;
  startAssistantStream: (chatId: string, messageId: string) => void;
  updateAssistantStream: (chatId: string, messageId: string, content: string) => void;
  finalizeAssistantStream: (chatId: string, messageId: string, finalContent: string) => Promise<void>;
  updateSettings: (settings: Partial<Settings>) => void;
}

const defaultSettings: Settings = {
  apiKeys: {
    openai: '',
    anthropic: '',
    google: '',
    azure: '',
    ollamaUrl: 'http://localhost:11434',
  },
  theme: 'system',
};

export const useStore = create<AppState>((set, get) => ({
  chats: [],
  activeChatId: null,
  settings: defaultSettings,
  isLoading: true,

  loadChats: async () => {
    try {
      const chats = await getAllChats();
      set({ chats: chats.reverse(), isLoading: false });
    } catch (error) {
      console.error('Failed to load chats:', error);
      set({ isLoading: false });
    }
  },

  createChat: async (model = 'gpt-4o', provider = 'openai') => {
    const chat: Chat = {
      id: crypto.randomUUID(),
      title: 'گفتگوی جدید',
      messages: [],
      model,
      provider,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    
    await saveChat(chat);
    set((state) => ({ 
      chats: [chat, ...state.chats],
      activeChatId: chat.id 
    }));
    return chat;
  },

  deleteChat: async (id: string) => {
    await deleteChatDb(id);
    set((state) => ({ 
      chats: state.chats.filter(c => c.id !== id),
      activeChatId: state.activeChatId === id ? null : state.activeChatId 
    }));
  },

  setActiveChat: (id: string | null) => {
    set({ activeChatId: id });
  },

  addMessage: async (chatId: string, message: Message) => {
    const state = get();
    const chat = state.chats.find(c => c.id === chatId);
    if (!chat) return;

    const updatedMessages = [...chat.messages, message];
    let newTitle = chat.title;
    if (chat.messages.length === 0 && message.role === 'user') {
      newTitle = message.content.slice(0, 30) + (message.content.length > 30 ? '...' : '');
    }

    const updatedChat = {
      ...chat,
      title: newTitle,
      messages: updatedMessages,
      updatedAt: Date.now(),
    };

    await saveChat(updatedChat);
    set((state) => ({
      chats: state.chats.map(c => c.id === chatId ? updatedChat : c),
    }));
  },

  startAssistantStream: (chatId: string, messageId: string) => {
    set((state) => ({
      chats: state.chats.map(chat =>
        chat.id === chatId
          ? {
              ...chat,
              messages: chat.messages.map(msg =>
                msg.id === messageId ? { ...msg, isStreaming: true, temporaryContent: '' } : msg
              ),
            }
          : chat
      ),
    }));
  },

  updateAssistantStream: (chatId: string, messageId: string, content: string) => {
    set((state) => ({
      chats: state.chats.map(chat =>
        chat.id === chatId
          ? {
              ...chat,
              messages: chat.messages.map(msg =>
                msg.id === messageId && msg.isStreaming
                  ? { ...msg, temporaryContent: content }
                  : msg
              ),
            }
          : chat
      ),
    }));
  },

  finalizeAssistantStream: async (chatId: string, messageId: string, finalContent: string) => {
    const state = get();
    const chat = state.chats.find(c => c.id === chatId);
    if (!chat) return;

    const updatedMessages = chat.messages.map(msg =>
      msg.id === messageId
        ? { ...msg, content: finalContent, temporaryContent: undefined, isStreaming: false }
        : msg
    );

    const updatedChat = {
      ...chat,
      messages: updatedMessages,
      updatedAt: Date.now(),
    };

    await saveChat(updatedChat);
    set((state) => ({
      chats: state.chats.map(c => c.id === chatId ? updatedChat : c),
    }));
  },

  updateSettings: (settings: Partial<Settings>) => {
    set((state) => ({
      settings: { ...state.settings, ...settings },
    }));
  },
}));
