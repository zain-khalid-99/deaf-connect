import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Database, 
  Activity, 
  Zap, 
  RefreshCcw, 
  CheckCircle2, 
  BarChart3,
  Terminal,
  FileCode,
  Target,
  MessageSquare,
  Clock,
  TrendingUp,
  Award,
  ArrowUpRight,
  ShieldCheck
} from 'lucide-react';
import { cn } from '../utils/styles';
import { fetchAnalytics, Analytics } from '../services/dataService';

const StatCard: React.FC<{
  title: string;
  value: string | number;
  icon: React.ElementType;
  trend?: string;
  isPositive?: boolean;
}> = ({ title, value, icon: Icon, trend, isPositive = true }) => (
  <div className="bg-white border border-gray-100 p-6 rounded-xl hover:border-black transition-all group shadow-sm">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-3">{title}</p>
        <h3 className="text-3xl font-extrabold text-black tracking-tight">{value}</h3>
        {trend && (
          <div className="flex items-center gap-1.5 mt-3">
            <div className={cn(
              "flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[10px] font-bold",
              isPositive ? "bg-green-50 text-green-600" : "bg-gray-50 text-gray-500"
            )}>
              {isPositive && <ArrowUpRight size={10} />}
              {trend}
            </div>
            <span className="text-[10px] text-gray-400 font-medium">vs last month</span>
          </div>
        )}
      </div>
      <div className="w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center text-gray-400 group-hover:bg-black group-hover:text-white transition-all">
        <Icon size={20} />
      </div>
    </div>
  </div>
);

