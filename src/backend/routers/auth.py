"""
Authentication endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import hashlib

from ..database import teachers_collection

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register")
def register(username: str, display_name: str, password: str) -> Dict[str, Any]:
    """Register a new teacher account"""
    # Check if username already exists
    existing_teacher = teachers_collection.find_one({"_id": username})
    
    if existing_teacher:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash the provided password
    hashed_password = hash_password(password)
    
    # Create new teacher record
    new_teacher = {
        "_id": username,
        "username": username,
        "display_name": display_name,
        "password": hashed_password,
        "role": "teacher"
    }
    
    # Insert the new teacher
    teachers_collection.insert_one(new_teacher)
    
    # Return teacher information (excluding password)
    return {
        "username": new_teacher["username"],
        "display_name": new_teacher["display_name"],
        "role": new_teacher["role"],
        "message": "Registration successful"
    }

@router.post("/login")
def login(username: str, password: str) -> Dict[str, Any]:
    """Login a teacher account"""
    # Hash the provided password
    hashed_password = hash_password(password)
    
    # Find the teacher in the database
    teacher = teachers_collection.find_one({"_id": username})
    
    if not teacher or teacher["password"] != hashed_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Return teacher information (excluding password)
    return {
        "username": teacher["username"],
        "display_name": teacher["display_name"],
        "role": teacher["role"]
    }

@router.get("/check-session")
def check_session(username: str) -> Dict[str, Any]:
    """Check if a session is valid by username"""
    teacher = teachers_collection.find_one({"_id": username})
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return {
        "username": teacher["username"],
        "display_name": teacher["display_name"],
        "role": teacher["role"]
    }