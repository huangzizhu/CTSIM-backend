CREATE TABLE IF NOT EXISTS refresh_tokens (
                                              id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 主键
                                              userId INTEGER NOT NULL,              -- 用户ID
                                              refreshToken TEXT NOT NULL,           -- refresh token
                                              ipAddress TEXT,                       -- 可选：生成时的IP
                                              createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP  -- 创建时间
);

-- 如果一个用户可能有多个 token，且你会按 user_id 查，建议加索引：
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_userId
    ON refresh_tokens(userId);