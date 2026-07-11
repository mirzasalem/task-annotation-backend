#!/usr/bin/env python
"""Create demo user for the application."""
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User


def create_demo_user():
    email = "demo@vai-radiology.com"
    password = "Demo@1234"
    username = "demo_user"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email},
    )
    user.email = email
    user.set_password(password)
    user.save()

    action = "Created" if created else "Updated"
    print(f"{action} demo user:")
    print(f"  Email: {email}")
    print(f"  Password: {password}")


if __name__ == "__main__":
    create_demo_user()
