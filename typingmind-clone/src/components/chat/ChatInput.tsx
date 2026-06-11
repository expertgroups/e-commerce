'use client';

import React, { forwardRef, useImperativeHandle, useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface Props {
  onSend: (text: string) => void;
  isLoading: boolean;
}

export interface ChatInputHandles {
  setInputValue: (value: string) => void;
}

const ChatInput = forwardRef<ChatInputHandles, Props>(({ onSend, isLoading }, ref) => {
  const [input, setInput] = useState('');

  useImperativeHandle(ref, () => ({
    setInputValue: (value: string) => setInput(value),
  }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSend(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
      <div className="relative flex items-center max-w-4xl mx-auto">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          placeholder="پیام خود را بنویسید..."
          className="w-full resize-none rounded-xl border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white"
          rows={1}
          style={{ minHeight: '48px', maxHeight: '200px' }}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="absolute left-2 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5" />}
        </button>
      </div>
    </form>
  );
});

ChatInput.displayName = 'ChatInput';
export default ChatInput;
