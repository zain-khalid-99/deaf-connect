import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Target, Globe, Shield, Activity, ChevronRight, Command, Layers, Share2 } from 'lucide-react';
import { cn } from '../utils/styles';

interface LandingPageProps {
  onStart: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onStart }) => {
  return (
    <div className="min-h-screen bg-white text-black overflow-x-hidden selection:bg-black selection:text-white font-sans">
      <div className="relative z-10 max-w-7xl mx-auto px-6 pt-12 pb-32">
        {/* Navigation */}
        <nav className="flex items-center justify-between mb-24">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-black rounded-xl flex items-center justify-center">
              <Zap size={20} fill="white" className="text-white" />
            </div>
            <span className="text-xl font-black tracking-tighter uppercase">SignSync AI</span>
          </div>
          <button 
             onClick={onStart}
             className="px-8 py-2.5 border border-black rounded-full text-[10px] font-black uppercase tracking-[0.2em] transition-all hover:bg-black hover:text-white"
          >
            Access Terminal
          </button>
        </nav>

        {/* Hero Section */}
        <div className="text-center space-y-12 mb-32 max-w-5xl mx-auto">
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-3 px-4 py-1.5 bg-gray-50 border border-gray-100 rounded-full text-gray-400 text-[9px] font-black uppercase tracking-[0.3em]"
          >
            <Activity size={12} />
            Neural Gesture Orchestration v5.0
          </motion.div>
          
          <div className="space-y-4">
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-6xl md:text-8xl lg:text-9xl font-black tracking-tightest leading-[0.85] uppercase"
            >
              Bridge the <br />
              <span className="text-gray-300">Silence.</span>
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-gray-400 text-sm md:text-lg max-w-2xl mx-auto font-bold uppercase tracking-widest leading-relaxed pt-4"
            >
              Real-time ASL-to-English translation powered by high-fidelity neural tracking and Llama-3 synthesis.
            </motion.p>
          </div>

          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
            className="pt-10 flex flex-col sm:flex-row items-center justify-center gap-6"
          >
            <button 
              onClick={onStart}
              className="group relative px-14 py-6 bg-black text-white rounded-2xl text-xs font-black uppercase tracking-[0.2em] transition-all hover:scale-105 active:scale-95 shadow-2xl flex items-center gap-4"
            >
              Initialize Neural Link
              <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="px-10 py-6 text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 hover:text-black transition-colors">
              Documentation
            </button>
          </motion.div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {[
            { icon: Command, title: 'Neural Precision', desc: 'Millimeter-accurate finger tracking using advanced point-cloud normalization.' },
            { icon: Layers, title: 'Llama-3 Synthesis', desc: 'Context-aware sentence generation that transforms gloss into natural English.' },
            { icon: Share2, title: 'Zero Latency', desc: 'Optimized inference pipeline delivering consistent 60FPS translation speeds.' }
          ].map((feature, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 + (i * 0.1) }}
              className="p-10 bg-white border border-gray-50 rounded-3xl hover:border-black transition-all group flex flex-col items-center text-center"
            >
              <div className="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center text-black mb-8 group-hover:bg-black group-hover:text-white transition-all shadow-sm">
                <feature.icon size={28} />
              </div>
              <h3 className="text-xs font-black uppercase tracking-widest mb-4 text-black">{feature.title}</h3>
              <p className="text-gray-400 leading-loose text-[10px] font-bold uppercase tracking-wider">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Footer Decoration */}
      <div className="py-20 border-t border-gray-50 text-center">
         <p className="text-[9px] font-black text-gray-300 uppercase tracking-[0.5em]">SignSync AI Terminal &copy; 2024</p>
      </div>
    </div>
  );
};

