import React from 'react';
import { motion } from 'framer-motion';
import { Search, Grid, List as ListIcon, Play } from 'lucide-react';

export const ReferencesPage: React.FC = () => {
  const commonSigns = [
    { label: 'Hello', category: 'Greetings', icon: '👋' },
    { label: 'Thank You', category: 'Etiquette', icon: '🙏' },
    { label: 'Please', category: 'Etiquette', icon: '🤲' },
    { label: 'Sorry', category: 'Etiquette', icon: '😔' },
    { label: 'Help', category: 'Common', icon: '🆘' },
    { label: 'Yes', category: 'Common', icon: '✅' },
    { label: 'No', category: 'Common', icon: '❌' },
    { label: 'Water', category: 'Needs', icon: '💧' },
  ];

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-8 space-y-8"
    >
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tighter">ASL Reference Guide</h1>
          <p className="text-brand-text-secondary mt-1">Explore and learn common ASL signs supported by our AI.</p>
        </div>
        <div className="flex gap-2">
           <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-brand-text-secondary" size={16} />
              <input 
                type="text" 
                placeholder="Search signs..." 
                className="pl-10 pr-4 py-2 bg-brand-card border border-brand-border rounded-custom text-sm focus:outline-none focus:border-brand-primary"
              />
           </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
        {commonSigns.map((sign, i) => (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05 }}
            key={sign.label}
            className="glass-card aspect-square rounded-custom flex flex-col items-center justify-center gap-4 group cursor-pointer hover:bg-brand-primary/10 hover:border-brand-primary transition-all p-4"
          >
            <div className="text-4xl group-hover:scale-125 transition-transform duration-300">{sign.icon}</div>
            <div className="text-center">
              <p className="font-bold text-white uppercase tracking-tighter">{sign.label}</p>
              <p className="text-[10px] text-brand-text-secondary uppercase tracking-widest">{sign.category}</p>
            </div>
            <div className="opacity-0 group-hover:opacity-100 transition-opacity absolute bottom-3 right-3 text-brand-primary">
               <Play size={16} fill="currentColor" />
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};
