import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AOS from 'aos';
import 'aos/dist/aos.css';
import Home from './Home.jsx';
import Python1 from "./Python.jsx";
import HTML from "./HTML.jsx";
import CSS from "./CSS.jsx";
import JavaScript from './Javascript.jsx';
import MYSQL from './MYSQL.jsx';
import Contact from './Contact.jsx';
import About from './About.jsx';
import { AuthProvider, useAuth } from './Context/AuthContext';
import { LoginForm } from './components/Auth/LoginForm';
import { RegisterForm } from './components/Auth/RegisterForm';
import { Dashboard } from './components/Dashboard/Dashboard';
import { AdminPanel } from './components/Admin/AdminPanel';

const AuthenticationScreen = () => {
  const [authMode, setAuthMode] = useState('login');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
      {authMode === 'login' ? (
        <LoginForm onSwitchToRegister={() => setAuthMode('register')} />
      ) : (
        <RegisterForm onSwitchToLogin={() => setAuthMode('login')} />
      )}
    </div>
  );
};

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { currentUser, isAdmin, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!currentUser) {
    return <AuthenticationScreen />;
  }

  if (adminOnly && !isAdmin()) {
    // Redirect non-admin users trying to access admin routes
    return <Python1 />;
  }

  return children;
};

const MainApplication = () => {
  const { currentUser, isAdmin, loading } = useAuth();
  const [currentView, setCurrentView] = useState('dashboard');

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!currentUser) {
    return <AuthenticationScreen />;
  }

  if (currentView === 'admin' && isAdmin()) {
    return <AdminPanel onBack={() => setCurrentView('dashboard')} />;
  }

  return (
    <div>
      <Dashboard />
      {isAdmin() && (
        <div className="fixed bottom-6 right-6">
          <button
            onClick={() => setCurrentView('admin')}
            className="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            title="Admin Panel"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

function App() {
    useEffect(() => {
        // Global AOS initialization
        AOS.init({
            duration: 1000,
            once: true,
            mirror: false,
        });
    }, []);

    return (
        <Router>
            <AuthProvider>
                <Routes>
                    {/* Public routes */}
                    <Route path="/" element={<Home />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/contact" element={<Contact />} />
                    <Route path="/about" element={<About />} />
                    
                    {/* Authentication routes */}
                    <Route path="/login" element={<AuthenticationScreen />} />
                    <Route path="/create-account" element={<AuthenticationScreen />} />
                    
                    {/* Protected routes for regular users */}
                    <Route path="/python1" element={
                        <ProtectedRoute>
                            <Python1 />
                        </ProtectedRoute>
                    } />
                    <Route path="/html" element={
                        <ProtectedRoute>
                            <HTML />
                        </ProtectedRoute>
                    } />
                    <Route path="/css" element={
                        <ProtectedRoute>
                            <CSS />
                        </ProtectedRoute>
                    } />
                    <Route path="/javascript" element={
                        <ProtectedRoute>
                            <JavaScript />
                        </ProtectedRoute>
                    } />
                    <Route path="/mysql" element={
                        <ProtectedRoute>
                            <MYSQL />
                        </ProtectedRoute>
                    } />
                    
                    {/* Admin-only routes */}
                    <Route path="/dashboard" element={
                        <ProtectedRoute adminOnly={true}>
                            <MainApplication />
                        </ProtectedRoute>
                    } />
                </Routes>
            </AuthProvider>
        </Router>
    );
}

export default App;