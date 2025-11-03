-- ============================================================================
-- Financial News Classification System (FNCS) - Users Table Setup
-- ============================================================================
-- This script creates the users table for JWT authentication
-- Author: Alexis Alduncin
-- Database: Supabase PostgreSQL
-- ============================================================================

-- Drop table if exists (for clean setup)
DROP TABLE IF EXISTS users CASCADE;

-- Create users table for authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Create trigger function to auto-update updated_at field
CREATE OR REPLACE FUNCTION update_users_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at on UPDATE
CREATE TRIGGER trigger_update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_users_updated_at();

-- ============================================================================
-- Verification queries (commented out, use in setup script)
-- ============================================================================
-- SELECT COUNT(*) as total_users FROM users;
-- SELECT id, email, full_name, is_active, created_at FROM users ORDER BY id;
-- ============================================================================
