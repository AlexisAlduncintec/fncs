/**
 * Dashboard Page Component
 * Statistics and overview of categories
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { categoryService } from '../services/categoryService';
import LoadingSpinner from '../components/LoadingSpinner';

const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [recentCategories, setRecentCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      // Fetch all categories
      const result = await categoryService.getAllCategories();
      if (result.success) {
        const categories = result.data;

        // Calculate stats
        const totalCategories = categories.length;
        const activeCategories = categories.filter(cat => cat.is_active).length;
        const inactiveCategories = totalCategories - activeCategories;

        // Get recent categories (last 5)
        const recent = [...categories]
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 5);

        setStats({
          total: totalCategories,
          active: activeCategories,
          inactive: inactiveCategories,
        });
        setRecentCategories(recent);
      }
    } catch (err) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoadingSpinner text="Loading dashboard..." />
      </div>
    );
  }

  const StatCard = ({ title, value, icon, color, subtitle }) => (
    <div className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${color}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-full bg-opacity-10 ${color.replace('border-', 'bg-')}`}>
          {icon}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Overview of your FNCS category management system
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            title="Total Categories"
            value={stats?.total || 0}
            subtitle="All categories in system"
            color="border-blue-500"
            icon={
              <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            }
          />

          <StatCard
            title="Active Categories"
            value={stats?.active || 0}
            subtitle={`${stats?.total > 0 ? Math.round((stats?.active / stats?.total) * 100) : 0}% of total`}
            color="border-green-500"
            icon={
              <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
          />

          <StatCard
            title="Inactive Categories"
            value={stats?.inactive || 0}
            subtitle={`${stats?.total > 0 ? Math.round((stats?.inactive / stats?.total) * 100) : 0}% of total`}
            color="border-gray-500"
            icon={
              <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
            }
          />
        </div>

        {/* Recent Categories */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Recent Categories</h2>
              <Link to="/categories" className="text-sm text-blue-600 hover:text-blue-500 font-medium">
                View all →
              </Link>
            </div>
          </div>

          <div className="p-6">
            {recentCategories.length === 0 ? (
              <div className="text-center py-12">
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
                <h3 className="mt-2 text-sm font-medium text-gray-900">No categories yet</h3>
                <p className="mt-1 text-sm text-gray-500">Get started by creating a new category.</p>
                <div className="mt-6">
                  <Link to="/categories" className="btn-primary">
                    Create Category
                  </Link>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {recentCategories.map((category) => (
                  <div
                    key={category.id}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex-1">
                      <div className="flex items-center">
                        <h3 className="text-sm font-medium text-gray-900">{category.name}</h3>
                        <span
                          className={`ml-2 px-2 py-0.5 text-xs font-semibold rounded-full ${
                            category.is_active
                              ? 'bg-green-100 text-green-800'
                              : 'bg-gray-200 text-gray-800'
                          }`}
                        >
                          {category.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                      <p className="mt-1 text-xs text-gray-500 line-clamp-1">
                        {category.description || 'No description'}
                      </p>
                    </div>
                    <div className="ml-4 flex items-center text-xs text-gray-500">
                      <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {new Date(category.created_at).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link to="/categories" className="block">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold">Manage Categories</h3>
                  <p className="mt-1 text-sm text-blue-100">
                    View, create, edit, and delete categories
                  </p>
                </div>
              </div>
            </div>
          </Link>

          <div
            onClick={() => {
              fetchDashboardData();
              toast.success('Dashboard refreshed!');
            }}
            className="block cursor-pointer"
          >
            <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg shadow-md p-6 text-white hover:shadow-lg transition-shadow">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold">Refresh Data</h3>
                  <p className="mt-1 text-sm text-green-100">
                    Update statistics and recent categories
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
