
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from landDetails.models import LandDetails
from .serializers import LandDetailSerializer;
from .serializers import UserUpdateSerializer
from rest_framework import generics
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated
from registration.models import CustomUser
from .serializers import CustomUserSerializer, LandSearchSerializer, LandMapSerializer
from rest_framework.permissions import AllowAny

# Theee view for listing and creating LandDetails
class LandDetailList(APIView):
    def get(self, request, format=None):
        # Retrieve all LandDetails from the database
        properties = LandDetails.objects.all()
        serializer = LandDetailSerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Create a new LandDetail instance
        serializer = LandDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Class-based view for retrieving, updating, and deleting individual LandDetails
class LandDetailDetail(APIView):
    def get_object(self, pk):
        # Try to retrieve a LandDetail instance by primary key
        try:
            return LandDetails.objects.get(pk=pk)
        except Exception:
            raise NotFound('The Land details do not exist')

    def get(self, request, pk, format=None):
        # Retrieve the LandDetail instance
        land_detail = self.get_object(pk)
        if land_detail is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LandDetailSerializer(land_detail)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # Update an existing LandDetail instance
        land_detail = self.get_object(pk)
        if land_detail is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LandDetailSerializer(land_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# ViewSet for listing LandDetails based on search criteria
class LandSearchViewList(viewsets.ReadOnlyModelViewSet):
    queryset = LandDetails.objects.all()
    serializer_class = LandSearchSerializer

# ViewSet for managing LandDetails with latitude and longitude
class LandMapViewSetList(viewsets.ModelViewSet):
    queryset = LandDetails.objects.all()
    serializer_class = LandMapSerializer

    def get_queryset(self):
        # Filter queryset to include only records with latitude and longitude
        return LandDetails.objects.filter(latitude__isnull=False, longitude__isnull=False)

    def perform_create(self, serializer):
        # Override create method to set latitude and longitude
        serializer.save(latitude=self.request.data.get('latitude'), longitude=self.request.data.get('longitude'))

# Thheee view for retrieving and updating individual LandDetails
class LandMapSingleAPIView(APIView):
    def get(self, request, pk=None, format=None):
        land_parcel_number = request.query_params.get('land_parcel_number')
        
        if pk:
            # Filter by primary key if provided
            try:
                land_detail = LandDetails.objects.get(pk=pk)
            except LandDetails.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        elif land_parcel_number:
            # Filtering by land parcel number if provided
            try:
                land_detail = LandDetails.objects.get(land_parcel_number=land_parcel_number)
            except LandDetails.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'No identifier provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LandMapSerializer(land_detail)
        return Response(serializer.data)

    def post(self, request, format=None):
        land_parcel_number = request.data.get('land_parcel_number')
        if not land_parcel_number:
            return Response({"error": "Land parcel number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            land_detail = LandDetails.objects.get(land_parcel_number=land_parcel_number)
        except LandDetails.DoesNotExist:
            return Response({"error": "LandDetail not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if LandDetails.objects.filter(pk=land_detail.pk).exists():
            return Response({"error": "Object with this ID already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LandMapSerializer(land_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(latitude=request.data.get('latitude'), longitude=request.data.get('longitude'))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Generic CreateAPIView for registering new users
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


    def retrieveUsers(self, request, *args, **kwargs):
        # Retrieve a single user by ID
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def createUser(self, request, *args, **kwargs):
        # Creating a new user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ProfileViewSet(APIView):
    
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         serializer = ProfileSerializer(user)
#         return Response(serializer.data)
    

#     def patch(self, request, *args, **kwargs):
#         user = request.user
#         serializer = ProfileSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        try:
            django_logout(request)
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def test_logout(request):
        django_logout(request)
        return HttpResponse("Logged out successfully.")
    


class UserPofileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
