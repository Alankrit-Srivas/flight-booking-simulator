from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, timedelta
from database import get_db_connection
from auth_utils import hash_password, verify_password, create_access_token, decode_access_token
import mysql.connector

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Pydantic Models
class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)  # Add max_length
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

# Signup
@router.post("/signup", status_code=201)
def signup(user_data: UserSignup):
    """Register a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Truncate password if needed (bcrypt max is 72 bytes)
        password = user_data.password
        if len(password.encode('utf-8')) > 72:
            password = password[:72]

        # Hash password
        password_hash = hash_password(password)
        
        # Insert user
        query = """
            INSERT INTO users (email, password_hash, first_name, last_name, phone)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data.email,
            password_hash,
            user_data.first_name,
            user_data.last_name,
            user_data.phone
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        # Create access token
        token = create_access_token(data={"sub": user_data.email, "user_id": user_id})
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "message": "User registered successfully",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": user_data.email,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name
            }
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# Login
@router.post("/login")
def login(credentials: UserLogin):
    """Login user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user by email
        cursor.execute(
            "SELECT id, email, password_hash, first_name, last_name, is_active FROM users WHERE email = %s",
            (credentials.email,)
        )
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not user['is_active']:
            raise HTTPException(status_code=403, detail="Account is inactive")
        
        # Verify password
        if not verify_password(credentials.password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Update last login
        cursor.execute(
            "UPDATE users SET last_login = NOW() WHERE id = %s",
            (user['id'],)
        )
        conn.commit()
        
        # Create access token
        token = create_access_token(data={"sub": user['email'], "user_id": user['id']})
        
        cursor.close()
        conn.close()
        
        return {
            "success": True,
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user['id'],
                "email": user['email'],
                "first_name": user['first_name'],
                "last_name": user['last_name']
            }
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# Get Current User
@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    """Get current logged-in user details"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT id, email, first_name, last_name, phone, created_at FROM users WHERE email = %s",
            (payload['sub'],)
        )
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "success": True,
            "user": user
        }
    
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

# Logout (optional - client-side token removal)
@router.post("/logout")
def logout():
    """Logout user (client should remove token)"""
    return {
        "success": True,
        "message": "Logged out successfully"
    }