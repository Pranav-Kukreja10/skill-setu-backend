from ninja.security import HttpBearer 
import jwt 
from django.conf import settings 
from accounts.models import User 

class JWTAuth(HttpBearer):
    allowed_roles = None  # None means any authenticated role is accepted

    def authenticate(self, request, token): 
        try: 
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            token_role = payload.get("role")
            
            # Stateless Role Check: Reject unauthorized roles immediately with 0 database queries
            if self.allowed_roles is not None:
                if token_role not in self.allowed_roles:
                    return None

            user = User.objects.only("id", "username", "email", "role", "auth_provider", "avatar_url", "phone_number").get(id=payload["user_id"]) 
            request.jwt_payload = payload
            user.jwt_payload = payload
            return user 
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None

class RecruiterAuth(JWTAuth):
    allowed_roles = [User.Role.RECRUITER, User.Role.ADMIN]

class StudentAuth(JWTAuth):
    allowed_roles = [User.Role.STUDENT, User.Role.CANDIDATE, User.Role.ADMIN]

# Alias CandidateAuth to StudentAuth for seamless candidate/job-seeker parity
CandidateAuth = StudentAuth

class AcademiaAuth(JWTAuth):
    allowed_roles = [User.Role.ACADEMIA, User.Role.ADMIN]