from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Product, OrderItem, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models import Count
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer


    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id= kwargs['pk']).count()>0:
            return Response({'error':'Product cannot be deleted because it is associated with order item.'})
        return super().destroy(request, *args, **kwargs)  



class CollectionViewSet(ModelViewSet):
    queryset= Collection.objects.annotate(products_count= Count('featured_product')).all() 
    serializer_class = CollectionSerializer


    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(featured_product_id= kwargs['pk']).count()>0:
            return Response({'error':'Collection cannot be deleted because it is associated with a product.'})
        return super().destroy(request, *args, **kwargs)        