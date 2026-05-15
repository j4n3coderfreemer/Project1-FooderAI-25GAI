-- ============================================================
-- FOODER AI — DATABASE SCHEMA
-- SQL Server / SSMS
-- Chạy toàn bộ file này 1 lần để tạo database và 8 bảng
-- ============================================================

-- BƯỚC 1: Tạo database (bỏ qua nếu đã có)
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'FooderAI')
    CREATE DATABASE FooderAI;
GO

USE FooderAI;
GO

-- ============================================================
-- NHÓM 1: NGƯỜI DÙNG & XÁC THỰC
-- ============================================================

-- Bảng tài khoản đăng nhập
CREATE TABLE USERS (
    user_id     INT IDENTITY(1,1) PRIMARY KEY,
    username    NVARCHAR(50)  NOT NULL UNIQUE,
    email       NVARCHAR(100) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,       -- bcrypt hash, không lưu mật khẩu thật
    created_at  DATETIME      DEFAULT GETDATE(),
    is_active   BIT           DEFAULT 1         -- 0 = bị khóa tài khoản
);
GO

-- Bảng thông tin cơ thể (1-1 với USERS)
CREATE TABLE USER_PROFILES (
    profile_id     INT IDENTITY(1,1) PRIMARY KEY,
    user_id        INT           NOT NULL UNIQUE,   -- UNIQUE = đảm bảo 1-1
    weight_kg      FLOAT,                           -- cân nặng (kg)
    height_cm      FLOAT,                           -- chiều cao (cm)
    age            INT,
    gender         NVARCHAR(10)  CHECK (gender IN ('male', 'female', 'other')),
    activity_level NVARCHAR(20)  CHECK (activity_level IN (
                       'sedentary',      -- ít vận động (x1.2)
                       'light',          -- nhẹ 1-3 ngày/tuần (x1.375)
                       'moderate',       -- vừa 3-5 ngày/tuần (x1.55)
                       'active',         -- nhiều 6-7 ngày/tuần (x1.725)
                       'very_active'     -- rất nhiều / VĐV (x1.9)
                   )),
    goal           NVARCHAR(20)  CHECK (goal IN ('lose', 'maintain', 'gain')),
    updated_at     DATETIME      DEFAULT GETDATE(),

    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
);
GO

-- ============================================================
-- NHÓM 2: THỰC PHẨM & DINH DƯỠNG
-- ============================================================

-- Bảng thực phẩm (hệ thống + user tự thêm)
CREATE TABLE FOODS (
    food_id          INT IDENTITY(1,1) PRIMARY KEY,
    food_name        NVARCHAR(150) NOT NULL,
    category         NVARCHAR(50),               -- "Rau củ", "Thịt", "Hải sản"...
    calories_per100g FLOAT         NOT NULL,
    protein_g        FLOAT         DEFAULT 0,
    carbs_g          FLOAT         DEFAULT 0,
    fat_g            FLOAT         DEFAULT 0,
    fiber_g          FLOAT         DEFAULT 0,
    image_path       NVARCHAR(255),              -- đường dẫn ảnh (từ page_scan)
    is_custom        BIT           DEFAULT 0,    -- 0=hệ thống, 1=user tự thêm
    created_by       INT,                        -- NULL nếu là món hệ thống

    FOREIGN KEY (created_by) REFERENCES USERS(user_id) ON DELETE SET NULL
);
GO

-- ============================================================
-- NHÓM 3: NHẬT KÝ & THEO DÕI
-- ============================================================

-- Nhật ký ăn uống từng bữa
CREATE TABLE FOOD_LOGS (
    log_id     INT IDENTITY(1,1) PRIMARY KEY,
    user_id    INT          NOT NULL,
    food_id    INT          NOT NULL,
    quantity_g FLOAT        NOT NULL,            -- số gram ăn thực tế
    meal_type  NVARCHAR(10) CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    log_date   DATE         DEFAULT CAST(GETDATE() AS DATE),
    logged_at  DATETIME     DEFAULT GETDATE(),

    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES FOODS(food_id)
);
GO

-- Nhật ký tập luyện
CREATE TABLE EXERCISE_LOGS (
    ex_log_id      INT IDENTITY(1,1) PRIMARY KEY,
    user_id        INT           NOT NULL,
    exercise_name  NVARCHAR(100) NOT NULL,       -- "Chạy bộ", "Đạp xe"...
    duration_min   INT           NOT NULL,        -- số phút tập
    calories_burned FLOAT,                        -- calo đốt (tính từ MET hoặc AI)
    log_date       DATE          DEFAULT CAST(GETDATE() AS DATE),
    logged_at      DATETIME      DEFAULT GETDATE(),

    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
);
GO

