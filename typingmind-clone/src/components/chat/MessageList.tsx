'use client';

import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '@/types';
import { clsx } from 'clsx';

interface Props {
  messages: Message[];
}

export default function MessageList({ messages }: Props) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-gray-50 dark:bg-gray-900">
      {messages.map((msg) => {
        const displayContent = msg.isStreaming ? (msg.temporaryContent || '') : msg.content;
        const isTemporary = msg.isStreaming;

        return (
          <div
            key={msg.id}
            className={clsx(
              "flex w-full",
              msg.role === 'user' ? "justify-end" : "justify-start"
            )}
          >
            <div
              className={clsx(
                "max-w-[80%] rounded-2xl p-4 shadow-sm",
                msg.role === 'user'
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 rounded-bl-none border border-gray-200 dark:border-gray-700",
                isTemporary && "animate-pulse"
              )}
            >
              <div className="prose dark:prose-invert prose-sm max-w-none">
                <ReactMarkdown>{displayContent}</ReactMarkdown>
              </div>
              <div className="text-xs opacity-50 mt-2 text-left">
                {new Date(msg.createdAt).toLocaleTimeString()}
                {isTemporary && <span className="ml-1">...</span>}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
