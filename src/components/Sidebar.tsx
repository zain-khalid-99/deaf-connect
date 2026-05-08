import React, { useState, useEffect } from 'react';
import { 
  Home, 
  MessageSquare, 
  History, 
  BookOpen, 
  Settings, 
  FileText,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Zap,
  ExternalLink,
  Shield
} from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '../utils/styles';
import { fetchHistory, Conversation } from '../services/dataService';

interface SidebarProps {
  activePage: string;
  onNavigate: (page: string) => void;
  isCollapsed: boolean;
  setIsCollapsed: (collapsed: boolean) => void;
  isMobile?: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  activePage, 
  onNavigate, 
  isCollapsed, 
  setIsCollapsed,
  isMobile = false
}) => {
  const [recentChats, setRecentChats] = useState<Conversation[]>([]);

  useEffect(() => {
    const loadRecent = async () => {
      try {
        const data = await fetchHistory();
        setRecentChats(data || []);
      } catch (err) {
        console.error("Failed to fetch history:", err);
      }
    };
    loadRecent();
    const interval = setInterval(loadRecent, 30000);
    return () => clearInterval(interval);
  }, [activePage]);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'communication', label: 'Live Translation', icon: Zap },
    { id: 'history', label: 'History', icon: History },
    { id: 'references', label: 'ASL Dictionary', icon: BookOpen },
    { id: 'documentation', label: 'Resources', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const sidebarWidth = isMobile ? '100%' : (isCollapsed ? '80px' : '260px');

  return (
    <motion.div 
      initial={false}
      animate={{ width: sidebarWidth }}
      className={cn(
        "h-screen bg-white border-r border-gray-100 flex flex-col relative z-50 transition-all duration-300 ease-in-out shadow-sm",
        isMobile ? "w-full" : ""
      )}
    >
      {/* Logo Area */}
      {!isMobile && (
        <div className={cn(
          "pt-8 pb-10 flex items-center gap-3",
          isCollapsed ? "justify-center px-0" : "px-6"
        )}>
          <div className="w-10 h-10 bg-black rounded-xl flex items-center justify-center font-bold text-white flex-shrink-0 shadow-lg shadow-black/10">
            <Shield size={20} fill="white" />
          </div>
          {!isCollapsed && (
            <motion.div 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex flex-col"
            >
              <span className="font-extrabold text-lg tracking-tight leading-none">SignSync</span>
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mt-0.5">Neural AI</span>
            </motion.div>
          )}
        </div>
      )}

      {/* Navigation */}
      <nav className={cn(
        "flex-1 space-y-1.5",
        isCollapsed && !isMobile ? "px-3" : "px-4"
      )}>
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={cn(
              "w-full flex items-center gap-3 px-3 py-3 rounded-lg font-semibold text-sm transition-all group overflow-hidden whitespace-nowrap",
              activePage === item.id 
                ? "bg-gray-100 text-black" 
                : "text-gray-500 hover:bg-gray-50 hover:text-black"
            )}
          >
            <item.icon size={20} className={cn(
              "flex-shrink-0",
              activePage === item.id ? "text-black" : "opacity-70 group-hover:opacity-100"
            )} />
            {(!isCollapsed || isMobile) && (
              <motion.span 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }}
                className="flex-1 text-left"
              >
                {item.label}
              </motion.span>
            )}
          </button>
        ))}

        {(!isCollapsed || isMobile) && recentChats.length > 0 && (
          <div className="mt-8 pt-6 border-t border-gray-100 space-y-4 px-2">
            <h4 className="text-[10px] font-bold uppercase tracking-widest text-gray-400 px-1">Recent Activity</h4>
            <div className="space-y-1 max-h-[200px] overflow-y-auto sidebar-scroll">
              {recentChats.slice(0, 5).map(chat => (
                <button 
                  key={chat.id}
                  onClick={() => onNavigate('history')}
                  className="w-full flex items-center gap-2 px-2 py-2 rounded-md text-left group hover:bg-gray-50 transition-colors"
                >
                  <MessageSquare size={14} className="text-gray-400 flex-shrink-0 group-hover:text-black transition-colors" />
                  <span className="text-xs text-gray-500 truncate group-hover:text-black transition-colors">{chat.sentence}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </nav>

      {/* User Section */}
      <div className={cn(
        "p-4 border-t border-gray-100 bg-gray-50/50",
        isCollapsed && !isMobile ? "flex justify-center" : ""
      )}>
        <div className={cn(
          "flex items-center gap-3 p-2 rounded-xl",
          isCollapsed && !isMobile ? "justify-center" : ""
        )}>
          <div className="w-9 h-9 rounded-full bg-white border border-gray-200 flex items-center justify-center text-xs font-bold text-black flex-shrink-0 shadow-sm uppercase">
            ZK
          </div>
          {(!isCollapsed || isMobile) && (
            <div className="flex-1 min-w-0">
              <p className="text-xs font-bold truncate text-black uppercase tracking-tight">Zain Khalid</p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                <p className="text-[9px] text-gray-500 truncate font-bold uppercase tracking-widest">Active Operator</p>
              </div>
            </div>
          )}
          {(!isCollapsed || isMobile) && (
            <button className="p-1.5 text-gray-400 hover:text-black hover:bg-white rounded-lg transition-all shadow-sm border border-transparent hover:border-gray-100">
               <LogOut size={16} />
            </button>
          )}
        </div>
      </div>

      {/* Collapse Toggle */}
      {!isMobile && (
        <button 
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="absolute -right-3 top-24 w-6 h-6 bg-white rounded-full border border-gray-200 flex items-center justify-center text-gray-400 cursor-pointer z-[60] hover:text-black hover:border-gray-400 hover:scale-110 transition-all shadow-sm"
        >
          {isCollapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
        </button>
      )}
    </motion.div>
  );
};

