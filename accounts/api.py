import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from ninja import Router
from django.contrib.auth import authenticate
from django.http import HttpRequest
from accounts.models import User
from accounts.schemas import UserRegisterSchema, UserLoginSchema, UserProfileOutSchema

router = Router(tags=["Authentication"])

def create_access_token(user: User) -> str:
    """Generates a JWT valid for 24 hours."""
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

@router.post("/register", response={201: UserProfileOutSchema, 400: dict})
def register_user(request: HttpRequest, payload: UserRegisterSchema):
    if User.objects.filter(username=payload.username).exists():
        return 400, {"message": "Username already taken."}
    
    if User.objects.filter(email=payload.email).exists():
        return 400, {"message": "Email already in use."}

    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        role=payload.role,
        phone_number=payload.phone_number
    )
    return 201, user

@router.post("/login", response={200: dict, 401: dict})
def login_user(request: HttpRequest, payload: UserLoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    
    if user is not None:
        # Generate the JWT instead of using Django's login()
        access_token = create_access_token(user)
        return 200, {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role,
            "message": "Login successful"
        }
        
    return 401, {"message": "Invalid username or password credentials"}
