import React, { useState, useEffect } from 'react';
import { authApi } from '../../services/api/authApi';

interface AuthComponentProps {
  onAuthChange: (user: any) => void;
}

const AuthComponent: React.FC<AuthComponentProps> = ({ onAuthChange }) => {
  const [isLogin, setIsLogin] = useState<boolean>(true);
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);

  // Check if user is already authenticated on component mount
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      checkAuthStatus();
    }
  }, []);

  const checkAuthStatus = async () => {
    try {
      const profile = await authApi.getProfile();
      setUser(profile.user);
      onAuthChange(profile.user);
    } catch (err) {
      console.error('Auth check failed:', err);
      localStorage.removeItem('authToken');
      setUser(null);
      onAuthChange(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isLogin) {
        // Login
        const result = await authApi.login(email, password);
        localStorage.setItem('authToken', result.token);
        setUser(result.user);
        onAuthChange(result.user);
      } else {
        // Register
        const result = await authApi.register(email, password, name);
        localStorage.setItem('authToken', result.token);
        setUser(result.user);
        onAuthChange(result.user);
      }

      // Reset form
      setEmail('');
      setPassword('');
      setName('');
    } catch (err) {
      console.error(isLogin ? 'Login' : 'Registration', 'error:', err);
      setError(`Authentication failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authApi.logout();
      localStorage.removeItem('authToken');
      setUser(null);
      onAuthChange(null);
    } catch (err) {
      console.error('Logout error:', err);
      // Even if logout API fails, clear local storage
      localStorage.removeItem('authToken');
      setUser(null);
      onAuthChange(null);
    }
  };

  if (user) {
    return (
      <div className="auth-component">
        <div className="user-info">
          <h4>Welcome, {user.name || user.email}!</h4>
          <p>Logged in as: {user.email}</p>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-component">
      <div className="auth-toggle">
        <button
          className={`toggle-btn ${isLogin ? 'active' : ''}`}
          onClick={() => setIsLogin(true)}
        >
          Login
        </button>
        <button
          className={`toggle-btn ${!isLogin ? 'active' : ''}`}
          onClick={() => setIsLogin(false)}
        >
          Register
        </button>
      </div>

      <form onSubmit={handleSubmit} className="auth-form">
        {!isLogin && (
          <div className="form-group">
            <label htmlFor="name">Full Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your full name"
              required={!isLogin}
            />
          </div>
        )}

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
            minLength={6}
          />
        </div>

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}

        <button type="submit" disabled={loading} className="auth-btn">
          {loading ? (isLogin ? 'Logging in...' : 'Registering...') : (isLogin ? 'Login' : 'Register')}
        </button>
      </form>
    </div>
  );
};

export default AuthComponent;