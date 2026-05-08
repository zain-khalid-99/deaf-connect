import React, { useState, useEffect } from 'react';
import { ASLVideoFeed } from '../components/ASLVideoFeed';
import { ChatInterface, type Message } from '../components/ChatInterface';
import { motion } from 'framer-motion';
import { Activity, Target, Zap, Mic, Trash2, Volume2, Send, Globe, ChevronUp, ChevronDown } from 'lucide-react';
import { cn } from '../utils/styles';
import { LANGUAGES, LanguageCode, translateText } from '../services/translationService';

export const CommunicationPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [selectedLang, setSelectedLang] = useState<LanguageCode>('en');
  const [sessionStats, setSessionStats] = useState({
    fps: 0,
    confidence: 0,
    signsDetected: 0,
    status: 'Idle'
  });
  const [isMobile, setIsMobile] = useState(window.innerWidth < 1024);
  const [showChatOnMobile, setShowChatOnMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 1024);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const addMessage = (text: string, sender: 'user' | 'system') => {
    const newMessage: Message = {
      id: Math.random().toString(36).substr(2, 9),
      text,
      sender,
      timestamp: Date.now(),
    };
    setMessages(prev => [...prev, newMessage]);
    if (sender === 'user') {
      setSessionStats(prev => ({ ...prev, signsDetected: prev.signsDetected + 1 }));
    } else {
      fetch('/api/conversations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          sentence: text, 
          detected_words: ['voice'], 
          confidence: 1.0 
        }),
      }).catch(console.error);
    }
  };

  const [isTranslatingMsg, setIsTranslatingMsg] = useState(false);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;
    
    if (selectedLang !== 'en') {
      setIsTranslatingMsg(true);
      try {
        const translated = await translateText(text, selectedLang);
        addMessage(translated, 'system');
      } catch (err) {
        console.error("Manual message translation failed:", err);
        addMessage(text, 'system');
      } finally {
        setIsTranslatingMsg(false);
      }
    } else {
      addMessage(text, 'system');
    }
  };

  const [isListening, setIsListening] = useState(false);

  const startListening = () => {
    if (!('webkitSpeechRecognition' in window) && !('speechRecognition' in window)) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).speechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = selectedLang === 'en' ? 'en-US' : selectedLang;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      handleSendMessage(transcript);
    };

    recognition.start();
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-full overflow-hidden bg-white"
    >
      {/* Header */}
      <header className="h-[64px] border-b border-gray-100 flex items-center justify-between px-6 bg-white/80 backdrop-blur-md flex-shrink-0 z-20">
        <div className="hidden sm:block">
          <h1 className="text-sm font-bold tracking-tight uppercase">Live Translation</h1>
          <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">Neural Pipeline Active</p>
        </div>
        <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
          <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-50 border border-gray-100 rounded-lg">
            <Globe size={14} className="text-black" />
            <select 
              value={selectedLang}
              onChange={(e) => setSelectedLang(e.target.value as LanguageCode)}
              className="bg-transparent text-[10px] font-bold text-black uppercase tracking-wider focus:outline-none cursor-pointer"
            >
              {Object.entries(LANGUAGES).map(([label, code]) => (
                <option key={code} value={code} className="bg-white text-black">
                  {label}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 border border-green-100 rounded-full">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
            <span className="text-[9px] font-bold text-green-600 uppercase tracking-widest">Neural Link Online</span>
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Main Processing Area (Left) */}
        <div className="flex-1 flex flex-col border-r border-gray-100 h-full overflow-hidden bg-gray-50">
          <div className="flex-1 relative">
            <ASLVideoFeed 
              onNewMessage={addMessage} 
              onStatsUpdate={(fps, conf) => setSessionStats(prev => ({ ...prev, fps, confidence: conf }))}
              targetLang={selectedLang}
            />
          </div>
          
          {/* Voice-to-Text Bar */}
          <div className="p-4 bg-white border-t border-gray-100 shadow-sm z-10">
            <div className="flex items-center gap-4 max-w-4xl mx-auto w-full">
              <button 
                onClick={startListening}
                className={cn(
                  "flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center transition-all border shadow-sm",
                  isListening ? "bg-red-500 border-red-500 text-white animate-pulse" : "bg-black border-black text-white hover:bg-gray-800"
                )}
              >
                <Mic size={20} />
              </button>
              <div className="flex-1 min-w-0">
                {isListening ? (
                  <div className="flex items-center gap-3">
                    <span className="flex gap-1.5">
                      {[1,2,3,4].map(i => (
                        <motion.div 
                          key={i}
                          animate={{ height: [4, 16, 4] }}
                          transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.1 }}
                          className="w-1 bg-black rounded-full"
                        />
                      ))}
                    </span>
                    <span className="text-xs text-black font-bold uppercase tracking-widest animate-pulse">Capturing Audio...</span>
                  </div>
                ) : (
                  <div className="flex flex-col">
                    <span className="text-xs text-gray-800 font-bold uppercase tracking-tight">Voice Recognition</span>
                    <span className="text-[10px] text-gray-400 font-medium italic">Click to capture speech for the hearing impaired.</span>
                  </div>
                )}
              </div>
              
              {!isMobile && (
                <div className="flex gap-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                  <div className="flex items-center gap-1.5">
                    <Activity size={12} />
                    <span className="text-black">{(sessionStats.confidence * 100).toFixed(0)}% CONF</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <Target size={12} />
                    <span className="text-black">{sessionStats.fps} FPS</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Conversation Sidebar (Right) */}
        <aside className={cn(
          "bg-white h-full transition-all duration-300 ease-in-out border-l border-gray-100 flex flex-col z-30",
          isMobile 
            ? `fixed bottom-0 left-0 right-0 h-[60vh] rounded-t-3xl shadow-2xl-up ${showChatOnMobile ? 'translate-y-0' : 'translate-y-full'}` 
            : "w-[400px]"
        )}>
          {isMobile && (
            <button 
              onClick={() => setShowChatOnMobile(!showChatOnMobile)}
              className="absolute -top-12 left-1/2 -translate-x-1/2 bg-white border border-gray-100 px-4 py-2 rounded-t-xl flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest shadow-lg"
            >
              {showChatOnMobile ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
              {showChatOnMobile ? 'Close Feed' : 'Open Feed'}
            </button>
          )}
          
          <div className="p-4 border-b border-gray-50 flex items-center justify-between">
             <h3 className="text-[10px] font-extrabold text-black uppercase tracking-widest">Translation Feed</h3>
             <div className="flex gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <div className="w-2 h-2 rounded-full bg-gray-200" />
                <div className="w-2 h-2 rounded-full bg-gray-200" />
             </div>
          </div>
          <div className="flex-1 min-h-0">
            <ChatInterface 
              messages={messages} 
              onSendMessage={handleSendMessage} 
              targetLang={selectedLang}
            />
          </div>
        </aside>
      </div>
    </motion.div>
  );
};

