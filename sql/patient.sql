CREATE TABLE patients (
    userId                  INTEGER PRIMARY KEY AUTOINCREMENT,   -- 内部自增主键
    cardNo                  TEXT NOT NULL UNIQUE,                -- 就诊卡号 / 病历号
    name                    TEXT NOT NULL,                       -- 姓名
    gender                  TEXT NOT NULL,                       -- 性别（M/F/O）
    birthDate               TEXT NOT NULL,                       -- 出生日期：YYYY-MM-DD
    phone                   TEXT,                                 -- 联系方式
    idNumber                TEXT UNIQUE,                          -- 身份证号
    address                 TEXT,                                 -- 地址

    emergencyContactName    TEXT,                                 -- 紧急联系人姓名
    emergencyContactPhone   TEXT,                                 -- 紧急联系人电话

    createdTime             TEXT DEFAULT (datetime('now')) ,      -- 创建时间
    updatedTime             TEXT DEFAULT (datetime('now'))                      -- 更新时间
);