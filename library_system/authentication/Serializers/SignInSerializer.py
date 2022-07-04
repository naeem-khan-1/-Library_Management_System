
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from authentication.models import User
from datetime import datetime, timedelta


class SignInSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username_or_email", "")
        password = data.get("password", "")

        if username and password:
            if "@" in username:
                try:
                    fetch_user = User.objects.get(email=username)
                except User.DoesNotExist:
                    raise exceptions.ValidationError({"detail": "Invalid email"})
            else:
                try:
                    fetch_user = User.objects.get(username=username)
                except User.DoesNotExist:
                    raise exceptions.ValidationError({"detail": "Invalid username"})

            username = fetch_user.username
            user = authenticate(username=username, password=password)
            if user:
                data["user"] = user
                user.save()
            else:
                raise exceptions.ValidationError({"detail": "Invalid Credentials"})

        else:
            raise exceptions.ParseError("Must provide username and password both")
        return data
