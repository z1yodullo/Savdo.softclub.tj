from .models import Product,Category
from .serializer import ProductSerializer,CategorySerializer
from .task import product_created
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache
from rest_framework.views import APIView

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