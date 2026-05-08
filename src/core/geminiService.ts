import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || '' });

export async function translateAslGlossToEnglish(gloss: string): Promise<string> {
  if (!gloss.trim()) return "";
  
  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: `Translate the following ASL gloss sequence into a natural, grammatically correct English sentence. 
      The gloss is: "${gloss}"
      Only provide the translated sentence, nothing else.`,
      config: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
      }
    });

    return response.text?.trim() || gloss;
  } catch (error) {
    console.error("Gemini Translation Error:", error);
    return gloss; // Fallback to raw gloss
  }
}

export async function translateVoiceToSimpleText(speech: string): Promise<string> {
  // Can be used to simplify complex spoken English for deaf users if needed
  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: `Simplify the following English text for a deaf user who prefers clear, direct communication. 
      Input: "${speech}"`,
    });
    return response.text?.trim() || speech;
  } catch {
    return speech;
  }
}
