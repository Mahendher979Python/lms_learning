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
sudo apt install python3-pip python3-venv nginx git mysql-server mysql-client libmysqlclient-dev certbot python3-certbot-nginx -y

# Step 3: Create Swap File (if needed)
echo "Step 3: Creating swap file..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# Step 4: Clone or navigate to project (skip if already cloned)
PROJECT_DIR="/home/ubuntu/online-learning-system"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Step 4: Cloning project repository..."
    cd /home/ubuntu
    git clone https://github.com/Mahendher979Python/lms_online_education.git online-learning-system
else
    echo "Step 4: Project directory already exists. Pulling latest changes..."
    cd $PROJECT_DIR
    git pull
fi

cd $PROJECT_DIR

# Step 5: Create Virtual Environment
echo "Step 5: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Step 6: Install Dependencies
echo "Step 6: Installing dependencies..."
pip install -r requirements.txt

# Step 7: Configure Environment Variables
echo "Step 7: Configuring environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual values!"
fi

# Step 8: Set Up MySQL Database
echo "Step 8: Setting up MySQL database..."
# Note: User must configure DB credentials in .env first
# This step is manual for security reasons

# Step 9: Make backup script executable
echo "Step 9: Setting up backup system..."
chmod +x $PROJECT_DIR/backup.sh

# Step 10: Run Django Migrations & Collect Static
echo "Step 10: Running Django migrations and collecting static files..."
cd backend
python manage.py migrate
python manage.py collectstatic --noinput

# Step 11: Set Up Gunicorn Service
echo "Step 11: Setting up Gunicorn service..."
sudo cp $PROJECT_DIR/lms.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start lms
sudo systemctl enable lms
sudo systemctl status lms

# Step 12: Configure Nginx
echo "Step 12: Configuring Nginx..."
sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/lms
sudo ln -sf /etc/nginx/sites-available/lms /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Step 13: Set Proper Permissions
echo "Step 13: Setting proper permissions..."
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
echo "4. (Optional) Set up daily backups: crontab -e"
echo ""
echo "Useful commands:"
echo "- Check Gunicorn logs: sudo journalctl -u lms -f"
echo "- Check Nginx logs: sudo tail -f /var/log/nginx/error.log"
