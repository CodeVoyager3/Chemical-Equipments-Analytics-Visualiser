from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterView(APIView):
    """User registration endpoint."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        confirm_password = request.data.get('confirm_password', '')
        
        # Validation
        errors = {}
        
        if not username:
            errors['username'] = 'Username is required'
        elif len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
            
        if not email:
            errors['email'] = 'Email is required'
        elif '@' not in email or '.' not in email:
            errors['email'] = 'Invalid email format'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered'
            
        if not password:
            errors['password'] = 'Password is required'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters'
            
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'
        
        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return Response({
                'message': 'User created successfully',
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'errors': {'general': str(e)}}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    """User login validation endpoint."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            return Response({
                'message': 'Login successful',
                'username': user.username
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
