/**
 * Categories Page Component
 * Complete CRUD interface for managing categories with search, filter, and toast notifications
 */

import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { categoryService } from '../services/categoryService';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/LoadingSpinner';

const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);
  const [filteredCategories, setFilteredCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // Search and filter states
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('all'); // 'all', 'active', 'inactive'

  // Modal states
  const [showModal, setShowModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [viewingCategory, setViewingCategory] = useState(null);

  // Form state with validation
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    is_active: true,
  });
  const [formErrors, setFormErrors] = useState({});

  const { user } = useAuth();

  // Load categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Filter categories when search query or filter status changes
  useEffect(() => {
    filterCategories();
  }, [categories, searchQuery, filterStatus]);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const result = await categoryService.getAllCategories();
      if (result.success) {
        setCategories(result.data);
      } else {
        toast.error('Failed to load categories');
      }
    } catch (err) {
      toast.error(err.error || 'Failed to load categories');
    } finally {
      setLoading(false);
    }
  };

  const filterCategories = () => {
    let filtered = [...categories];

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (cat) =>
          cat.name.toLowerCase().includes(query) ||
          (cat.description && cat.description.toLowerCase().includes(query))
      );
    }

    // Apply status filter
    if (filterStatus === 'active') {
      filtered = filtered.filter((cat) => cat.is_active);
    } else if (filterStatus === 'inactive') {
      filtered = filtered.filter((cat) => !cat.is_active);
    }

    setFilteredCategories(filtered);
  };

  const validateForm = () => {
    const errors = {};

    if (!formData.name.trim()) {
      errors.name = 'Category name is required';
    } else if (formData.name.trim().length < 3) {
      errors.name = 'Category name must be at least 3 characters';
    } else if (formData.name.trim().length > 50) {
      errors.name = 'Category name must not exceed 50 characters';
    }

    if (formData.description && formData.description.length > 200) {
      errors.description = 'Description must not exceed 200 characters';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
    // Clear error for this field
    if (formErrors[name]) {
      setFormErrors({ ...formErrors, [name]: '' });
    }
  };

  const openCreateModal = () => {
    setEditingCategory(null);
    setFormData({ name: '', description: '', is_active: true });
    setFormErrors({});
    setShowModal(true);
  };

  const openEditModal = (category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name,
      description: category.description || '',
      is_active: category.is_active,
    });
    setFormErrors({});
    setShowModal(true);
  };

  const openDetailsModal = (category) => {
    setViewingCategory(category);
    setShowDetailsModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingCategory(null);
    setFormData({ name: '', description: '', is_active: true });
    setFormErrors({});
  };

  const closeDetailsModal = () => {
    setShowDetailsModal(false);
    setViewingCategory(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form
    if (!validateForm()) {
      toast.error('Please fix the errors in the form');
      return;
    }

    setSubmitting(true);

    try {
      if (editingCategory) {
        // Update existing category
        const result = await categoryService.updateCategory(editingCategory.id, formData);
        if (result.success) {
          toast.success('Category updated successfully!');
          fetchCategories();
          closeModal();
        } else {
          toast.error(result.error || 'Failed to update category');
        }
      } else {
        // Create new category
        const result = await categoryService.createCategory(formData);
        if (result.success) {
          toast.success('Category created successfully!');
          fetchCategories();
          closeModal();
        } else {
          toast.error(result.error || 'Failed to create category');
        }
      }
    } catch (err) {
      toast.error(err.error || 'An error occurred');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"?`)) {
      return;
    }

    const deleteToast = toast.loading('Deleting category...');

    try {
      const result = await categoryService.deleteCategory(id);
      if (result.success) {
        toast.success('Category deleted successfully!', { id: deleteToast });
        fetchCategories();
      } else {
        toast.error(result.error || 'Failed to delete category', { id: deleteToast });
      }
    } catch (err) {
      toast.error(err.error || 'Failed to delete category', { id: deleteToast });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoadingSpinner text="Loading categories..." />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="md:flex md:items-center md:justify-between">
            <div className="flex-1 min-w-0">
              <h1 className="text-3xl font-bold text-gray-900">Categories Management</h1>
              <p className="mt-1 text-sm text-gray-500">
                Manage financial news categories for the FNCS system
              </p>
            </div>
            <div className="mt-4 flex md:mt-0 md:ml-4">
              <button onClick={openCreateModal} className="btn-primary">
                <svg className="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Category
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filter Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="bg-white p-4 rounded-lg shadow space-y-4 sm:space-y-0 sm:flex sm:items-center sm:space-x-4">
          {/* Search Input */}
          <div className="flex-1">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="text"
                placeholder="Search categories..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>

          {/* Status Filter */}
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-700">Status:</label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="block w-full sm:w-auto pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="all">All</option>
              <option value="active">Active Only</option>
              <option value="inactive">Inactive Only</option>
            </select>
          </div>

          {/* Results Count */}
          <div className="text-sm text-gray-500">
            {filteredCategories.length} of {categories.length} categories
          </div>
        </div>
      </div>

      {/* Categories Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {filteredCategories.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              {categories.length === 0 ? 'No categories' : 'No matching categories'}
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {categories.length === 0
                ? 'Get started by creating a new category.'
                : 'Try adjusting your search or filter criteria.'}
            </p>
            {categories.length === 0 && (
              <div className="mt-6">
                <button onClick={openCreateModal} className="btn-primary">
                  Create Category
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filteredCategories.map((category) => (
              <div key={category.id} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">{category.name}</h3>
                    <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                      {category.description || 'No description'}
                    </p>
                  </div>
                  <span
                    className={`ml-2 px-2 py-1 text-xs font-semibold rounded-full flex-shrink-0 ${
                      category.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {category.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>

                <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
                  <span>ID: {category.id}</span>
                  <span>
                    {new Date(category.created_at).toLocaleDateString()}
                  </span>
                </div>

                <div className="mt-4 grid grid-cols-3 gap-2">
                  <button
                    onClick={() => openDetailsModal(category)}
                    className="btn-secondary text-sm"
                    title="View Details"
                  >
                    <svg className="w-4 h-4 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => openEditModal(category)}
                    className="btn-secondary text-sm"
                    title="Edit"
                  >
                    <svg className="w-4 h-4 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => handleDelete(category.id, category.name)}
                    className="btn-danger text-sm"
                    title="Delete"
                  >
                    <svg className="w-4 h-4 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create/Edit Modal */}
      {showModal && (
        <div className="fixed z-50 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
            {/* Background overlay */}
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" onClick={closeModal}></div>

            {/* Modal panel */}
            <div className="relative inline-block bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-lg w-full" onClick={(e) => e.stopPropagation()}>
              <form onSubmit={handleSubmit}>
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className="mt-3 text-center sm:mt-0 sm:text-left w-full">
                      <h3 className="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                        {editingCategory ? 'Edit Category' : 'Create New Category'}
                      </h3>

                      <div className="mt-6 space-y-4">
                        {/* Name Field */}
                        <div>
                          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                            Category Name <span className="text-red-500">*</span>
                          </label>
                          <input
                            type="text"
                            name="name"
                            id="name"
                            required
                            value={formData.name}
                            onChange={handleInputChange}
                            className={`input-field mt-1 ${formErrors.name ? 'border-red-500' : ''}`}
                            placeholder="Enter category name"
                          />
                          {formErrors.name && (
                            <p className="mt-1 text-sm text-red-600">{formErrors.name}</p>
                          )}
                        </div>

                        {/* Description Field */}
                        <div>
                          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                            Description
                          </label>
                          <textarea
                            name="description"
                            id="description"
                            rows={3}
                            value={formData.description}
                            onChange={handleInputChange}
                            className={`input-field mt-1 ${formErrors.description ? 'border-red-500' : ''}`}
                            placeholder="Enter category description (optional)"
                          />
                          {formErrors.description && (
                            <p className="mt-1 text-sm text-red-600">{formErrors.description}</p>
                          )}
                          <p className="mt-1 text-xs text-gray-500">
                            {formData.description.length}/200 characters
                          </p>
                        </div>

                        {/* Active Checkbox */}
                        <div className="flex items-center">
                          <input
                            type="checkbox"
                            name="is_active"
                            id="is_active"
                            checked={formData.is_active}
                            onChange={handleInputChange}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                          <label htmlFor="is_active" className="ml-2 block text-sm text-gray-900">
                            Active
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                  <button
                    type="submit"
                    disabled={submitting}
                    className="btn-primary w-full sm:w-auto sm:ml-3 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {submitting ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 inline-block" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        {editingCategory ? 'Updating...' : 'Creating...'}
                      </>
                    ) : (
                      <>{editingCategory ? 'Update' : 'Create'}</>
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={closeModal}
                    disabled={submitting}
                    className="btn-secondary w-full sm:w-auto mt-3 sm:mt-0 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Details Modal */}
      {showDetailsModal && viewingCategory && (
        <div className="fixed z-50 inset-0 overflow-y-auto" aria-labelledby="details-modal-title" role="dialog" aria-modal="true">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
            {/* Background overlay */}
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" onClick={closeDetailsModal}></div>

            {/* Modal panel */}
            <div className="relative inline-block bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-lg w-full" onClick={(e) => e.stopPropagation()}>
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6">
                <div className="sm:flex sm:items-start">
                  <div className="mt-3 text-center sm:mt-0 sm:text-left w-full">
                    <h3 className="text-lg leading-6 font-medium text-gray-900 flex items-center justify-between" id="details-modal-title">
                      Category Details
                      <span
                        className={`px-3 py-1 text-xs font-semibold rounded-full ${
                          viewingCategory.is_active
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {viewingCategory.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </h3>

                    <div className="mt-6 space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-500">ID</label>
                        <p className="mt-1 text-sm text-gray-900">{viewingCategory.id}</p>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-500">Name</label>
                        <p className="mt-1 text-base text-gray-900 font-medium">{viewingCategory.name}</p>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-500">Description</label>
                        <p className="mt-1 text-sm text-gray-900">
                          {viewingCategory.description || 'No description provided'}
                        </p>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-500">Created At</label>
                          <p className="mt-1 text-sm text-gray-900">
                            {new Date(viewingCategory.created_at).toLocaleString()}
                          </p>
                        </div>

                        {viewingCategory.updated_at && (
                          <div>
                            <label className="block text-sm font-medium text-gray-500">Updated At</label>
                            <p className="mt-1 text-sm text-gray-900">
                              {new Date(viewingCategory.updated_at).toLocaleString()}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={() => {
                    closeDetailsModal();
                    openEditModal(viewingCategory);
                  }}
                  className="btn-primary w-full sm:w-auto sm:ml-3"
                >
                  Edit
                </button>
                <button
                  type="button"
                  onClick={closeDetailsModal}
                  className="btn-secondary w-full sm:w-auto mt-3 sm:mt-0"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoriesPage;
