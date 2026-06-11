import { openDB, DBSchema, IDBPDatabase } from 'idb';
import { Chat } from '@/types';

interface ChatDB extends DBSchema {
  chats: {
    key: string;
    value: Chat;
    indexes: {
      'by-date': number;
    };
  };
}

let dbPromise: Promise<IDBPDatabase<ChatDB>> | null = null;

export const initDB = () => {
  if (!dbPromise) {
    dbPromise = openDB<ChatDB>('typingmind-db', 1, {
      upgrade(db) {
        const store = db.createObjectStore('chats', { keyPath: 'id' });
        store.createIndex('by-date', 'updatedAt');
      },
    });
  }
  return dbPromise;
};

export const saveChat = async (chat: Chat) => {
  const db = await initDB();
  await db.put('chats', chat);
};

export const getAllChats = async () => {
  const db = await initDB();
  return db.getAllFromIndex('chats', 'by-date');
};

export const getChat = async (id: string) => {
  const db = await initDB();
  return db.get('chats', id);
};

export const deleteChat = async (id: string) => {
  const db = await initDB();
  await db.delete('chats', id);
};

export const clearAllChats = async () => {
  const db = await initDB();
  const tx = db.transaction('chats', 'readwrite');
  await tx.store.clear();
};