-- Tổng hợp mỗi ngày — feed vào 4 StatCard trên dashboard
CREATE TABLE DAILY_SUMMARIES (
    summary_id         INT IDENTITY(1,1) PRIMARY KEY,
    user_id            INT   NOT NULL,
    summary_date       DATE  NOT NULL,
    total_calories_in  FLOAT DEFAULT 0,   -- tổng calo nạp vào
    total_calories_out FLOAT DEFAULT 0,   -- tổng calo đốt (tập luyện)
    bmi                FLOAT,             -- tính từ fooder_widgetBack.calculate_bmi()
    bmr                FLOAT,             -- tính từ fooder_widgetBack.calculate_bmr()
    tdee               FLOAT,             -- tính từ fooder_widgetBack.calculate_tdee()
    goal_calories      INT,               -- mục tiêu calo ngày hôm đó

    UNIQUE (user_id, summary_date),       -- mỗi user chỉ có 1 bản ghi/ngày
    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
);
GO

-- ============================================================
-- NHÓM 4: AI & CHAT (tích hợp với page_ai.py)
-- ============================================================

-- Phiên chat (1 user - nhiều phiên)
CREATE TABLE CHAT_SESSIONS (
    session_id  INT IDENTITY(1,1) PRIMARY KEY,
    user_id     INT      NOT NULL,
    started_at  DATETIME DEFAULT GETDATE(),
    msg_count   INT      DEFAULT 0,       -- đếm để so với NSFWGuard.MAX_MSGS = 45
    is_active   BIT      DEFAULT 1        -- 0 = phiên đã đóng / hết quota
);
GO

-- Từng tin nhắn trong phiên chat
CREATE TABLE CHAT_MESSAGES (
    msg_id      INT IDENTITY(1,1) PRIMARY KEY,
    session_id  INT           NOT NULL,
    role        NVARCHAR(10)  NOT NULL CHECK (role IN ('user', 'assistant')),
    content     NVARCHAR(MAX) NOT NULL,
    sent_at     DATETIME      DEFAULT GETDATE(),
    is_nsfw     BIT           DEFAULT 0   -- NSFWGuard đánh dấu nếu vi phạm

    FOREIGN KEY (session_id) REFERENCES CHAT_SESSIONS(session_id) ON DELETE CASCADE
);
GO

-- ============================================================
-- INDEX — tăng tốc truy vấn thường dùng
-- ============================================================

-- Lọc nhật ký ăn theo ngày (dùng nhiều nhất trên dashboard)
CREATE INDEX IX_FoodLogs_UserDate
    ON FOOD_LOGS (user_id, log_date);

-- Lọc tổng hợp theo ngày
CREATE INDEX IX_DailySummaries_UserDate
    ON DAILY_SUMMARIES (user_id, summary_date);

-- Lọc tin nhắn theo phiên
CREATE INDEX IX_ChatMessages_Session
    ON CHAT_MESSAGES (session_id, sent_at);
GO

-- ============================================================
-- DỮ LIỆU MẪU — xóa phần này trước khi demo thật
-- ============================================================

-- 1 user mẫu (password: "test123" — đây chỉ là placeholder, thực tế phải hash)
INSERT INTO USERS (username, email, password_hash)
VALUES (N'gritalyst_test', N'test@fooderai.vn', N'$2b$12$placeholder_hash');

-- Profile mẫu: nam 20 tuổi, 65kg, 170cm, vận động vừa, mục tiêu duy trì
INSERT INTO USER_PROFILES (user_id, weight_kg, height_cm, age, gender, activity_level, goal)
VALUES (1, 65.0, 170.0, 20, N'male', N'moderate', N'maintain');

-- Một số món ăn hệ thống mẫu
INSERT INTO FOODS (food_name, category, calories_per100g, protein_g, carbs_g, fat_g, fiber_g)
VALUES
    (N'Cơm trắng',      N'Tinh bột',  130, 2.7, 28.6, 0.3, 0.4),
    (N'Ức gà luộc',     N'Thịt',      165, 31.0,  0.0, 3.6, 0.0),
    (N'Rau muống xào',  N'Rau củ',     19, 2.6,   1.8, 0.2, 2.1),
    (N'Trứng gà luộc',  N'Trứng',     155, 13.0,  1.1,11.0, 0.0),
    (N'Chuối',          N'Trái cây',   89, 1.1,  23.0, 0.3, 2.6),
    (N'Phở bò',         N'Món nước',  215, 14.0,  25.0, 6.0, 0.8);
GO

PRINT N'FooderAI database tạo thành công! Kiểm tra Object Explorer bên trái.';
GO