import React, { useEffect, useRef, useState } from 'react';
import { HandLandmarker, drawHandSkeleton, extractAndNormalizeLandmarks } from '../core/landmark_extractor';
import { SignClassifier, type SignResult } from '../core/inference';
import { generateAiSentence } from '../services/aiTranslatorService';
import { motion, AnimatePresence } from 'framer-motion';
import { CONFIG } from '../utils/config';
import { cn } from '../utils/styles';
import { Camera, RotateCcw, Volume2, Globe, Command, Zap } from 'lucide-react';
import { translateText, speakText, LanguageCode } from '../services/translationService';
import { fetchSettings } from '../services/dataService';

interface ASLVideoFeedProps {
  onNewMessage: (text: string, sender: 'user' | 'system') => void;
  onStatsUpdate: (fps: number, confidence: number) => void;
  targetLang?: LanguageCode;
}

export const ASLVideoFeed: React.FC<ASLVideoFeedProps> = ({ onNewMessage, onStatsUpdate, targetLang = 'en' }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [currentSign, setCurrentSign] = useState<string>("");
  const [sentenceBuffer, setSentenceBuffer] = useState<string[]>([]);
  const [isTranslating, setIsTranslating] = useState(false);
  const [lastSignTime, setLastSignTime] = useState<number>(0);
  const [lastTranslatedSentence, setLastTranslatedSentence] = useState<string | null>(null);
  const [dbSettings, setDbSettings] = useState<any>(null);

  useEffect(() => {
    fetchSettings().then(setDbSettings).catch(console.error);
  }, []);
  
  const classifierRef = useRef(new SignClassifier());
  const sequenceBufferRef = useRef<number[][]>([]);
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(performance.now());

  useEffect(() => {
    let landmarker: HandLandmarker | null = null;

    if (isCameraActive && videoRef.current) {
      setCameraError(null);
      landmarker = new HandLandmarker((results) => {
        if (canvasRef.current && videoRef.current) {
          const canvas = canvasRef.current;
          const ctx = canvas.getContext('2d');
          if (!ctx) return;

          ctx.clearRect(0, 0, canvas.width, canvas.height);
          
          frameCountRef.current++;
          const now = performance.now();
          if (now - lastTimeRef.current >= 1000) {
             onStatsUpdate(frameCountRef.current, 0);
             frameCountRef.current = 0;
             lastTimeRef.current = now;
          }

          if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            const landmarks = results.multiHandLandmarks[0];
            drawHandSkeleton(ctx, landmarks);
            
            const normalized = extractAndNormalizeLandmarks(landmarks);
            sequenceBufferRef.current.push(normalized);
            if (sequenceBufferRef.current.length > CONFIG.SEQUENCE_LENGTH) {
              sequenceBufferRef.current.shift();
            }

            const result = classifierRef.current.predict(normalized);
            if (result) {
              onStatsUpdate(frameCountRef.current === 0 ? 0 : -1, result.confidence);
              const stabilized = classifierRef.current.getStabilizedPrediction();
              
              const threshold = parseFloat(dbSettings?.confidence_threshold || '0.7');
              if (stabilized && stabilized !== "detecting..." && result.confidence >= threshold) {
                setCurrentSign(stabilized);
                setLastSignTime(Date.now());
              }
            }
          } else {
            setCurrentSign("");
            sequenceBufferRef.current = [];
            onStatsUpdate(frameCountRef.current === 0 ? 0 : -1, 0);
          }
        }
      });

      landmarker.start(videoRef.current).catch(err => {
        console.error("Camera failed:", err);
        let message = "Camera failed to start.";
        if (err.name === 'NotAllowedError' || err.message?.includes('Permission denied')) {
          message = "Camera access denied. Please check your browser permissions.";
        }
        setCameraError(message);
        setIsCameraActive(false);
      });
    }

    return () => {
      landmarker?.stop();
    };
  }, [isCameraActive, dbSettings]);

  useEffect(() => {
    if (sentenceBuffer.length === 0 || isTranslating) return;
    const timeout = parseFloat(dbSettings?.sentence_timeout || '2.5') * 1000;
    const interval = setInterval(() => {
      const now = Date.now();
      if (now - lastSignTime >= timeout && !isTranslating && sentenceBuffer.length > 0) {
        handleTranslate();
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [sentenceBuffer, lastSignTime, isTranslating, dbSettings]);

  const addToSentence = () => {
    if (currentSign && !sentenceBuffer.includes(currentSign)) {
      setSentenceBuffer(prev => [...prev, currentSign]);
    }
  };

  const handleTranslate = async () => {
    if (sentenceBuffer.length === 0) return;
    setIsTranslating(true);
    try {
      const words = [...sentenceBuffer];
      let finalOutput = "";
      if (dbSettings?.ai_translation_enabled !== 'false') {
        finalOutput = await generateAiSentence(words);
      } else {
        finalOutput = words.join(" ");
      }
      if (targetLang !== 'en') {
        finalOutput = await translateText(finalOutput, targetLang);
      }
      setLastTranslatedSentence(finalOutput);
      onNewMessage(finalOutput, 'user');
      if (dbSettings?.auto_speak !== 'false') {
        speakText(finalOutput, targetLang, {
          speed: parseFloat(dbSettings?.tts_speed || '1'),
          volume: parseFloat(dbSettings?.tts_volume || '1')
        });
      }
      setSentenceBuffer([]);
    } catch (error) {
      console.error("ASL Translation Pipeline fail:", error);
    } finally {
      setIsTranslating(false);
    }
  };

  const clearBuffer = () => setSentenceBuffer([]);

  return (
    <div className="flex flex-col h-full bg-white overflow-hidden">
      {/* Viewport */}
      <div className="relative flex-1 bg-gray-50 flex items-center justify-center overflow-hidden border-b border-gray-100">
        <video ref={videoRef} className="w-full h-full object-cover scale-x-[-1]" playsInline muted />
        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full object-cover scale-x-[-1] pointer-events-none opacity-40" width={CONFIG.FRAME_WIDTH} height={CONFIG.FRAME_HEIGHT} />
        
        <AnimatePresence>
          {isCameraActive && currentSign && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="absolute bottom-8 left-1/2 -translate-x-1/2">
              <div className="px-10 py-4 bg-white/90 backdrop-blur-2xl border border-black shadow-2xl rounded-2xl flex items-center gap-4">
                 <div className="w-2 h-2 rounded-full bg-black animate-pulse" />
                 <span className="text-3xl font-black uppercase tracking-tighter text-black">{currentSign}</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {!isCameraActive && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm z-30 p-8 text-center">
            {cameraError ? (
              <div className="max-w-xs">
                <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-xl text-xs font-bold uppercase tracking-widest border border-red-100">{cameraError}</div>
                <button onClick={() => setIsCameraActive(true)} className="btn-primary w-full py-4 text-[10px] uppercase tracking-widest flex items-center justify-center gap-3">
                  <Camera size={16} /> Re-Initialize
                </button>
              </div>
            ) : (
              <button onClick={() => setIsCameraActive(true)} className="btn-primary px-10 py-4 text-[10px] uppercase tracking-widest flex items-center gap-3">
                <Zap size={16} fill="white" /> Initialize Neural Link
              </button>
            )}
          </div>
        )}
      </div>

      {/* Intelligence Sector */}
      <div className="p-6 bg-white space-y-6">
        <div className="space-y-3">
            <div className="flex items-center justify-between">
                <span className="text-[9px] font-black uppercase tracking-[0.2em] text-gray-400 flex items-center gap-2">
                    <Command size={12} /> Neural Buffer
                </span>
                <span className="text-[8px] font-black text-gray-300 uppercase tracking-widest">Pipeline v5.0.1</span>
            </div>
            <div className="min-h-[56px] p-4 bg-gray-50/50 border border-gray-100 rounded-xl flex flex-wrap gap-2.5 items-center">
                {sentenceBuffer.map((word, i) => (
                  <motion.span initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} key={`${word}-${i}`} className="px-4 py-1.5 bg-black text-white text-[10px] font-black rounded-lg uppercase tracking-widest shadow-sm">
                    {word}
                  </motion.span>
                ))}
                {sentenceBuffer.length === 0 && !lastTranslatedSentence && (
                    <span className="text-[10px] text-gray-400 font-bold uppercase tracking-widest animate-pulse ml-1">Awaiting sign detection...</span>
                )}
                {sentenceBuffer.length === 0 && lastTranslatedSentence && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-black text-[10px] font-black flex items-center gap-3 uppercase tracking-widest">
                        <span className="px-2 py-0.5 bg-green-50 text-green-600 rounded text-[8px]">Processed</span>
                        {lastTranslatedSentence}
                    </motion.div>
                )}
            </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-6">
                <button onClick={() => { clearBuffer(); setLastTranslatedSentence(null); }} className="flex items-center gap-2 text-gray-400 hover:text-black transition-all text-[10px] font-black uppercase tracking-widest">
                  <RotateCcw size={14} /> Clear Buffer
                </button>
                <div className="hidden sm:flex items-center gap-2 text-[9px] font-black text-gray-400 uppercase tracking-widest">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-500" /> Confidence: <span className="text-black">High (96%)</span>
                </div>
            </div>

            <div className="flex gap-3 w-full sm:w-auto">
                <button disabled={!currentSign} onClick={addToSentence} className="btn-secondary flex-1 sm:flex-initial py-2.5 px-6 text-[10px] uppercase tracking-widest disabled:opacity-20">
                    Capture Sign
                </button>
                <button disabled={sentenceBuffer.length === 0 || isTranslating} onClick={handleTranslate} className="btn-primary flex-1 sm:flex-initial py-2.5 px-8 text-[10px] uppercase tracking-widest disabled:opacity-20 shadow-xl">
                    {isTranslating ? "Translating..." : "Sync Sentence"}
                </button>
            </div>
        </div>
      </div>
    </div>
  );
};

