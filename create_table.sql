-- ============================================================================
-- Financial News Classification System (FNCS) - Categories Table Setup
-- ============================================================================
-- This script creates the categories table with proper indexes and sample data
-- Author: Alexis Alduncin
-- Database: Supabase PostgreSQL
-- ============================================================================

-- Drop table if exists (for clean setup)
DROP TABLE IF EXISTS categories CASCADE;

-- Create categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX idx_categories_name ON categories(name);
CREATE INDEX idx_categories_is_active ON categories(is_active);

-- Create trigger function to auto-update updated_at field
CREATE OR REPLACE FUNCTION update_categories_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at on UPDATE
CREATE TRIGGER trigger_update_categories_updated_at
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_categories_updated_at();

-- Insert sample data for testing
INSERT INTO categories (name, description, is_active) VALUES
    ('Market Analysis', 'News related to market trends and financial analysis', true),
    ('Earnings Reports', 'Company earnings and financial results', true),
    ('Economic Indicators', 'Economic data and indicators', true),
    ('Mergers & Acquisitions', 'M&A news and updates', true),
    ('Cryptocurrency', 'Digital currency and blockchain news', true),
    ('Stock Market', 'Stock market movements and analysis', true),
    ('Banking', 'Banking sector news and regulations', true),
    ('Real Estate', 'Property market and real estate investment news', true),
    ('Commodities', 'Oil, gold, and other commodity markets', true),
    ('IPO News', 'Initial public offerings and new listings', true);

-- ============================================================================
-- Verification queries (commented out, use in setup_db.py)
-- ============================================================================
-- SELECT COUNT(*) as total_categories FROM categories;
-- SELECT * FROM categories WHERE is_active = true ORDER BY id;
-- ============================================================================
