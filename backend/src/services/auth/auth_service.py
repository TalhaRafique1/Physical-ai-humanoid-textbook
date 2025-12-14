"""
Authentication Service for the textbook generation system.

This module implements user authentication using Better-Auth as specified in the constitution.
"""
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field
import logging

# Mock implementation of Better-Auth functionality
# In a real implementation, this would use the actual Better-Auth library

class User(BaseModel):
    """User model for authentication."""
    id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User's email address")
    name: str = Field(default="", description="User's full name")
    created_at: datetime = Field(default_factory=datetime.now, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences and settings")


class AuthCredentials(BaseModel):
    """Authentication credentials model."""
    email: str
    password: str


class AuthService:
    """Service class for handling user authentication."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # In-memory storage for demonstration purposes
        # In production, this would use a database
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}

        # Secret key for JWT tokens (in production, this should be securely stored)
        self.jwt_secret = secrets.token_hex(32)
        self.jwt_algorithm = "HS256"

    def hash_password(self, password: str) -> str:
        """Hash a password using salted SHA-256."""
        salt = secrets.token_hex(16)
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"{salt}${pwdhash.hex()}"

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            salt, stored_hash = hashed_password.split('$')
            pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return pwdhash.hex() == stored_hash
        except Exception:
            return False

    async def register_user(self, email: str, password: str, name: str = "") -> Optional[Dict[str, Any]]:
        """Register a new user."""
        try:
            # Check if user already exists
            if email in [user.email for user in self.users.values()]:
                return None

            # Create new user
            user_id = f"user_{secrets.token_hex(8)}"
            hashed_pwd = self.hash_password(password)

            user = User(
                id=user_id,
                email=email,
                name=name,
                preferences={
                    'personalization_enabled': True,
                    'preferred_language': 'en',
                    'theme': 'light',
                    'learning_preferences': {
                        'content_depth': 'medium',
                        'learning_style': 'visual',
                        'reading_speed': 'normal'
                    }
                }
            )

            self.users[user_id] = user

            # Create session token
            token = self._generate_token(user_id)

            # Store session
            self.sessions[token] = {
                'user_id': user_id,
                'expires_at': datetime.now() + timedelta(days=7)
            }

            self.logger.info(f"User registered: {email}")

            return {
                'user': user.dict(),
                'token': token,
                'expires_in': 7 * 24 * 60 * 60  # 7 days in seconds
            }
        except Exception as e:
            self.logger.error(f"Error registering user {email}: {str(e)}")
            return None

    async def login_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user and return a session token."""
        try:
            # Find user by email
            user = None
            for u in self.users.values():
                if u.email == email:
                    user = u
                    break

            if not user:
                return None

            # Verify password
            stored_user_password = user.preferences.get('hashed_password', '')
            if not self.verify_password(password, stored_user_password):
                return None

            # Create session token
            token = self._generate_token(user.id)

            # Store session
            self.sessions[token] = {
                'user_id': user.id,
                'expires_at': datetime.now() + timedelta(days=7)
            }

            self.logger.info(f"User logged in: {email}")

            return {
                'user': user.dict(),
                'token': token,
                'expires_in': 7 * 24 * 60 * 60  # 7 days in seconds
            }
        except Exception as e:
            self.logger.error(f"Error logging in user {email}: {str(e)}")
            return None

    async def logout_user(self, token: str) -> bool:
        """Logout a user by invalidating their session."""
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False

    async def get_user_by_token(self, token: str) -> Optional[User]:
        """Get user information by their session token."""
        if token not in self.sessions:
            return None

        session = self.sessions[token]

        # Check if session is expired
        if session['expires_at'] < datetime.now():
            del self.sessions[token]
            return None

        user_id = session['user_id']
        return self.users.get(user_id)

    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences."""
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        user.preferences.update(preferences)
        user.updated_at = datetime.now()

        return True

    def _generate_token(self, user_id: str) -> str:
        """Generate a JWT token for the user."""
        payload = {
            'user_id': user_id,
            'exp': datetime.now() + timedelta(days=7),
            'iat': datetime.now()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_token(self, token: str) -> Optional[str]:
        """Verify a JWT token and return the user ID."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            user_id = payload.get('user_id')

            # Check if session still exists
            if token in self.sessions:
                session = self.sessions[token]
                if session['user_id'] == user_id and session['expires_at'] > datetime.now():
                    return user_id

            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


# Example usage:
# auth_service = AuthService()
# result = await auth_service.register_user("user@example.com", "password123", "John Doe")
# token = result['token']
# user = await auth_service.get_user_by_token(token)