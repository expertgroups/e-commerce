'use client';

import React from 'react';
import { Settings as SettingsIcon, Moon, Sun, Monitor } from 'lucide-react';
import { Settings } from '@/types';

interface Props {
  settings: Settings;
  onUpdateSettings: (settings: Partial<Settings>) => void;
  onClose: () => void;
}

export default function SettingsModal({ settings, onUpdateSettings, onClose }: Props) {
  const [localSettings, setLocalSettings] = React.useState(settings);

  const handleSave = () => {
    onUpdateSettings(localSettings);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md" onClick={e => e.stopPropagation()}>
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <SettingsIcon size={24} />
          تنظیمات
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">OpenAI API Key</label>
            <input
              type="password"
              value={localSettings.apiKeys.openai}
              onChange={(e) => setLocalSettings({...localSettings, apiKeys: {...localSettings.apiKeys, openai: e.target.value}})}
              className="w-full p-2 rounded border dark:bg-gray-700 dark:border-gray-600"
              placeholder="sk-..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Anthropic API Key</label>
            <input
              type="password"
              value={localSettings.apiKeys.anthropic}
              onChange={(e) => setLocalSettings({...localSettings, apiKeys: {...localSettings.apiKeys, anthropic: e.target.value}})}
              className="w-full p-2 rounded border dark:bg-gray-700 dark:border-gray-600"
              placeholder="sk-ant-..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Google API Key</label>
            <input
              type="password"
              value={localSettings.apiKeys.google}
              onChange={(e) => setLocalSettings({...localSettings, apiKeys: {...localSettings.apiKeys, google: e.target.value}})}
              className="w-full p-2 rounded border dark:bg-gray-700 dark:border-gray-600"
              placeholder="AIza..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Ollama URL</label>
            <input
              type="text"
              value={localSettings.apiKeys.ollamaUrl}
              onChange={(e) => setLocalSettings({...localSettings, apiKeys: {...localSettings.apiKeys, ollamaUrl: e.target.value}})}
              className="w-full p-2 rounded border dark:bg-gray-700 dark:border-gray-600"
              placeholder="http://localhost:11434"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">تم</label>
            <div className="flex gap-2">
              <button
                onClick={() => setLocalSettings({...localSettings, theme: 'light'})}
                className={`flex items-center gap-1 px-3 py-2 rounded ${localSettings.theme === 'light' ? 'bg-blue-100 dark:bg-blue-900' : 'hover:bg-gray-100 dark:hover:bg-gray-700'}`}
              >
                <Sun size={18} /> روشن
              </button>
              <button
                onClick={() => setLocalSettings({...localSettings, theme: 'dark'})}
                className={`flex items-center gap-1 px-3 py-2 rounded ${localSettings.theme === 'dark' ? 'bg-blue-100 dark:bg-blue-900' : 'hover:bg-gray-100 dark:hover:bg-gray-700'}`}
              >
                <Moon size={18} /> تاریک
              </button>
              <button
                onClick={() => setLocalSettings({...localSettings, theme: 'system'})}
                className={`flex items-center gap-1 px-3 py-2 rounded ${localSettings.theme === 'system' ? 'bg-blue-100 dark:bg-blue-900' : 'hover:bg-gray-100 dark:hover:bg-gray-700'}`}
              >
                <Monitor size={18} /> سیستم
              </button>
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            لغو
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            ذخیره
          </button>
        </div>
      </div>
    </div>
  );
}
