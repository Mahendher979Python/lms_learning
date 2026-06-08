# Complete Deployment Guide for Django LMS on AWS EC2

## 1. Prerequisites
- AWS Account
- Domain name (optional, but recommended)
- Basic knowledge of Linux and AWS

---

## 2. Step 1: Launch EC2 Instance

### 2.1 Launch Instance
1. Go to AWS EC2 Console → Launch Instances
2. Choose Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
3. Select Instance Type: t2.medium (minimum recommended for production)
4. Configure Instance Details: Default settings
5. Add Storage: 30 GB+ SSD
6. Add Tags (optional): Key=Name, Value=LMS-Server
7. Configure Security Group:
   - Type: SSH, Port: 22, Source: Your IP or 0.0.0.0/0 (not recommended for production)
   - Type: HTTP, Port: 80, Source: 0.0.0.0/0
   - Type: HTTPS, Port: 443, Source: 0.0.0.0/0
8. Review and Launch
9. Create a new key pair or use existing one, download the .pem file

### 2.2 Allocate Elastic IP (Important for Static IP)
1. Go to EC2 → Elastic IPs
2. Allocate Elastic IP address
3. Associate it with your EC2 instance

---

## 3. Step 2: Connect to EC2 Instance
```bash
chmod 400 your-key-pair.pem
ssh -i your-key-pair.pem ubuntu@your-elastic-ip
```

---

## 4. Step 3: Initial Server Setup
```bash
# Update and upgrade packages
sudo apt update && sudo apt upgrade -y

# Create a swap file (if needed)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 5. Step 4: Install Required Software
```bash
sudo apt install python3-pip python3-venv nginx git mysql-server mysql-client libmysqlclient-dev certbot python3-certbot-nginx -y
```

---

## 6. Step 5: Configure MySQL
```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Connect to MySQL
sudo mysql -u root -p

# Run these SQL commands inside MySQL:
CREATE DATABASE lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lms_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON lms_db.* TO 'lms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 7. Step 6: Clone or Upload Project
```bash
cd /home/ubuntu
git clone https://github.com/Mahendher979Python/lms_online_education.git online-learning-system
cd online-learning-system
```

---

## 8. Step 7: Create Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 9. Step 8: Configure Environment Variables
```bash
# Copy example .env file
cp .env.example .env

# Edit .env file with your credentials
nano .env
```

Update these values in .env:
```
SECRET_KEY=your_very_long_and_secure_secret_key_here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-elastic-ip,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com,http://your-elastic-ip

DB_ENGINE=django.db.backends.mysql
DB_NAME=lms_db
DB_USER=lms_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=3306

# Email settings (for OTP, notifications)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Payment gateways
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# AI
GEMINI_API_KEY=your_gemini_api_key
```

---

## 10. Step 9: Run Migrations & Collect Static
```bash
cd backend
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

---

## 11. Step 10: Configure Gunicorn
```bash
# Copy service file to systemd
sudo cp /home/ubuntu/online-learning-system/lms.service /etc/systemd/system/

# Reload daemon and start service
sudo systemctl daemon-reload
sudo systemctl start lms
sudo systemctl enable lms
sudo systemctl status lms
```

---

## 12. Step 11: Configure Nginx
```bash
# Copy nginx config
sudo cp /home/ubuntu/online-learning-system/nginx.conf /etc/nginx/sites-available/lms

# Create symlink and remove default
sudo ln -sf /etc/nginx/sites-available/lms /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx config and restart
sudo nginx -t
sudo systemctl restart nginx
```

---

## 13. Step 12: Set Correct File Permissions
```bash
cd /home/ubuntu/online-learning-system
sudo chown -R ubuntu:www-data .
sudo chmod -R 755 .
sudo chmod -R 775 backend/media/
```

---

## 14. Step 13: SSL/HTTPS with Let's Encrypt
```bash
# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Certbot will automatically update your nginx config
```

---

## 15. Step 14: Set Up Backup System
```bash
# Make backup script executable
chmod +x /home/ubuntu/online-learning-system/backup.sh

# Add to crontab to run daily at 2 AM
crontab -e
# Add this line:
0 2 * * * /home/ubuntu/online-learning-system/backup.sh >> /home/ubuntu/backup_logs.log 2>&1
```

---

## 16. Verify Deployment
1. Visit `https://your-domain.com` in your browser
2. Test login with superuser credentials
3. Test admin, trainer, and student roles
4. Verify all modules work correctly

---

## Useful Commands
```bash
# Check Gunicorn logs
sudo journalctl -u lms -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart services
sudo systemctl restart lms
sudo systemctl restart nginx

# Reload services
sudo systemctl reload lms
sudo systemctl reload nginx
```

---

## Troubleshooting
1. **502 Bad Gateway**: Check Gunicorn is running with `sudo systemctl status lms`
2. **Static files not loading**: Run `python manage.py collectstatic --noinput`
3. **Database errors**: Verify .env has correct database credentials

