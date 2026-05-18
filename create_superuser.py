import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'superadmin'
email = 'superadmin@example.com'
password = 'superadmin123'

if not User.objects.filter(username=username).exists():
    superuser = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='admin',
        is_superuser=True,
        is_staff=True
    )
    print('='*50)
    print('SUPERUSER CREATED SUCCESSFULLY!')
    print('='*50)
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Email: {email}')
    print('='*50)
else:
    print('='*50)
    print('SUPERUSER ALREADY EXISTS!')
    print('='*50)
    print(f'Username: {username}')
    print(f'Password: {password} (if you changed it, use your new password)')
    print(f'Email: {email}')
    print('='*50)
