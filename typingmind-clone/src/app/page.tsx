'use client';

import React, { useEffect, useRef, useState } from 'react';
import { useStore } from '@/store/useStore';
import { Message, Chat } from '@/types';
import { streamResponse } from '@/lib/ai/ai-service';
import Sidebar from '@/components/sidebar/Sidebar';
import MessageList from '@/components/chat/MessageList';
import ChatInput, { ChatInputHandles } from '@/components/chat/ChatInput';
import SettingsModal from '@/components/settings/SettingsModal';
import PromptLibrary from '@/components/prompt-library/PromptLibrary';
import { Plus, Settings, BookOpen, Moon, Sun, Monitor, Trash2 } from 'lucide-react';

export default function Home() {
  const { 
    chats, 
    activeChatId, 
    settings, 
    isLoading,
    loadChats, 
    createChat, 
    deleteChat, 
    setActiveChat, 
    addMessage,
    startAssistantStream,
    updateAssistantStream,
    finalizeAssistantStream,
    updateSettings 
  } = useStore();

  const [isStreaming, setIsStreaming] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showPromptLibrary, setShowPromptLibrary] = useState(false);
  const chatInputRef = useRef<ChatInputHandles>(null);

  const activeChat = chats.find(c => c.id === activeChatId) || null;

  useEffect(() => {
    loadChats();
  }, []);

  useEffect(() => {
    // Apply theme
    const root = document.documentElement;
    if (settings.theme === 'dark') {
      root.classList.add('dark');
    } else if (settings.theme === 'light') {
      root.classList.remove('dark');
    } else {
      // System preference
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }
    }
  }, [settings.theme]);

  const handleNewChat = async () => {
    await createChat('gpt-4o', 'openai');
  };

  const handleSelectChat = (id: string) => {
    setActiveChat(id);
    setShowPromptLibrary(false);
  };

  const handleDeleteChat = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    await deleteChat(id);
    if (activeChatId === id) {
      setActiveChat(null);
    }
  };

  const handleSend = async (text: string) => {
    if (!activeChat || isStreaming) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      createdAt: Date.now(),
    };

    await addMessage(activeChat.id, userMsg);

    const assistantMsgId = crypto.randomUUID();
    const initialAssistantMsg: Message = {
      id: assistantMsgId,
      role: 'assistant',
      content: '',
      temporaryContent: '',
      isStreaming: true,
      createdAt: Date.now(),
      model: activeChat.model,
    };

    await addMessage(activeChat.id, initialAssistantMsg);
    startAssistantStream(activeChat.id, assistantMsgId);

    setIsStreaming(true);

    try {
      const apiKey = settings.apiKeys[activeChat.provider as keyof typeof settings.apiKeys] || '';

      const updateContentCallback = (newContent: string) => {
        updateAssistantStream(activeChat.id, assistantMsgId, newContent);
      };

      await streamResponse(
        activeChat.provider,
        activeChat.model,
        [...activeChat.messages, userMsg],
        apiKey,
        updateContentCallback,
        settings.apiKeys.ollamaUrl
      );

      const finalContent = useStore.getState().chats
        .find(c => c.id === activeChat.id)
        ?.messages.find(m => m.id === assistantMsgId)?.temporaryContent || '';

      await finalizeAssistantStream(activeChat.id, assistantMsgId, finalContent);

    } catch (error) {
      console.error("Error streaming:", error);
      const errorMsg: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: "خطا در دریافت پاسخ. لطفاً کلید API را بررسی کنید.",
        createdAt: Date.now(),
      };
      await addMessage(activeChat.id, errorMsg);
      
      // Remove the streaming message
      const state = useStore.getState();
      const chat = state.chats.find(c => c.id === activeChat.id);
      if (chat) {
        const updatedMessages = chat.messages.filter(m => m.id !== assistantMsgId);
        const updatedChat = { ...chat, messages: updatedMessages, updatedAt: Date.now() };
        await import('@/lib/db/chat-db').then(m => m.saveChat(updatedChat));
        useStore.setState(state => ({ 
          chats: state.chats.map(c => c.id === activeChat.id ? updatedChat : c) 
        }));
      }
    } finally {
      setIsStreaming(false);
    }
  };

  const handleSelectPrompt = (content: string) => {
    if (chatInputRef.current) {
      chatInputRef.current.setInputValue(content);
    }
    setShowPromptLibrary(false);
  };

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-100 dark:bg-gray-900">
        <div className="text-xl">در حال بارگذاری...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans" dir="rtl">
      <Sidebar 
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={handleSelectChat}
        onDeleteChat={handleDeleteChat}
        onNewChat={handleNewChat}
      />

      <main className="flex-1 flex flex-col relative">
        {showPromptLibrary ? (
          <div className="p-4 bg-white dark:bg-gray-800 h-full">
            <button 
              onClick={() => setShowPromptLibrary(false)}
              className="mb-4 px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
            >
              بازگشت به چت
            </button>
            <PromptLibrary onSelectPrompt={handleSelectPrompt} />
          </div>
        ) : activeChat ? (
          <>
            <header className="h-14 border-b border-gray-200 dark:border-gray-700 flex items-center px-4 justify-between bg-white dark:bg-gray-800">
              <div className="font-medium">{activeChat.model}</div>
              <div className="text-xs text-gray-500">{activeChat.provider.toUpperCase()}</div>
            </header>

            <MessageList messages={activeChat.messages} />

            <ChatInput ref={chatInputRef} onSend={handleSend} isLoading={isStreaming} />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center flex-col text-gray-500">
            <h2 className="text-2xl font-bold mb-2">به TypingMind Clone خوش آمدید</h2>
            <p>یک گفتگوی جدید شروع کنید یا از منوی کناری یکی را انتخاب کنید.</p>
            <button 
              onClick={handleNewChat} 
              className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 flex items-center gap-2"
            >
              <Plus size={20} />
              شروع گفتگو
            </button>
          </div>
        )}

        {/* Bottom toolbar */}
        {!showPromptLibrary && activeChat && (
          <div className="absolute bottom-20 left-4 flex flex-col gap-2">
            <button
              onClick={() => setShowPromptLibrary(true)}
              className="p-2 bg-white dark:bg-gray-800 rounded-lg shadow hover:bg-gray-100 dark:hover:bg-gray-700"
              title="کتابخانه Prompt"
            >
              <BookOpen size={20} />
            </button>
            <button
              onClick={() => setShowSettings(true)}
              className="p-2 bg-white dark:bg-gray-800 rounded-lg shadow hover:bg-gray-100 dark:hover:bg-gray-700"
              title="تنظیمات"
            >
              <Settings size={20} />
            </button>
          </div>
        )}

        {showSettings && (
          <SettingsModal 
            settings={settings}
            onUpdateSettings={updateSettings}
            onClose={() => setShowSettings(false)}
          />
        )}
      </main>
    </div>
  );
}
