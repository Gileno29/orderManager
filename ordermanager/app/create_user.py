import os
from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'ordermanager')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin@ordermanager')

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser {username}...")
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully!")
    else:
        print(f"Superuser {username} already exists.")

if __name__ == "__main__":
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ordermanager.settings')
    django.setup()
    create_superuser()