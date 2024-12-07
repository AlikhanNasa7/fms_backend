from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from users.models import CustomUser
from .permissions import IsFarmer, IsBuyer
from rest_framework import viewsets
from .serializers import ProfileSerializer, FarmerSerializer, BuyerSerializer, RegisterSerializer, FarmerFilter
from users.models import Farmer, Buyer
from rest_framework import mixins
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
import jwt
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from datetime import datetime as dt
import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from market.api.serializers import FarmSerializer
from products.api.serializers import ProductSerializer
from products.models import Product
from rest_framework_simplejwt.tokens import AccessToken

SECRET_KEY = settings.SECRET_KEY
class MyTokenObtainSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token['role'] = user.role

        return token


class MyTokenObtainView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]
        access_token = serializer.validated_data["access"]
        access_payload = AccessToken(access_token).payload
        user_id = access_payload.get('user_id')
        user = CustomUser.objects.get(pk=user_id)

        print(1341234)
        has_image = False
        if user.image:
            has_image = True
        if has_image:
            image = "http://127.0.0.1:8000" + str(user.image.url)
            response = Response({
                "success": "Login successful", 
                "access": access_token, 
                "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "image": image
                }
            }, status=status.HTTP_200_OK)
        else:
            response = Response({
                "success": "Login successful", 
                "access": access_token, 
                "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                }
            }, status=status.HTTP_200_OK)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
        )
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return JsonResponse({'detail': 'Refresh token not found'}, status=401)

        try:
            refresh = RefreshToken(refresh_token)

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            access_payload = AccessToken(access_token).payload
            user_id = access_payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)

            response = JsonResponse({
                "success": "Refreshed token", 
                "access": access_token, 
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)
            
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
            )
            
            return response

        except Exception as e:
            return JsonResponse({'detail': 'Invalid refresh token or expired'}, status=401)


class RegisterView(APIView):
    @extend_schema(
        summary="User Registration",
        description="Endpoint to register a new user. Provide a username, email, and password to create an account.",
        request=RegisterSerializer,
        responses={
            201: "User created successfully.",
            400: "Invalid input data.",
        },
    )
    def post(self, request):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenRefreshView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
            access_token = serializer.validated_data["access"]

            response = Response({"success": "Token refreshed"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            return response
        except TokenError as e:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken as e:
            return Response({"error": "Inlaid token"}, status=status.HTTP_403_FORBIDDEN)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"success": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def retrieve(self, request):

        user = request.user
        serializer = self.get_serializer(user)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request):
        user = request.user

        if user.role == 'farmer':
            serializer = FarmerSerializer(user, data=request.data, partial=True)
        elif user.role == 'buyer':
            serializer = BuyerSerializer(user, data=request.data, partial=True)
        # else:
        #     serializer = AdminSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FarmersViewset(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    filter_backends = (DjangoFilterBackend,)  # Enable Django filter
    filterset_class = FarmerFilter  # Apply the FarmerFilter
    search_fields = ['specialization']
    ordering_fields = ['years_of_experience', 'total_farm_area', 'average_performance']
    # renderer_classes = [JSONRenderer]

    def retrieve(self, request, pk=None):
        farmer = Farmer.objects.get(pk=pk)
        farmer_serializer = FarmerSerializer(farmer)
        farms = farmer.farms
        farms_serializer = FarmSerializer(farms, many=True)
        last_10_products = Product.objects.filter(farm_id__farmer_id=farmer).order_by('-created_at')[:10]
        product_serializer = ProductSerializer(last_10_products, many=True)
        return Response({
            'last_products': product_serializer.data, 
            'farms': farms_serializer.data, 
            'farmer_details': farmer_serializer.data
        })
class BuyerViewset(mixins.ListModelMixin, 
                   mixins.RetrieveModelMixin, 
                   viewsets.GenericViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


RESET_PASSWORD_URL = "http://127.0.0.1:8000/api/reset-password/"


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the email from the request body
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Find the user by email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User with this email does not exist")

        # Get the Unix timestamp (seconds since epoch)
        exp_timestamp = (dt.utcnow() + datetime.timedelta(hours=1)).timestamp()
        # Create the token (user_id + timestamp, expires in 1 hour)
        payload = {
            'user_id': str(user.user_id),
            'exp': exp_timestamp,
        }


        try:
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            # Create the reset password link

            reset_link = f"{RESET_PASSWORD_URL}{token}"

            # Send the reset link to the user's email
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n\n{reset_link}',
                settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in your settings.py
                [email]
            )

            # Return a success response (don't disclose user details for security reasons)
            return Response({"message": "Password reset link has been sent to your email"}, status=status.HTTP_200_OK)

        except Exception as e:
            # Return an error response if something goes wrong in generating the token or sending the email
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        


class PasswordResetView(APIView):
    def get(self, request, token, *args, **kwargs):
        """
        Handle GET request to validate the reset token before user proceeds to reset password.
        """

        # Try to decode the JWT token
        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"error": "The link has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # If token is valid, proceed with further actions like displaying the reset form
        return Response({"message": "Token is valid. Proceed to reset your password."}, status=status.HTTP_200_OK)


    def post(self, request, token, *args, **kwargs):
        # Decode the JWT token
        try:
            decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"error": "The link has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract user_id from token (or any other necessary claims)
        user_id = decoded_data.get("user_id")
        if not user_id:
            return Response({"error": "User ID missing in token."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get new password from the request data
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Return success response
        return Response({"message": "Password has been successfully updated.", "UTC_NOW":dt.utcnow().isoformat(), "Expiration date":dt.utcfromtimestamp(decoded_data.get("exp")).isoformat()}, status=status.HTTP_200_OK)
