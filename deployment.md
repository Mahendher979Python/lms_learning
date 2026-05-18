# AWS EC2 Ubuntu Deployment Guide for Django LMS

## Prerequisites
- AWS EC2 Ubuntu instance (22.04 LTS recommended)
- Domain name (optional but recommended)
- SSH access to EC2 instance

## Step 1: Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install Required Software
```bash
sudo apt install python3-pip python3-venv nginx git postgresql postgresql-contrib -y
```

## Step 3: Clone the Project
```bash
cd /home/ubuntu
git clone https://github.com/Mahendher979Python/online-learning-system.git
cd online-learning-system
```

## Step 4: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 6: Configure Environment Variables
```bash
cp .env.example .env
nano .env  # Edit with your actual values
```

## Step 7: Set Up PostgreSQL Database
```bash
sudo -u postgres psql
```
Inside PostgreSQL:
```sql
CREATE DATABASE your_db_name;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
\q
```

## Step 8: Run Django Migrations & Collect Static
```bash
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Create admin user
```

## Step 9: Set Up Gunicorn Service
```bash
sudo cp /home/ubuntu/online-learning-system/lms.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start lms
sudo systemctl enable lms
sudo systemctl status lms  # Verify it's running
```

## Step 10: Configure Nginx
```bash
sudo cp /home/ubuntu/online-learning-system/nginx.conf /etc/nginx/sites-available/lms
sudo ln -s /etc/nginx/sites-available/lms /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## Step 11: Set Up SSL with Let's Encrypt (Optional but Recommended)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Step 12: Set Proper Permissions
```bash
cd /home/ubuntu/online-learning-system
sudo chown -R ubuntu:www-data .
sudo chmod -R 755 .
sudo chmod -R 775 backend/media/
```

## Useful Commands
- Check Gunicorn logs: `sudo journalctl -u lms -f`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Restart Gunicorn: `sudo systemctl restart lms`
- Restart Nginx: `sudo systemctl restart nginx`
