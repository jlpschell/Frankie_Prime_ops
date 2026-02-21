-- ============================================
-- SHARED BRAIN SCHEMA — Prime + VC via Supabase
-- Run this in Supabase SQL Editor (one time)
-- ============================================

-- 1. Shared Files — all .md, .py, .js files live here
CREATE TABLE IF NOT EXISTS shared_files (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  file_path text NOT NULL UNIQUE,
  content text NOT NULL,
  tags text[] DEFAULT '{}',
  updated_by text NOT NULL,
  version int DEFAULT 1,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE shared_files ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for service role" ON shared_files FOR ALL USING (true);
ALTER PUBLICATION supabase_realtime ADD TABLE shared_files;

-- 2. Sync Log — append-only audit trail (who did what, when)
CREATE TABLE IF NOT EXISTS sync_log (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  agent text NOT NULL,
  action text NOT NULL,
  file_path text,
  summary text NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE sync_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for service role" ON sync_log FOR ALL USING (true);
ALTER PUBLICATION supabase_realtime ADD TABLE sync_log;

-- 3. Skills — reusable scripts/capabilities both agents can use
CREATE TABLE IF NOT EXISTS skills (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL UNIQUE,
  description text,
  code text NOT NULL,
  language text DEFAULT 'bash',
  created_by text NOT NULL,
  version int DEFAULT 1,
  tags text[] DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE skills ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for service role" ON skills FOR ALL USING (true);
ALTER PUBLICATION supabase_realtime ADD TABLE skills;
