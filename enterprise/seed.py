import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enterprise.settings')
django.setup()

from admin.models import user

users = [
    {
        'name': 'System Admin',
        'email': 'admin@assetflow.io',
        'password': 'admin',
        'role': 'admin',
    },
    {
        'name': 'Sarah Connor',
        'email': 'depthead@assetflow.io',
        'password': 'dept',
        'role': 'dept_head',
    },
    {
        'name': 'Michael Scott',
        'email': 'manager@assetflow.io',
        'password': 'mgr',
        'role': 'manager',
    },
    {
        'name': 'Jim Halpert',
        'email': 'employee@assetflow.io',
        'password': 'emp',
        'role': 'employee',
    },
]

for u in users:
    obj, created = user.objects.get_or_create(
        email=u['email'],
        defaults={
            'name': u['name'],
            'password': make_password(u['password']),
            'role': u['role'],
            'is_active': True,
        }
    )
    if created:
        print(f"[CREATED] {u['role']}: {u['email']} / {u['password']}")
    else:
        print(f"[EXISTS]  {u['role']}: {u['email']}")
