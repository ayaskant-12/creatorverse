#!/usr/bin/env python3
"""
Quick test script for CreatorVerse
"""
import os
import sys

def test_imports():
    """Test if all required packages are installed"""
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from werkzeug.security import generate_password_hash
        import openai
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database connection"""
    try:
        from app import app, db, User
        with app.app_context():
            db.create_all()
            user_count = User.query.count()
            print(f"✅ Database connection successful. Users in DB: {user_count}")
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing CreatorVerse setup...")
    
    if test_imports() and test_database():
        print("\n🎉 All tests passed! You can now run:")
        print("   python app.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
