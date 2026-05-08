import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || '' });

export const LANGUAGES = {
  "English 🇺🇸": "en",
  "Urdu 🇵🇰": "ur",
  "Hindi 🇮🇳": "hi",
  "Arabic 🇸🇦": "ar",
  "French 🇫🇷": "fr",
  "Russian 🇷🇺": "ru",
  "Chinese 🇨🇳": "zh-cn"
};

export type LanguageCode = typeof LANGUAGES[keyof typeof LANGUAGES];

export async function translateText(text: string, targetLang: string): Promise<string> {
  try {
    const prompt = `Translate the following text into the language with code "${targetLang}". 
    Provide ONLY the translated text, no explanations or additional words.
    
    Text: "${text}"`;

    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt
    });

    return response.text?.trim() || text;
  } catch (error) {
    console.error("Translation failed:", error);
    return text; // Fallback to original
  }
}

export interface SpeakOptions {
  speed?: number;
  volume?: number;
  voiceProfile?: string;
}

export function speakText(text: string, langCode: string, options: SpeakOptions = {}) {
  if (!window.speechSynthesis) return;
  
  // Cancel any ongoing speech
  window.speechSynthesis.cancel();
  
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = langCode;
  utterance.rate = options.speed || 1;
  utterance.volume = options.volume || 1;
  
  // Try to find a matching voice
  const voices = window.speechSynthesis.getVoices();
  const voice = voices.find(v => v.lang.startsWith(langCode));
  if (voice) utterance.voice = voice;
  
  window.speechSynthesis.speak(utterance);
}
