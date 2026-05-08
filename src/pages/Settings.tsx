import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Camera, Mic, Volume2, Shield, Cpu, Monitor, Save, RotateCcw, ChevronDown, Check, Sliders, HardDrive, Bell } from 'lucide-react';
import { fetchSettings, updateSetting } from '../services/dataService';
import { cn } from '../utils/styles';

export const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<Record<string, string>>({});
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const loadSettings = async () => {
      const data = await fetchSettings();
      setSettings(data);
    };
    loadSettings();
  }, []);

  const handleUpdateSetting = async (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: String(value) }));
    await updateSetting(key, String(value));
    window.dispatchEvent(new CustomEvent('settings-updated'));
  };

  const handleSave = async () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      setMessage("System synchronized.");
      setTimeout(() => setMessage(null), 3000);
    }, 800);
  };

  const sections = [
    { 
      title: 'Neural Engine', 
      icon: Cpu, 
      desc: 'Precision tracking and inference parameters.',
      items: [
        { label: 'Inference Threshold', key: 'confidence_threshold', type: 'select', options: ['0.5', '0.6', '0.7', '0.8', '0.9'] },
        { label: 'Sentence Timeout', key: 'sentence_timeout', type: 'select', options: ['1.5', '2.0', '2.5', '3.0', '5.0'] },
        { label: 'AI Synthesis', key: 'ai_translation_enabled', type: 'toggle' },
      ]
    },
    { 
      title: 'Voice Output', 
      icon: Volume2, 
      desc: 'Speech synthesis and acoustic feedback.',
      items: [
        { label: 'Neural Profile', key: 'tts_voice', type: 'select', options: ['Neural (Male)', 'Neural (Female)', 'System Default'] },
        { label: 'Voice Speed', key: 'tts_speed', type: 'slider', min: 0.5, max: 2, step: 0.1 },
        { label: 'Auto-Speak', key: 'auto_speak', type: 'toggle' },
      ]
    },
    { 
      title: 'Infrastructure', 
      icon: HardDrive, 
      desc: 'Hardware acceleration and display settings.',
      items: [
        { label: 'Capture Quality', key: 'webcam_res', type: 'select', options: ['720p', '1080p', '480p'] },
        { label: 'Global Theme', key: 'theme', type: 'select', options: ['light', 'dark'] },
        { label: 'Push Notifications', key: 'notifications_enabled', type: 'toggle' },
      ]
    }
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 sm:p-10 space-y-10 max-w-5xl mx-auto h-full overflow-y-auto"
    >
      <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-black tracking-tighter text-black uppercase">Preferences</h1>
          <p className="text-gray-400 text-sm font-medium mt-1 uppercase tracking-widest text-[10px]">Configure terminal behavior and neural link</p>
        </div>
        <AnimatePresence>
          {message && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="px-4 py-2 bg-black text-white text-[10px] font-black rounded-lg flex items-center gap-2 uppercase tracking-widest shadow-xl"
            >
              <Check size={12} /> {message}
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      <div className="space-y-8 pb-20">
        {sections.map((section) => (
          <div key={section.title} className="bg-white border border-gray-100 rounded-xl overflow-hidden shadow-sm">
            <div className="p-6 bg-gray-50 border-b border-gray-50 flex items-center gap-4">
               <div className="w-10 h-10 bg-white border border-gray-100 rounded-lg flex items-center justify-center text-black">
                 <section.icon size={20} />
               </div>
               <div>
                  <h3 className="font-black text-xs uppercase tracking-widest text-black">{section.title}</h3>
                  <p className="text-[10px] font-bold text-gray-400 uppercase tracking-tight mt-0.5">{section.desc}</p>
               </div>
            </div>
            
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
               {section.items.map((item: any) => (
                 <div key={item.key} className="flex flex-col gap-3">
                    <label className="text-[9px] font-black uppercase tracking-widest text-gray-400">{item.label}</label>
                    <div className="h-14 px-4 bg-gray-50 border border-gray-100 rounded-xl flex items-center justify-between text-xs group focus-within:border-black transition-all">
                       {item.type === 'toggle' ? (
                          <>
                            <span className="text-[10px] font-black text-black uppercase tracking-widest">{settings[item.key] === 'true' ? 'Active' : 'Muted'}</span>
                            <button 
                              onClick={() => handleUpdateSetting(item.key, settings[item.key] === 'true' ? 'false' : 'true')}
                              className={cn(
                                "w-11 h-6 rounded-full transition-all relative",
                                settings[item.key] === 'true' ? "bg-black" : "bg-gray-200"
                              )}
                            >
                               <div className={cn(
                                   "absolute top-1 w-4 h-4 bg-white rounded-full transition-all shadow-sm",
                                   settings[item.key] === 'true' ? "left-6" : "left-1"
                               )} />
                            </button>
                          </>
                       ) : item.type === 'slider' ? (
                          <div className="w-full flex items-center gap-4">
                             <input 
                               type="range"
                               min={item.min}
                               max={item.max}
                               step={item.step}
                               value={settings[item.key] || item.min}
                               onChange={(e) => handleUpdateSetting(item.key, e.target.value)}
                               className="flex-1 accent-black cursor-pointer h-1 bg-gray-200 rounded-full appearance-none"
                             />
                             <span className="text-[10px] font-black text-black min-w-[20px]">{settings[item.key] || item.min}</span>
                          </div>
                       ) : (
                          <div className="relative w-full">
                            <select 
                              value={settings[item.key] || ''}
                              onChange={(e) => handleUpdateSetting(item.key, e.target.value)}
                              className="w-full bg-transparent text-black font-black uppercase tracking-widest text-[10px] focus:outline-none cursor-pointer appearance-none pr-8"
                            >
                               {item.options?.map((opt: string) => (
                                 <option key={opt} value={opt} className="bg-white text-black">{opt}</option>
                               ))}
                            </select>
                            <div className="absolute right-0 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
                               <ChevronDown size={14} />
                            </div>
                          </div>
                       )}
                    </div>
                 </div>
               ))}
            </div>
          </div>
        ))}
      </div>
      
      <div className="fixed bottom-0 left-0 right-0 p-6 sm:left-[280px] bg-white/80 backdrop-blur-xl border-t border-gray-100 flex justify-end gap-4 z-40">
         <button className="text-[10px] font-black uppercase tracking-widest text-gray-400 hover:text-black transition-colors px-6">
            Discard
         </button>
         <button 
            onClick={handleSave}
            className="btn-primary flex items-center gap-3 px-10 py-4 text-[10px] uppercase tracking-widest shadow-2xl"
         >
            {isSaving ? <RotateCcw size={14} className="animate-spin" /> : <Save size={14} />}
            {isSaving ? "Syncing..." : "Commit Changes"}
         </button>
      </div>
    </motion.div>
  );
};

