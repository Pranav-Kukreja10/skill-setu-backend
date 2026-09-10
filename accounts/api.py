import os
import requests
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from ninja import Router
from django.contrib.auth import authenticate
from django.http import HttpRequest
from accounts.models import User
from accounts.schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserProfileOutSchema,
    OAuthUrlOutSchema,
    OAuthLoginInSchema,
    OAuthAuthResponseOut
)
from accounts.security import JWTAuth

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
        access_token = create_access_token(user)
        return 200, {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role,
            "message": "Login successful"
        }
        
    return 401, {"message": "Invalid username or password credentials"}


@router.get("/me", response={200: UserProfileOutSchema, 401: dict}, auth=JWTAuth())
def get_current_user_profile(request: HttpRequest):
    """
    Returns the authenticated user profile, role, avatar, and authentication provider.
    """
    return 200, request.auth


# ---------------------------------------------------------
# OAUTH2 SINGLE SIGN-ON (GOOGLE & GITHUB)
# ---------------------------------------------------------

@router.get("/oauth/urls", response=OAuthUrlOutSchema, auth=None)
def get_oauth_authorization_urls(request: HttpRequest):
    """
    Returns pre-configured Google and GitHub OAuth2 authorization URLs
    for instant client redirect in frontend Single-Page Applications.
    """
    google_client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "demo-google-client-id.apps.googleusercontent.com")
    github_client_id = os.getenv("GITHUB_OAUTH_CLIENT_ID", "demo-github-client-id")
    redirect_uri = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:3000/auth/callback")

    google_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={google_client_id}&redirect_uri={redirect_uri}&response_type=code&"
        f"scope=openid%20email%20profile&access_type=offline&prompt=consent"
    )
    github_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={github_client_id}&redirect_uri={redirect_uri}&scope=user:email"
    )

    return {
        "google_auth_url": google_url,
        "github_auth_url": github_url
    }


def _verify_google_token(token: str) -> dict:
    """Verifies a Google ID token or demo token."""
    if token.startswith("demo_google_"):
        # Resilient pitch demo payload
        parts = token.split("_")
        name_hint = "_".join(parts[2:]) if len(parts) > 2 else "scholar"
        return {
            "email": f"{name_hint}@gmail.com",
            "sub": f"google_{name_hint}_12345",
            "name": f"{name_hint.replace('_', ' ').title()} (Google User)",
            "picture": f"https://api.dicebear.com/7.x/bottts/svg?seed={name_hint}"
        }

    # Live Google Tokeninfo verification
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        return {
            "email": data.get("email"),
            "sub": data.get("sub"),
            "name": data.get("name", ""),
            "picture": data.get("picture", "")
        }
    raise ValueError(f"Invalid Google ID token: {resp.text}")


def _verify_github_token(token_or_code: str) -> dict:
    """Exchanges GitHub OAuth code or token for user details."""
    if token_or_code.startswith("demo_github_"):
        # Resilient pitch demo payload
        parts = token_or_code.split("_")
        name_hint = "_".join(parts[2:]) if len(parts) > 2 else "coder"
        return {
            "email": f"{name_hint}@github.example",
            "sub": f"gh_{name_hint}_67890",
            "name": f"{name_hint.replace('_', ' ').title()} (GitHub Dev)",
            "picture": f"https://avatars.githubusercontent.com/u/{abs(hash(name_hint)) % 10000000}"
        }

    # If code, exchange for access token
    client_id = os.getenv("GITHUB_OAUTH_CLIENT_ID", "")
    client_secret = os.getenv("GITHUB_OAUTH_CLIENT_SECRET", "")
    access_token = token_or_code

    if client_id and client_secret and len(token_or_code) < 30:
        # It's an authorization code
        ex_resp = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": token_or_code
            },
            headers={"Accept": "application/json"},
            timeout=10
        )
        if ex_resp.status_code == 200:
            access_token = ex_resp.json().get("access_token", token_or_code)

    # Fetch GitHub user profile
    user_resp = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}", "Accept": "application/json"},
        timeout=10
    )
    if user_resp.status_code == 200:
        udata = user_resp.json()
        email = udata.get("email")
        if not email:
            # Fetch primary verified email from emails API
            em_resp = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"token {access_token}", "Accept": "application/json"},
                timeout=10
            )
            if em_resp.status_code == 200:
                for em in em_resp.json():
                    if em.get("primary") and em.get("verified"):
                        email = em.get("email")
                        break
        return {
            "email": email or f"{udata.get('login')}@users.noreply.github.com",
            "sub": str(udata.get("id")),
            "name": udata.get("name") or udata.get("login"),
            "picture": udata.get("avatar_url", "")
        }
    raise ValueError(f"Failed to authenticate with GitHub: {user_resp.text}")


@router.post("/oauth/login", response={200: OAuthAuthResponseOut, 400: dict}, auth=None)
def oauth_social_login(request: HttpRequest, payload: OAuthLoginInSchema):
    """
    Unified OAuth2 Single Sign-On (Google & GitHub).
    Verifies token/code, automatically provisions new user accounts with the chosen role,
    and returns a signed Skill Setu JWT access token.
    """
    provider = payload.provider.lower().strip()
    if provider not in ["google", "github"]:
        return 400, {"message": "Unsupported OAuth provider. Allowed providers: 'google', 'github'."}

    try:
        if provider == "google":
            info = _verify_google_token(payload.token_or_code)
            auth_provider = User.AuthProvider.GOOGLE
        else:
            info = _verify_github_token(payload.token_or_code)
            auth_provider = User.AuthProvider.GITHUB
    except Exception as e:
        return 400, {"message": f"OAuth2 Provider Authentication Failed: {str(e)}"}

    email = info.get("email")
    if not email:
        return 400, {"message": "Could not retrieve a verified email address from the OAuth provider."}

    provider_sub = info.get("sub")
    name = info.get("name", "")
    avatar = info.get("picture", "")

    # Look up existing user by email or provider_id
    user = User.objects.filter(email__iexact=email).first()
    is_new = False

    if not user:
        # Auto-provision new account
        base_username = email.split("@")[0].replace(".", "_").replace("+", "_")
        username = base_username
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{suffix}"
            suffix += 1

        chosen_role = payload.role.upper() if payload.role and payload.role.upper() in User.Role.values else User.Role.STUDENT
        user = User.objects.create(
            username=username,
            email=email,
            first_name=name.split()[0] if name else username,
            last_name=" ".join(name.split()[1:]) if name and len(name.split()) > 1 else "",
            role=chosen_role,
            auth_provider=auth_provider,
            provider_id=provider_sub,
            avatar_url=avatar
        )
        user.set_unusable_password()
        user.save()
        is_new = True
    else:
        # Existing user: link OAuth provider details and update avatar if empty
        updated = False
        if not user.provider_id:
            user.provider_id = provider_sub
            updated = True
        if not user.avatar_url and avatar:
            user.avatar_url = avatar
            updated = True
        if updated:
            user.save(update_fields=["provider_id", "avatar_url"])

    token = create_access_token(user)

    return 200, {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "email": user.email,
        "avatar_url": user.avatar_url or avatar,
        "is_new_user": is_new,
        "auth_provider": user.auth_provider,
        "message": "OAuth authentication successful. Welcome to Skill Setu!"
    }
