#!/bin/bash

# Quick deployment verification script for LMS

echo "=============================================="
echo "🔍 LMS Deployment Verification"
echo "=============================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "❌ Please don't run as root! Run as ubuntu user."
    exit 1
fi

cd /home/ubuntu/online-learning-system || exit 1

# 1. Check .env file exists
echo "1️⃣ Checking .env file..."
if [ -f .env ]; then
    echo "✅ .env file found"
    echo "   Checking ALLOWED_HOSTS..."
    if grep -q "43.204.217.186" .env; then
        echo "   ✅ EC2 IP in ALLOWED_HOSTS"
    else
        echo "   ❌ EC2 IP (43.204.217.186) NOT found in ALLOWED_HOSTS"
    fi
    
    echo "   Checking DEBUG..."
    if grep -q "DEBUG=False" .env; then
        echo "   ✅ DEBUG is False (good for production)"
    else
        echo "   ⚠️  DEBUG is still True - set to False in production!"
    fi
else
    echo "❌ .env file NOT found!"
fi
echo ""

# 2. Check virtual environment
echo "2️⃣ Checking virtual environment..."
if [ -d "venv" ]; then
    echo "✅ venv exists"
else
    echo "❌ venv NOT found!"
fi
echo ""

# 3. Check services
echo "3️⃣ Checking services..."
echo "   - Gunicorn (lms):"
if systemctl is-active --quiet lms; then
    echo "     ✅ lms service is running"
else
    echo "     ❌ lms service is NOT running!"
fi

echo "   - Nginx:"
if systemctl is-active --quiet nginx; then
    echo "     ✅ nginx service is running"
else
    echo "     ❌ nginx service is NOT running!"
fi

echo "   - MySQL:"
if systemctl is-active --quiet mysql; then
    echo "     ✅ mysql service is running"
else
    echo "     ❌ mysql service is NOT running!"
fi
echo ""

# 4. Check static files
echo "4️⃣ Checking static files..."
if [ -d "staticfiles" ]; then
    echo "✅ staticfiles directory exists"
else
    echo "❌ staticfiles directory NOT found - run collectstatic!"
fi
echo ""

# 5. Check staticfiles content
echo "5️⃣ Checking staticfiles content..."
if [ -n "$(ls -A staticfiles 2>/dev/null)" ]; then
    echo "✅ staticfiles has content"
else
    echo "⚠️  staticfiles is empty - run python manage.py collectstatic --noinput"
fi
echo ""

echo "=============================================="
echo "✅ Verification complete!"
echo "=============================================="
