-- ########################################################
-- DEAF CONNECT: SUPABASE POSTGRESQL SCHEMA
-- ########################################################
-- Paste this into the Supabase SQL Editor (https://supabase.com/dashboard/project/_/sql)
-- and click "RUN".

-- 1. Users Table (Syncs with Supabase Auth or managed manually)
CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Conversations Table
CREATE TABLE IF NOT EXISTS public.conversations (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES public.users(id) ON DELETE CASCADE,
    title TEXT DEFAULT 'New Conversation',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Messages Table
CREATE TABLE IF NOT EXISTS public.messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES public.conversations(id) ON DELETE CASCADE,
    sender TEXT NOT NULL, -- 'user' or 'ai'
    raw_words TEXT, -- ASL Gloss signals
    translated_sentence TEXT, -- Final English sentence
    confidence FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. User Settings Table
CREATE TABLE IF NOT EXISTS public.settings (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE REFERENCES public.users(id) ON DELETE CASCADE,
    theme TEXT DEFAULT 'dark',
    speech_rate FLOAT DEFAULT 1.0,
    speech_volume FLOAT DEFAULT 1.0,
    auto_speak BOOLEAN DEFAULT TRUE,
    camera_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Analytics Table
CREATE TABLE IF NOT EXISTS public.analytics (
    id SERIAL PRIMARY KEY,
    user_id TEXT REFERENCES public.users(id) ON DELETE CASCADE,
    total_words INTEGER DEFAULT 0,
    avg_confidence FLOAT DEFAULT 0.0,
    session_duration INTEGER DEFAULT 0, -- in seconds
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ########################################################
-- ROW LEVEL SECURITY (RLS) - Optional but recommended
-- ########################################################

-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics ENABLE ROW LEVEL SECURITY;

-- Basic policy: Users can only access their own data
-- Note: Replace 'auth.uid()' with 'id' if using custom auth strings
-- CREATE POLICY "Users can view own data" ON public.users FOR SELECT USING (true);

-- ########################################################
-- INDEXES FOR PERFORMANCE
-- ########################################################
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON public.conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON public.messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON public.analytics(user_id);
