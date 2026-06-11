export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  temporaryContent?: string;
  isStreaming?: boolean;
  createdAt: number;
  model?: string;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  model: string;
  provider: 'openai' | 'anthropic' | 'google' | 'ollama' | 'azure';
  createdAt: number;
  updatedAt: number;
}

export interface Settings {
  apiKeys: {
    openai: string;
    anthropic: string;
    google: string;
    azure: string;
    ollamaUrl: string;
  };
  theme: 'light' | 'dark' | 'system';
}

export interface Prompt {
  id: string;
  title: string;
  content: string;
  category?: string;
  createdAt: number;
  updatedAt: number;
}
