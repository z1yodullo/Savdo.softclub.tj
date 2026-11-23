from django.urls import path,include
# from .views import productlist,get_by_id,update,delete
from .views import Products,Categories,CategoryListView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)





route=DefaultRouter()
route.register('products',Products)
route.register('categories',Categories)

urlpatterns=[
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    # path('',productlist),
    # path('get_one/<int:pk>/',get_by_id),
    # path('update/<int:pk>/',update),
    # path('delete/<int:pk>/',delete),
    path('token/',TokenObtainPairView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('category-list/',CategoryListView.as_view()),
    path('',include(route.urls))
]   