from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication

class JWTAuthentication(BaseJWTAuthentication):
    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is not None:
            user, auth = user_auth_tuple
            # Access the user attribute of the token object
            username = auth['user']
            # Do something with the username
        return user_auth_tuple
