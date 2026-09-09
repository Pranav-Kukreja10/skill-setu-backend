from ninja.security import HttpBearer 
import jwt 
from django.conf import settings 
from accounts.models import User 

class JWTAuth(HttpBearer):
    def authenticate(self, request, token): 
        try: 
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id = payload["user_id"]) 
            return user 
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return None