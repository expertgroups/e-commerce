import { openDB, DBSchema, IDBPDatabase } from 'idb';
import { Prompt } from '@/types';

interface PromptDB extends DBSchema {
  prompts: {
    key: string;
    value: Prompt;
    indexes: {
      'by-category': string;
      'by-date': number;
    };
  };
}

let promptDbPromise: Promise<IDBPDatabase<PromptDB>> | null = null;

export const initPromptDB = () => {
  if (!promptDbPromise) {
    promptDbPromise = openDB<PromptDB>('typingmind-prompts-db', 1, {
      upgrade(db) {
        const store = db.createObjectStore('prompts', { keyPath: 'id' });
        store.createIndex('by-category', 'category');
        store.createIndex('by-date', 'updatedAt');
      },
    });
  }
  return promptDbPromise;
};

export const savePrompt = async (prompt: Prompt) => {
  const db = await initPromptDB();
  await db.put('prompts', prompt);
};

export const getAllPrompts = async () => {
  const db = await initPromptDB();
  return db.getAllFromIndex('prompts', 'by-date');
};

export const deletePrompt = async (id: string) => {
  const db = await initPromptDB();
  await db.delete('prompts', id);
};
