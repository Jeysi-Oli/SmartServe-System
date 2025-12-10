-- schema_v1.sql
-- Project: SmartServe
-- Description: Initial database schema (3NF Compliant)

-- Enable Foreign Key support for SQLite
PRAGMA foreign_keys = ON;

-- 1. USERS TABLE (Stores Residents and Admins)
-- Stores login credentials and profile information
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'resident', -- Values: 'resident' or 'admin'
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. REQUESTS TABLE (Transactions)
-- Tracks document requests linked to a specific user
CREATE TABLE request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending', -- Values: 'pending', 'approved', 'rejected', 'completed'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    admin_notes TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);