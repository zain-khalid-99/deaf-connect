import Database from "better-sqlite3";
import path from "path";

const db = new Database("app.db");

// Initialize tables
db.exec(`
  CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sentence TEXT NOT NULL,
    detected_words TEXT,
    confidence REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_deleted INTEGER DEFAULT 0
  );

  CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
  );

  CREATE TABLE IF NOT EXISTS analytics (
    key TEXT PRIMARY KEY,
    value REAL
  );
`);

// Default settings
const defaultSettings = {
  theme: "dark",
  voice_enabled: "true",
  selected_voice: "default",
  camera_index: "0",
  mic_enabled: "true",
  auto_speak: "true",
  language: "en",
  confidence_threshold: "0.7",
  sentence_timeout: "2.5"
};

const insertSetting = db.prepare("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)");
Object.entries(defaultSettings).forEach(([key, value]) => {
  insertSetting.run(key, value);
});

export default db;
