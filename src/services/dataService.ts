/**
 * Data Service for persistence
 */

export interface Conversation {
  id: number;
  sentence: string;
  detected_words: string;
  confidence: number;
  timestamp: string;
  is_deleted: number;
}

export interface Analytics {
  total_conversations: number;
  total_words: number;
  total_sentences: number;
  average_confidence: number;
}

export async function fetchHistory(search?: string): Promise<Conversation[]> {
  const url = search ? `/api/conversations?search=${encodeURIComponent(search)}` : '/api/conversations';
  const res = await fetch(url);
  return res.json();
}

export async function saveConversation(data: { sentence: string; detected_words: string[]; confidence: number }): Promise<Conversation> {
  const res = await fetch('/api/conversations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function deleteConversation(id: number): Promise<void> {
  await fetch(`/api/conversations/${id}`, { method: 'DELETE' });
}

export async function fetchAnalytics(): Promise<Analytics> {
  const res = await fetch('/api/analytics');
  return res.json();
}

export async function fetchSettings(): Promise<Record<string, string>> {
  const res = await fetch('/api/settings');
  return res.json();
}

export async function updateSetting(key: string, value: string): Promise<void> {
  await fetch('/api/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key, value }),
  });
}
