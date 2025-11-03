/**
 * Home Page Component
 * Landing page for the FNCS application
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const HomePage = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 sm:text-6xl">
            FNCS
          </h1>
          <p className="mt-3 text-xl text-gray-600 sm:mt-5 sm:text-2xl">
            Financial News Classification System
          </p>
          <p className="mt-6 max-w-2xl mx-auto text-lg text-gray-500">
            Manage and organize financial news categories with a secure, modern web application.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            {user ? (
              <Link to="/categories" className="btn-primary text-lg px-8 py-3">
                Go to Categories
              </Link>
            ) : (
              <>
                <Link to="/login" className="btn-primary text-lg px-8 py-3">
                  Sign In
                </Link>
                <Link to="/register" className="btn-secondary text-lg px-8 py-3">
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Features */}
          <div className="mt-20 grid grid-cols-1 gap-8 sm:grid-cols-3">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-4xl mb-4">🔐</div>
              <h3 className="text-lg font-semibold text-gray-900">Secure Authentication</h3>
              <p className="mt-2 text-gray-600">
                JWT-based authentication with bcrypt password hashing
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-4xl mb-4">📊</div>
              <h3 className="text-lg font-semibold text-gray-900">Category Management</h3>
              <p className="mt-2 text-gray-600">
                Complete CRUD operations for organizing news categories
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-4xl mb-4">⚡</div>
              <h3 className="text-lg font-semibold text-gray-900">Modern Stack</h3>
              <p className="mt-2 text-gray-600">
                Built with React, Flask, and PostgreSQL on Supabase
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
