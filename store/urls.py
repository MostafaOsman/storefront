from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework_nested import routers
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet
from pprint import pprint



router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,'products')
router.register('collections',views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-reviews')


#URLConf
urlpatterns = router.urls + products_router.urls

