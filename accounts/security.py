from ninja.security import HttpBearer 
import jwt 
from django.conf import settings 
from accounts.models import User 

class JWTAuth(HttpBearer):
    def authenticate(self, request, token): 
        try: 
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"]) 
            return user 
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None

class RecruiterAuth(JWTAuth):
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        if user and user.role in [User.Role.RECRUITER, User.Role.ADMIN]:
            return user
        return None

class StudentAuth(JWTAuth):
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        if user and user.role in [User.Role.STUDENT, User.Role.CANDIDATE, User.Role.ADMIN]:
            return user
        return None

# Alias CandidateAuth to StudentAuth for seamless candidate/job-seeker parity
CandidateAuth = StudentAuth

class AcademiaAuth(JWTAuth):
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        if user and user.role in [User.Role.ACADEMIA, User.Role.ADMIN]:
            return user
        return None