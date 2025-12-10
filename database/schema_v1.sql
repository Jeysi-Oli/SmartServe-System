-- Project: SmartServe (Database Schema)
-- Description: Database Schema for Barangay Document Management System (3NF Compliant Structure)

-- Enable Foreign Key support for SQLite
PRAGMA foreign_keys = ON;

-- ==========================================
-- 1. USER TABLE
-- Stores profile info for Residents and Admins
-- ==========================================
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'resident', -- 'resident' or 'admin'
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 2. REQUEST TABLE
-- Tracks document transactions linked to Users
-- ==========================================
CREATE TABLE IF NOT EXISTS request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    admin_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Key: Links Request to User (One-to-Many)
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);