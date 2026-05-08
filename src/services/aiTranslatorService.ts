/**
 * AI Sentence Generation Service
 * Proxies requests to our server which interacts with Groq API
 */

export async function generateAiSentence(words: string[]): Promise<string> {
  if (!words || words.length === 0) return "";
  
  try {
    const response = await fetch("/api/translate-sentence", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ words }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    const data = await response.json();
    return data.sentence;
  } catch (error) {
    console.error("AI Translation Error:", error);
    // Fallback to simple join if AI fails
    return words.join(" ");
  }
}
