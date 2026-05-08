import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Cpu, Camera, MessageSquare, Zap, Shield, Book } from 'lucide-react';

export const DocumentationPage: React.FC = () => {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-8 space-y-12 max-w-5xl mx-auto"
    >
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-black tracking-tighter uppercase">System Documentation</h1>
        <p className="text-brand-text-secondary max-w-2xl mx-auto">
          Technical specifications and user guidance for the Deaf Connect Real-Time ASL Communication Terminal.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-8">
          <section className="space-y-4">
             <div className="flex items-center gap-4 text-brand-primary">
                <Cpu size={24} />
                <h2 className="text-2xl font-bold tracking-tight">The Neural Engine</h2>
             </div>
             <p className="text-brand-text-secondary leading-relaxed">
               Our system utilizes a multi-layered approach to gesture recognition. First, <b>MediaPipe Hands</b> extracts 21 high-fidelity 3D landmarks from your hand movements at up to 60 FPS. These landmarks are then processed by our <b>Transformer-based sign classifier</b> which recognizes ASL gloss.
             </p>
             <div className="glass-card p-4 rounded-custom border-l-4 border-l-brand-primary bg-brand-primary/5">
                <p className="text-sm italic">
                  "The engine is optimized for single-hand detection to ensure maximum portability and performance on edge devices."
                </p>
             </div>
          </section>

          <section className="space-y-4">
             <div className="flex items-center gap-4 text-brand-secondary">
                <MessageSquare size={24} />
                <h2 className="text-2xl font-bold tracking-tight">ASL-to-English Neural Translation</h2>
             </div>
             <p className="text-brand-text-secondary leading-relaxed">
               ASL is not "English with hands"—it has its own unique grammar and structure. Deaf Connect captures raw ASL gloss and uses <b>Gemini 2.0 Flash</b> to contextually translate those signals into natural, grammatically correct English sentences.
             </p>
          </section>
        </div>

        <div className="space-y-6">
           <div className="glass-card p-6 rounded-custom border-brand-border">
              <h3 className="font-bold flex items-center gap-2 mb-4">
                 <Book size={18} className="text-brand-primary" />
                 Quick Start
              </h3>
              <ul className="space-y-4">
                {[
                  { step: "01", text: "Position your hand within the frame" },
                  { step: "02", text: "Perform signs clearly and steadily" },
                  { step: "03", text: "Click 'ADD SIGN' to build your sentence" },
                  { step: "04", text: "Hit 'TRANSLATE' to broadcast speech" },
                ].map(item => (
                  <li key={item.step} className="flex gap-4">
                     <span className="text-brand-primary font-mono font-bold">{item.step}</span>
                     <span className="text-sm text-brand-text-secondary">{item.text}</span>
                  </li>
                ))}
              </ul>
           </div>

           <div className="glass-card p-6 rounded-custom border-brand-border flex items-center gap-4">
              <Shield className="text-brand-primary" size={32} />
              <div>
                 <h4 className="font-bold text-sm">Priority Privacy</h4>
                 <p className="text-[10px] text-brand-text-secondary mt-1 uppercase tracking-widest font-mono">
                   Data processed locally
                 </p>
              </div>
           </div>
        </div>
      </div>
    </motion.div>
  );
};
