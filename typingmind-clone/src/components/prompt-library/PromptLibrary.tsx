'use client';

import React, { useState, useEffect } from 'react';
import { getAllPrompts, savePrompt, deletePrompt } from '@/lib/db/prompt-db';
import { Prompt } from '@/types';
import { Plus, Trash2 } from 'lucide-react';

interface Props {
  onSelectPrompt: (content: string) => void;
}

export default function PromptLibrary({ onSelectPrompt }: Props) {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [newPrompt, setNewPrompt] = useState({ title: '', content: '', category: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPrompts();
  }, []);

  const loadPrompts = async () => {
    setLoading(true);
    try {
      const data = await getAllPrompts();
      setPrompts(data.sort((a, b) => b.updatedAt - a.updatedAt));
    } catch (error) {
      console.error('Failed to load prompts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!newPrompt.title.trim() || !newPrompt.content.trim()) return;
    const promptToSave: Prompt = {
      id: crypto.randomUUID(),
      title: newPrompt.title,
      content: newPrompt.content,
      category: newPrompt.category || undefined,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    await savePrompt(promptToSave);
    setNewPrompt({ title: '', content: '', category: '' });
    loadPrompts();
  };

  const handleDelete = async (id: string) => {
    await deletePrompt(id);
    loadPrompts();
  };

  if (loading) return <div className="p-4 text-center">در حال بارگذاری...</div>;

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-lg font-semibold mb-4 border-b pb-2">کتابخانه Prompt</h2>

      <div className="mb-4 space-y-2">
        <input
          type="text"
          placeholder="عنوان Prompt"
          value={newPrompt.title}
          onChange={(e) => setNewPrompt({...newPrompt, title: e.target.value})}
          className="w-full p-2 rounded border dark:bg-gray-700 dark:border-gray-600"
        />
        <textarea
          placeholder="محتوای Prompt"
          value={newPrompt.content}
          onChange={(e) => setNewPrompt({...newPrompt, content: e.target.value})}
          className="w-full p-2 rounded border dark:bg-gray-700 dark:border-gray-600"
          rows={3}
        />
        <input
          type="text"
          placeholder="دسته (اختیاری)"
          value={newPrompt.category}
          onChange={(e) => setNewPrompt({...newPrompt, category: e.target.value})}
          className="w-full p-2 rounded border dark:bg-gray-700 dark:border-gray-600"
        />
        <button
          onClick={handleSave}
          className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center justify-center gap-1"
        >
          <Plus size={16} /> ذخیره Prompt
        </button>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2">
        {prompts.map(prompt => (
          <div key={prompt.id} className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
            <div className="flex justify-between items-start">
              <h3 className="font-medium">{prompt.title}</h3>
              <button
                onClick={(e) => { e.stopPropagation(); handleDelete(prompt.id); }}
                className="text-red-500 hover:text-red-700 p-1"
              >
                <Trash2 size={14} />
              </button>
            </div>
            {prompt.category && <div className="text-xs text-gray-500 mb-1">دسته: {prompt.category}</div>}
            <p className="text-sm text-gray-700 dark:text-gray-300 truncate" onClick={() => onSelectPrompt(prompt.content)}>
              {prompt.content}
            </p>
            <div className="text-xs text-gray-500 mt-1">
              {new Date(prompt.updatedAt).toLocaleDateString()}
            </div>
          </div>
        ))}
        {prompts.length === 0 && <p className="text-center text-gray-500">هیچ Prompt ذخیره‌شده‌ای وجود ندارد.</p>}
      </div>
    </div>
  );
}
