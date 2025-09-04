-- Create database
CREATE DATABASE IF NOT EXISTS login_system;
USE login_system;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_last_login (last_login)
);

-- Create admin user (password: Admin123!)
INSERT INTO users (name, email, password, is_admin, created_at, last_login) 
VALUES (
    'Administrator', 
    'admin@example.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.G', 
    TRUE, 
    NOW(), 
    NOW()
) ON DUPLICATE KEY UPDATE name=name;

-- Create regular test user (password: Test123!)
INSERT INTO users (name, email, password, is_admin, created_at, last_login) 
VALUES (
    'Test User', 
    'test@example.com', 
    '$2b$12$8K1p/a0dhrxSH4LEWQ7ZAekcaghyzeqrjUuOiIpAWuQQisgHg.Cha', 
    FALSE, 
    NOW(), 
    NOW()
) ON DUPLICATE KEY UPDATE name=name;

CREATE TABLE IF NOT EXISTS contact_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('unread', 'read', 'archived') DEFAULT 'unread'
);