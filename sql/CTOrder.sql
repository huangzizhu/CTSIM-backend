CREATE TABLE ct_order (
    orderId INTEGER PRIMARY KEY AUTOINCREMENT,
    patientId INTEGER NOT NULL,
    visitId INTEGER NOT NULL,
    ctId INTEGER NOT NULL,
    status INTEGER NOT NULL,             -- 0=待排队, 1=排队中, 2=扫描中, 3=已完成, 4=已取消, 5=过期
    scheduledTime DATETIME NOT NULL,
    queueEnterTime DATETIME,
    startTime DATETIME,
    endTime DATETIME,
    expectedDuration INTEGER,           -- 预计扫描时长，单位：分钟
    actualDuration INTEGER,             -- 实际扫描时长，单位：分钟
    priority INTEGER DEFAULT 0,         -- 0=普通, 1=急诊, 2=VIP
    isEmergency BOOLEAN DEFAULT FALSE,  -- 是否急诊
    notes TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
    canceledAt TIMESTAMP,
    FOREIGN KEY (patientId) REFERENCES patients(pid),
    FOREIGN KEY (visitId) REFERENCES visits(visitId),
    FOREIGN KEY (ctId) REFERENCES ct(ctId)
);