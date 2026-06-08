# Deployment Production Checklist

## 1. Environment Variables (.env file)
- [ ] **SECRET_KEY**: Replace with a strong, unique secret key
- [ ] **DEBUG**: Set to `False` for production
- [ ] **ALLOWED_HOSTS**: Include your domain, IP, and localhost
- [ ] **CSRF_TRUSTED_ORIGINS**: Add your HTTPS URLs
- [ ] **DB_ENGINE**: Use `django.db.backends.mysql`
- [ ] **DB_NAME**: Database name (default: `lms_db`)
- [ ] **DB_USER**: Database user (default: `lms_user`)
- [ ] **DB_PASSWORD**: Strong password for database user
- [ ] **DB_HOST**: Database host (default: `localhost`)
- [ ] **DB_PORT**: Database port (default: `3306`)
- [ ] **EMAIL_HOST_USER**: Your email address for sending notifications
- [ ] **EMAIL_HOST_PASSWORD**: Email app password (not your regular password)
- [ ] **RAZORPAY_KEY_ID**: Razorpay key (if using payments)
- [ ] **RAZORPAY_KEY_SECRET**: Razorpay secret (if using payments)
- [ ] **GEMINI_API_KEY**: Google Gemini API key (if using AI features)

## 2. Database Setup (MySQL)
- [ ] MySQL server is installed and running
- [ ] Database `lms_db` is created with `utf8mb4` charset
- [ ] User `lms_user` is created and granted all privileges on `lms_db`
- [ ] MySQL is secured (run `sudo mysql_secure_installation`)

## 3. File Permissions
- [ ] Project directory owned by `ubuntu:www-data`
- [ ] Files and folders have correct permissions
- [ ] `backend/media/` is writable by the web server
- [ ] `staticfiles/` is accessible by Nginx

## 4. Static & Media Files
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Verify static files are served correctly
- [ ] Media upload directory is accessible

## 5. Services
- [ ] Gunicorn service is running: `sudo systemctl status lms`
- [ ] Gunicorn service is enabled on boot: `sudo systemctl enable lms`
- [ ] Nginx service is running: `sudo systemctl status nginx`
- [ ] Nginx config is valid: `sudo nginx -t`
- [ ] Firewall allows HTTP (port 80) and HTTPS (port 443)

## 6. SSL/HTTPS
- [ ] SSL certificate is installed (using Let's Encrypt)
- [ ] Nginx is configured to use HTTPS
- [ ] HTTP redirects to HTTPS
- [ ] Certificate auto-renewal is set up

## 7. Backups
- [ ] Backup script is executable
- [ ] Daily backups are scheduled via crontab
- [ ] Backups are stored off-server (optional but recommended)

## 8. Testing
- [ ] Visit your domain in a browser
- [ ] Test login with admin user
- [ ] Test all main functionalities (courses, attendance, etc.)
- [ ] Verify email notifications work
- [ ] Test media file uploads
