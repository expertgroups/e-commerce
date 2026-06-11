import { Message } from '@/types';

export async function streamResponse(
  provider: string,
  model: string,
  messages: Message[],
  apiKey: string,
  onChunk: (content: string) => void,
  ollamaUrl?: string
): Promise<void> {
  const formattedMessages = messages.map((msg) => ({
    role: msg.role,
    content: msg.content,
  }));

  if (provider === 'openai') {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: formattedMessages,
        stream: true,
      }),
    });

    if (!response.ok) throw new Error(`OpenAI Error: ${response.statusText}`);

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') continue;

          try {
            const parsed = JSON.parse(data);
            const content = parsed.choices?.[0]?.delta?.content || '';
            if (content) {
              fullContent += content;
              onChunk(fullContent);
            }
          } catch (e) {
            // Ignore parse errors
          }
        }
      }
    }
  } else if (provider === 'anthropic') {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model,
        max_tokens: 4096,
        messages: formattedMessages.filter(m => m.role !== 'system'),
        stream: true,
      }),
    });

    if (!response.ok) throw new Error(`Anthropic Error: ${response.statusText}`);

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') continue;

          try {
            const parsed = JSON.parse(data);
            if (parsed.type === 'content_block_delta' && parsed.delta?.text) {
              fullContent += parsed.delta.text;
              onChunk(fullContent);
            }
          } catch (e) {
            // Ignore parse errors
          }
        }
      }
    }
  } else if (provider === 'google') {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: formattedMessages.map(m => ({
          role: m.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: m.content }],
        })),
      }),
    });

    if (!response.ok) throw new Error(`Google Error: ${response.statusText}`);

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      // Google returns an array of responses
      const matches = chunk.match(/"text":\s*"([^"]*)"/g);
      if (matches) {
        for (const match of matches) {
          const text = match.replace(/"text":\s*"|"/g, '');
          fullContent += text;
          onChunk(fullContent);
        }
      }
    }
  } else if (provider === 'ollama') {
    const baseUrl = ollamaUrl || 'http://localhost:11434';
    const response = await fetch(`${baseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model,
        messages: formattedMessages,
        stream: true,
      }),
    });

    if (!response.ok) throw new Error(`Ollama Error: ${response.statusText}`);

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.trim()) {
          try {
            const parsed = JSON.parse(line);
            const content = parsed.message?.content || '';
            if (content) {
              fullContent += content;
              onChunk(fullContent);
            }
          } catch (e) {
            // Ignore parse errors
          }
        }
      }
    }
  } else {
    throw new Error(`Unsupported provider: ${provider}`);
  }
}
