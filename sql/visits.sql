-- 确保 SQLite 外键生效
PRAGMA foreign_keys = ON;

CREATE TABLE visits (
    visitId       INTEGER PRIMARY KEY AUTOINCREMENT,   -- 就诊记录主键
    patientId     INTEGER NOT NULL,                    -- 患者ID，外键 -> patients.userId
    doctorId      INTEGER NOT NULL,                    -- 医生ID，外键 -> users.userId

    visitTime     TEXT    NOT NULL,                    -- 就诊时间：YYYY-MM-DD HH:MM:SS
    isEmergency   INTEGER NOT NULL DEFAULT 0,          -- 是否急诊：0/1
    symptoms      TEXT    NOT NULL,                    -- 症状描述

    department    TEXT,                                -- 科室
    diagnosis     TEXT,                                -- 诊断结果
    triageLevel   INTEGER,                             -- 分级（1-4之类的）
    status        TEXT    NOT NULL DEFAULT 'ongoing',  -- 就诊状态：ongoing/finished/canceled

    createdTime   TEXT    NOT NULL DEFAULT (datetime('now')), -- 创建时间
    updatedTime   TEXT,                                        -- 更新时间

    FOREIGN KEY (patientId) REFERENCES patients(pid),
    FOREIGN KEY (doctorId)  REFERENCES user(uid)
);