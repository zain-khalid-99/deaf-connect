import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, Volume2, Globe, RefreshCcw, Loader2, Copy, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../utils/styles';
import ReactMarkdown from 'react-markdown';
import { translateText, speakText, LanguageCode } from '../services/translationService';

export type Message = {
  id: string;
  text: string;
  sender: 'user' | 'system'; 
  timestamp: number;
};

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
  targetLang?: LanguageCode;
}

const MessageBubble: React.FC<{ msg: Message; targetLang: LanguageCode }> = ({ msg, targetLang }) => {
  const [translatedText, setTranslatedText] = useState<string | null>(null);
  const [isTranslating, setIsTranslating] = useState(false);

  const handleTranslate = async () => {
    if (isTranslating) return;
    setIsTranslating(true);
    try {
      const result = await translateText(msg.text, targetLang);
      setTranslatedText(result);
    } catch (err) {
      console.error(err);
    } finally {
      setIsTranslating(false);
    }
  };

  const handleSpeak = async () => {
    speakText(translatedText || msg.text, translatedText ? targetLang : 'en-US');
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "max-w-[85%] flex flex-col gap-1.5",
        msg.sender === 'user' ? "self-start" : "self-end"
      )}
    >
      <div
        className={cn(
          "p-4 text-sm leading-relaxed shadow-sm transition-all",
          msg.sender === 'user' 
            ? "bg-black text-white rounded-2xl rounded-tl-none" 
            : "bg-white border border-gray-100 text-black rounded-2xl rounded-tr-none"
        )}
      >
        <div className="prose prose-sm max-w-none text-inherit">
          <ReactMarkdown>{translatedText || msg.text}</ReactMarkdown>
        </div>
      </div>
      
      {/* Actions */}
      <div className={cn(
        "flex gap-3 px-1 transition-opacity",
        msg.sender === 'user' ? "justify-start" : "justify-end"
      )}>
        <button 
          onClick={handleTranslate}
          disabled={isTranslating}
          className={cn(
            "flex items-center gap-1 text-[9px] font-black uppercase tracking-widest transition-colors",
            isTranslating ? "text-gray-400 animate-pulse" : "text-gray-400 hover:text-black"
          )}
        >
          {isTranslating ? <Loader2 size={10} className="animate-spin" /> : <Globe size={10} />}
          <span>Translate</span>
        </button>
        <button 
          onClick={handleSpeak}
          className="flex items-center gap-1 text-[9px] font-black uppercase tracking-widest text-gray-400 hover:text-black transition-colors"
        >
          <Volume2 size={10} />
          <span>Listen</span>
        </button>
        <button 
          onClick={() => navigator.clipboard.writeText(translatedText || msg.text)}
          className="flex items-center gap-1 text-[9px] font-black uppercase tracking-widest text-gray-400 hover:text-black transition-colors"
        >
          <Copy size={10} />
          <span>Copy</span>
        </button>
      </div>

      {translatedText && (
        <span className="text-[8px] text-gray-400 uppercase font-black tracking-widest px-1">
          Synced to {targetLang}
        </span>
      )}
    </motion.div>
  );
};

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ messages, onSendMessage, targetLang = 'en' }) => {
  const [inputText, setInputText] = useState("");
  const [isListening, setIsListening] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (inputText.trim()) {
      onSendMessage(inputText);
      setInputText("");
    }
  };

  const startListening = () => {
    if (!('webkitSpeechRecognition' in window) && !('speechRecognition' in window)) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).speechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setInputText(transcript);
    };

    recognition.start();
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-8 scroll-smooth flex flex-col">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center opacity-30 gap-4">
             <div className="w-12 h-12 bg-gray-50 rounded-full flex items-center justify-center border border-gray-100">
                <RefreshCcw size={20} className="text-gray-400" />
             </div>
             <p className="text-[10px] font-black uppercase tracking-[0.2em]">Neural Feed Ready</p>
          </div>
        )}
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <MessageBubble key={msg.id} msg={msg} targetLang={targetLang} />
          ))}
        </AnimatePresence>
      </div>

      {/* Input Area */}
      <div className="p-4 bg-gray-50/50 border-t border-gray-100">
        <div className="relative group max-w-4xl mx-auto">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your response..."
            className="w-full bg-white border border-gray-200 rounded-xl py-4 pl-5 pr-28 text-sm focus:outline-none focus:border-black transition-all shadow-sm"
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSend();
              }
            }}
          />

          <div className="absolute right-2 top-2 bottom-2 flex items-center gap-2">
            <button 
              onClick={startListening}
              className={cn(
                "w-10 h-10 flex items-center justify-center rounded-lg transition-all",
                isListening ? "bg-red-500 text-white animate-pulse" : "bg-gray-100 text-gray-500 hover:bg-black hover:text-white"
              )}
            >
              <Mic size={18} />
            </button>

            <button 
              onClick={handleSend}
              disabled={!inputText.trim()}
              className={cn(
                "w-10 h-10 flex items-center justify-center rounded-lg transition-all shadow-lg",
                inputText.trim() ? "bg-black text-white" : "bg-gray-200 text-white cursor-not-allowed"
              )}
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};


function MessageSquareIcon({ size }: { size: number }) {
  return (
    <svg 
      width={size} 
      height={size} 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="1.5" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    >
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
  );
}
