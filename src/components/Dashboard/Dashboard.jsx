import React from 'react';
import { LogOut, User, Calendar, Clock, Shield } from 'lucide-react';
import { useAuth } from '../../Context/AuthContext';

export const Dashboard = () => {
  const { currentUser, logout, isAdmin } = useAuth();

  const handleLogout = () => {
    logout();
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (!currentUser) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <User className="w-5 h-5 text-white" />
                </div>
                <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
              </div>
              {isAdmin() && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  <Shield className="w-3 h-3 mr-1" />
                  Admin
                </span>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Welcome Card */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <User className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h2 className="text-3xl font-bold text-gray-900">Welcome back, {currentUser.name}!</h2>
                  <p className="text-gray-600 mt-1">Great to see you again</p>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-blue-50 rounded-xl p-6">
                  <div className="flex items-center space-x-3">
                    <Calendar className="w-8 h-8 text-blue-600" />
                    <div>
                      <h3 className="font-semibold text-gray-900">Member Since</h3>
                      <p className="text-gray-600">{formatDate(currentUser.createdAt)}</p>
                    </div>
                  </div>
                </div>
                
                <div className="bg-green-50 rounded-xl p-6">
                  <div className="flex items-center space-x-3">
                    <Clock className="w-8 h-8 text-green-600" />
                    <div>
                      <h3 className="font-semibold text-gray-900">Last Login</h3>
                      <p className="text-gray-600">
                        {currentUser.lastLogin ? formatDate(currentUser.lastLogin) : 'Just now'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Status</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Account Type</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    isAdmin() 
                      ? 'bg-purple-100 text-purple-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {isAdmin() ? 'Administrator' : 'Standard User'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Status</span>
                  <span className="px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                    Active
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Email</span>
                  <span className="text-sm text-gray-900 truncate max-w-32">{currentUser.email}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};