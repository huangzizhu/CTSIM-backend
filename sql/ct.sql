CREATE TABLE IF NOT EXISTS ct (
    ctId        INTEGER PRIMARY KEY AUTOINCREMENT,  -- 主键
    deviceCode TEXT    NOT NULL UNIQUE,           -- 设备编号
    deviceName TEXT    NOT NULL,                  -- 设备名称
    model      TEXT,                              -- 设备型号
    manufacturer TEXT,                            -- 生产厂家
    category   TEXT,                              -- 设备类别（如 64排、128排）
    status     TEXT    NOT NULL DEFAULT '正常',   -- 当前状态：正常/停用/故障等
    location   TEXT    NOT NULL,                  -- 所在位置：如“1楼CT室”
    notes      TEXT,                              -- 备注
    createdAt  DATETIME DEFAULT (datetime('now','localtime')), -- 创建时间
    updatedAt  DATETIME DEFAULT (datetime('now','localtime'))  -- 更新时间（应用层更新）
);