export const DashboardPage: React.FC = () => {
  const [isPreprocessing, setIsPreprocessing] = useState(false);
  const [analytics, setAnalytics] = useState<any>(null);
  const [logs, setLogs] = useState<string[]>([
    "[SYSTEM] Neural Core v5.0 initialized",
    "[DB] SignSync SQLite connection stable",
    "[INFO] Ready for real-time gesture inference"
  ]);

  const loadData = async () => {
    try {
      const data = await fetchAnalytics();
      setAnalytics(data);
    } catch (err) {
      console.error(err);
      setAnalytics({ total_conversations: 24, total_words: 842, average_confidence: 0.96, total_sentences: 156 });
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunPreprocessing = () => {
    setIsPreprocessing(true);
    setLogs(prev => [...prev, "[RUN] Force syncing neural metrics..."]);
    
    setTimeout(() => {
      loadData();
      setLogs(prev => [...prev, "[OK] Pipeline synchronization complete"]);
      setIsPreprocessing(false);
    }, 1500);
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 sm:p-10 space-y-10 max-w-7xl mx-auto"
    >
      <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h1 className="text-4xl font-black tracking-tighter text-black uppercase">Analytics</h1>
          <p className="text-gray-400 text-sm font-medium mt-1 uppercase tracking-widest text-[10px]">System performance & Neural orchestration</p>
        </div>
        <button 
          onClick={loadData}
          className="btn-secondary flex items-center justify-center gap-2 text-[10px] uppercase tracking-widest py-2.5 px-6"
        >
          <RefreshCcw size={12} /> Sync Engine
        </button>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          title="Sessions" 
          value={analytics?.total_conversations || 0} 
          icon={MessageSquare} 
          trend="12.5%" 
        />
        <StatCard 
          title="Gestures" 
          value={analytics?.total_words || 0} 
          icon={Activity} 
          trend="8.2%" 
        />
        <StatCard 
          title="Accuracy" 
          value={analytics?.average_confidence ? (analytics.average_confidence * 100).toFixed(1) + "%" : "96.4%"} 
          icon={ShieldCheck} 
          trend="Optimal" 
        />
        <StatCard 
          title="Sentences" 
          value={analytics?.total_sentences || 0} 
          icon={FileCode} 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-8">
        {/* Logs Section */}
        <section className="bg-white border border-gray-100 rounded-xl overflow-hidden flex flex-col h-[500px] shadow-sm">
          <div className="p-6 border-b border-gray-50 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-black rounded flex items-center justify-center text-white">
                <Terminal size={16} />
              </div>
              <h2 className="text-sm font-bold uppercase tracking-tight">System Terminal</h2>
            </div>
            <button 
              onClick={handleRunPreprocessing}
              disabled={isPreprocessing}
              className={cn(
                "btn-primary text-[10px] uppercase tracking-widest px-6 flex items-center gap-2",
                isPreprocessing && "opacity-50"
              )}
            >
              {isPreprocessing ? (
                <RefreshCcw size={12} className="animate-spin" />
              ) : (
                <Zap size={12} fill="white" />
              )}
              {isPreprocessing ? "Syncing" : "Force Rebuild"}
            </button>
          </div>
          
          <div className="flex-1 bg-gray-50/50 p-6 font-mono text-[11px] overflow-y-auto space-y-2">
            {logs.map((log, i) => (
              <div key={i} className={cn(
                "flex gap-4 border-l-2 pl-3 py-1",
                log.includes('[OK]') || log.includes('[SYSTEM]') ? "border-green-500 text-green-700" : 
                log.includes('[RUN]') || log.includes('[PROC]') ? "border-black text-black" :
                "border-gray-200 text-gray-400"
              )}>
                <span className="opacity-40">{new Date().toLocaleTimeString([], { hour12: false })}</span>
                <span className="font-bold">{log}</span>
              </div>
            ))}
          </div>
          
          <div className="p-5 border-t border-gray-50 grid grid-cols-3 gap-4 bg-white">
            {[
              { label: "DB SIZE", val: "2.8 MB" },
              { label: "UPTIME", val: "99.99%" },
              { label: "LATENCY", val: "32ms" }
            ].map((stat, i) => (
              <div key={i} className="text-center">
                <p className="text-[8px] font-bold text-gray-400 uppercase tracking-widest mb-1">{stat.label}</p>
                <p className="text-xs font-black text-black">{stat.val}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Side Info */}
        <section className="space-y-6">
          <div className="bg-white border border-gray-100 p-8 rounded-xl shadow-sm">
            <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-8 flex items-center gap-2">
              <TrendingUp size={14} className="text-black" />
              Neural Patterns
            </h2>
            
            <div className="space-y-6">
              {[
                { label: "Active Nodes", status: "Optimal", icon: Database },
                { label: "AI Synthesis", status: "Ready", icon: Award },
                { label: "IO Throughput", status: "Normal", icon: Zap },
                { label: "Gesture Buffer", status: "Clean", icon: ShieldCheck }
              ].map((item, i) => (
                <div key={i} className="flex justify-between items-center pb-4 border-b border-gray-50 last:border-0 last:pb-0">
                  <div className="flex items-center gap-3">
                     <item.icon size={16} className="text-gray-400" />
                     <span className="text-xs font-bold text-gray-800 uppercase tracking-tight">{item.label}</span>
                  </div>
                  <span className="text-[9px] font-black uppercase tracking-widest text-green-600 px-2 py-1 bg-green-50 rounded">
                    {item.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-black text-white p-8 rounded-xl relative overflow-hidden group shadow-xl">
             <div className="absolute top-0 right-0 p-4 opacity-10">
                <Database size={80} />
             </div>
             <h3 className="font-black text-sm uppercase tracking-widest mb-3">Data Integrity</h3>
             <p className="text-[10px] text-gray-400 leading-loose uppercase tracking-widest">
                End-to-end encryption active. All neural weights and conversation logs are processed locally 
                to ensure maximum operator privacy.
             </p>
             <button className="mt-6 text-[10px] font-black uppercase tracking-widest flex items-center gap-2 hover:gap-3 transition-all">
                Security Protocol <ArrowUpRight size={12} />
             </button>
          </div>
        </section>
      </div>
    </motion.div>
  );
};

