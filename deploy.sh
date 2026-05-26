#!/bin/bash

# AWS EC2 Ubuntu Deployment Script for Django LMS

set -e  # Exit on error

echo "=============================================="
echo "Starting Django LMS Deployment"
echo "=============================================="

# Step 1: Update System Packages
echo "Step 1: Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Step 2: Install Required Software
echo "Step 2: Installing required software..."
sudo apt install python3-pip python3-venv nginx git postgresql postgresql-contrib -y

# Step 3: Clone or navigate to project (skip if already cloned)
PROJECT_DIR="/home/ubuntu/online-learning-system"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Step 3: Cloning project repository..."
    cd /home/ubuntu
    git clone https://github.com/Mahendher979Python/online-learning-system.git
else
    echo "Step 3: Project directory already exists. Pulling latest changes..."
    cd $PROJECT_DIR
    git pull
fi

cd $PROJECT_DIR

# Step 4: Create Virtual Environment
echo "Step 4: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Step 5: Install Dependencies
echo "Step 5: Installing dependencies..."
pip install -r requirements.txt

# Step 6: Configure Environment Variables
echo "Step 6: Configuring environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual values!"
fi

# Step 7: Set Up PostgreSQL Database
echo "Step 7: Setting up PostgreSQL database..."
# Note: User must configure DB credentials in .env first
# This step is manual for security reasons

# Step 8: Run Django Migrations & Collect Static
echo "Step 8: Running Django migrations and collecting static files..."
cd backend
python manage.py migrate
python manage.py collectstatic --noinput

# Step 9: Set Up Gunicorn Service
echo "Step 9: Setting up Gunicorn service..."
sudo cp $PROJECT_DIR/lms.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start lms
sudo systemctl enable lms
sudo systemctl status lms

# Step 10: Configure Nginx
echo "Step 10: Configuring Nginx..."
sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/lms
sudo ln -sf /etc/nginx/sites-available/lms /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Step 11: Set Proper Permissions
echo "Step 11: Setting proper permissions..."
cd $PROJECT_DIR
sudo chown -R ubuntu:www-data .
sudo chmod -R 755 .
sudo chmod -R 775 backend/media/
sudo chmod -R 755 staticfiles/

echo "=============================================="
echo "Deployment Complete!"
echo "=============================================="
echo ""
echo "Next Steps:"
echo "1. Edit .env file with your actual credentials"
echo "2. Restart Gunicorn: sudo systemctl restart lms"
echo "3. (Optional) Set up SSL with Let's Encrypt"
echo ""
echo "Useful commands:"
echo "- Check Gunicorn logs: sudo journalctl -u lms -f"
echo "- Check Nginx logs: sudo tail -f /var/log/nginx/error.log"
