from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, CollectionViewSet
from pprint import pprint


router = SimpleRouter()
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)
pprint(router.urls)


urlpatterns = [ 
    
path('products/', views.ProductViewSet.as_view()),
path('collections/',views.CollectionViewSet.as_view())
 
]