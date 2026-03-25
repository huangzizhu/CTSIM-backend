-- user.sql
CREATE TABLE IF NOT EXISTS user (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hashedPassword TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 0 CHECK(level >= 0 AND level <= 2)
);