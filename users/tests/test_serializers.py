import pytest
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from users.serializers import CustomRegisterSerializer

import pytest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from users.serializers import CustomRegisterSerializer


def attach_session(request):
    """Attach session to request manually"""
    middleware = SessionMiddleware(get_response=lambda req: None)
    middleware.process_request(request)
    request.session.save()
User = get_user_model()

@pytest.mark.django_db
class TestCustomRegisterSerializer:

    def test_valid_data_creates_user(self):
        """Ensure serializer creates user with proper data"""
        data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "StrongPass123",
            "password2": "StrongPass123"
        }

        serializer = CustomRegisterSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

        # 🏗 Build a fake request with session
        factory = RequestFactory()
        request = factory.post("/register/", data)
        attach_session(request)
        request.user = AnonymousUser()

        # 💾 Now pass the request to save()
        user = serializer.save(request=request)

        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.check_password("StrongPass123") is True

    def test_passwords_do_not_match(self):
        """Should fail if passwords don't match"""
        data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "StrongPass123",
            "password2": "WrongPass123"
        }
        serializer = CustomRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password2" in serializer.errors or "non_field_errors" in serializer.errors

    def test_missing_required_fields(self):
        """Should fail with missing fields"""
        data = {
            "email": "test@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123"
        }
        serializer = CustomRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors
        assert "last_name" in serializer.errors
