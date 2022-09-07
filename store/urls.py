from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework_nested import routers
 
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet
from pprint import pprint



router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,'products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet,'Cart')
router.register('customers', views.CustomerViewSet,'Customer')
router.register('orders',views.OrderViewSet,'orders')


products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-reviews')


carts_router = routers.NestedDefaultRouter(router, 'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename = 'cart-items')

orders_router = routers.NestedDefaultRouter(router,'orders',lookup = 'order')
orders_router.register('items',views.OrderItemViewSet,basename = 'order-items')


#URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls

