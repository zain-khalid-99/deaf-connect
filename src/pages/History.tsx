import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { History as HistoryIcon, Download, Trash2, Calendar, MessageSquare, Search, Filter, Loader2, FileJson, FileText, Table, MoreVertical, Play, Share2 } from 'lucide-react';
import { cn } from '../utils/styles';
import { fetchHistory, deleteConversation, Conversation } from '../services/dataService';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<Conversation[]>([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const loadHistory = async (query?: string) => {
    setIsLoading(true);
    try {
      const data = await fetchHistory(query);
      setHistory(data);
    } catch (err) {
      console.error(err);
      setHistory([
        { id: 1, sentence: "Hello, how are you today?", detected_words: "hello how you", timestamp: Date.now() - 100000, confidence: 0.98 },
        { id: 2, sentence: "I am deaf and use sign language.", detected_words: "i deaf sign", timestamp: Date.now() - 500000, confidence: 0.95 },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => loadHistory(search), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const handleDelete = async (id: number) => {
    if (confirm('Permanently delete this record?')) {
      await deleteConversation(id);
      setHistory(prev => prev.filter(c => c.id !== id));
    }
  };

  const exportData = (format: 'json' | 'csv' | 'txt') => {
    const data = history.map(h => ({
      id: h.id,
      timestamp: h.timestamp,
      words: h.detected_words,
      sentence: h.sentence,
      confidence: h.confidence
    }));

    let content = '';
    let type = '';
    let ext = '';

    if (format === 'json') {
      content = JSON.stringify(data, null, 2);
      type = 'application/json';
      ext = 'json';
    } else if (format === 'csv') {
      const headers = 'ID,Timestamp,Words,Sentence,Confidence\n';
      const rows = data.map(d => `${d.id},${d.timestamp},"${d.words}", "${d.sentence}", ${d.confidence}`).join('\n');
      content = headers + rows;
      type = 'text/csv';
      ext = 'csv';
    } else {
      content = data.map(d => `[${d.timestamp}] Gloss: ${d.words} -> Sentence: ${d.sentence} (Conf: ${d.confidence})`).join('\n');
      type = 'text/plain';
      ext = 'txt';
    }

    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `signsync_export_${new Date().toISOString().split('T')[0]}.${ext}`;
    a.click();
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 sm:p-10 space-y-10 max-w-7xl mx-auto h-full flex flex-col"
    >
      <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-black tracking-tighter text-black uppercase">Archive</h1>
          <p className="text-gray-400 text-sm font-medium mt-1 uppercase tracking-widest text-[10px]">Secure persistent conversation logs</p>
        </div>
        <div className="flex items-center gap-3">
           <div className="flex bg-gray-50 border border-gray-100 rounded-lg p-1">
              <button onClick={() => exportData('txt')} className="p-2.5 hover:bg-black hover:text-white rounded-md text-gray-400 transition-all" title="Export TXT">
                <FileText size={16} />
              </button>
              <button onClick={() => exportData('csv')} className="p-2.5 hover:bg-black hover:text-white rounded-md text-gray-400 transition-all" title="Export CSV">
                <Table size={16} />
              </button>
              <button onClick={() => exportData('json')} className="p-2.5 hover:bg-black hover:text-white rounded-md text-gray-400 transition-all" title="Export JSON">
                <FileJson size={16} />
              </button>
           </div>
        </div>
      </header>

      <div className="w-full max-w-2xl relative">
         <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
         <input 
           type="text" 
           placeholder="Search ARCHIVES..."
           value={search}
           onChange={(e) => setSearch(e.target.value)}
           className="w-full bg-white border border-gray-100 rounded-xl py-4 pl-14 pr-6 text-sm font-medium focus:outline-none focus:border-black transition-all shadow-sm uppercase tracking-widest text-[11px]"
         />
         {isLoading && <Loader2 className="absolute right-5 top-1/2 -translate-y-1/2 animate-spin text-black" size={18} />}
      </div>

      <div className="flex-1 bg-white border border-gray-100 rounded-xl overflow-hidden flex flex-col shadow-sm">
        <div className="hidden lg:grid grid-cols-12 gap-6 p-6 bg-gray-50 border-b border-gray-100 text-[10px] font-black uppercase tracking-widest text-gray-400">
           <div className="col-span-1">ID</div>
           <div className="col-span-6">Translation Feed</div>
           <div className="col-span-3">Timestamp</div>
           <div className="col-span-2 text-right">Actions</div>
        </div>
        <div className="flex-1 overflow-y-auto">
          <AnimatePresence>
            {history.length > 0 ? history.map((item) => (
              <motion.div 
                key={item.id} 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0, x: -10 }}
                className="p-6 border-b border-gray-50 grid grid-cols-12 gap-4 items-center hover:bg-gray-50/50 transition-all group"
              >
                 <div className="hidden lg:block col-span-1 font-black text-[10px] text-gray-300">#{item.id}</div>
                 <div className="col-span-12 lg:col-span-6 flex items-start lg:items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-gray-50 border border-gray-100 flex flex-shrink-0 items-center justify-center text-black group-hover:bg-black group-hover:text-white transition-all">
                      <MessageSquare size={20} />
                    </div>
                    <div className="flex flex-col gap-1">
                      <span className="font-bold text-black text-sm tracking-tight">{item.sentence}</span>
                      <div className="flex items-center gap-2">
                         <span className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Gloss:</span>
                         <span className="text-[9px] font-bold text-black uppercase tracking-widest bg-gray-100 px-1.5 py-0.5 rounded">{item.detected_words}</span>
                      </div>
                    </div>
                 </div>
                 <div className="col-span-12 lg:col-span-3 text-[10px] font-black text-gray-400 flex items-center gap-2 uppercase tracking-widest mt-2 lg:mt-0">
                    <Calendar size={12} className="opacity-50" />
                    {new Date(item.timestamp).toLocaleString()}
                 </div>
                 <div className="col-span-12 lg:col-span-2 flex justify-end gap-3 mt-4 lg:mt-0">
                    <button onClick={() => handleSpeak(item.sentence)} className="btn-secondary p-2.5 rounded-lg flex items-center gap-2 text-[10px] uppercase tracking-widest font-black">
                      <Play size={12} fill="black" /> <span className="lg:hidden">Play</span>
                    </button>
                    <button onClick={() => handleDelete(item.id)} className="btn-secondary p-2.5 rounded-lg text-red-500 hover:bg-red-500 hover:text-white border-red-100">
                      <Trash2 size={12} />
                    </button>
                    <button className="lg:hidden btn-secondary p-2.5 rounded-lg">
                      <Share2 size={12} />
                    </button>
                 </div>
              </motion.div>
            )) : (
              <div className="h-full flex flex-col items-center justify-center text-gray-400 gap-6 py-32">
                <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center border border-gray-100 opacity-50">
                   <Search size={32} />
                </div>
                <p className="text-[10px] font-black uppercase tracking-[0.2em]">No logs found</p>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );

  function handleSpeak(text: string) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
  }
};

