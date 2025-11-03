/**
 * Category Service
 * Handles all category-related API calls
 */

import api from './api';

export const categoryService = {
  /**
   * Get all categories
   * @returns {Promise} API response with categories array
   */
  async getAllCategories() {
    try {
      const response = await api.get('/categories');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch categories' };
    }
  },

  /**
   * Get category by ID
   * @param {number} id - Category ID
   * @returns {Promise} API response with category data
   */
  async getCategoryById(id) {
    try {
      const response = await api.get(`/categories/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to fetch category' };
    }
  },

  /**
   * Create new category
   * @param {Object} categoryData - Category data
   * @param {string} categoryData.name - Category name
   * @param {string} categoryData.description - Category description
   * @param {boolean} categoryData.is_active - Category active status
   * @returns {Promise} API response with created category
   */
  async createCategory(categoryData) {
    try {
      const response = await api.post('/categories', categoryData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to create category' };
    }
  },

  /**
   * Update existing category
   * @param {number} id - Category ID
   * @param {Object} categoryData - Updated category data
   * @returns {Promise} API response with updated category
   */
  async updateCategory(id, categoryData) {
    try {
      const response = await api.put(`/categories/${id}`, categoryData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to update category' };
    }
  },

  /**
   * Delete category
   * @param {number} id - Category ID
   * @returns {Promise} API response
   */
  async deleteCategory(id) {
    try {
      const response = await api.delete(`/categories/${id}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Failed to delete category' };
    }
  },
};

export default categoryService;
