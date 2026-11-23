from .models import Product,Category
from .serializer import ProductSerializer,CategorySerializer
from .task import product_created
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializer import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh = request.data.get('refresh')

        if not refresh:
            return Response(
                {'detail': 'Refresh token required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh)
            token.blacklist()

            return Response(
                {'detail': 'Logout successful'},
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {'detail': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )



class Products(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def perform_create(self, serializer):
        product = serializer.save()
        product_created.delay(product.name)

class Categories(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("categories")

    def perform_update(self, serializer):
        serializer.save()
        cache.delete("categories")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete("categories")

class CategoryListView(APIView):

    def get(self, request):

        categories = cache.get("categories")

        if categories is None:
            categories = CategorySerializer(
                Category.objects.all(),
                many=True
            ).data

            cache.set("categories", categories, 300)

        return Response(categories)