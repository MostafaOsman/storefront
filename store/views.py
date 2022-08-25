from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from store.pagination import DefaultPagination
from .models import Cart, Product, OrderItem, Collection, Review
from .serializers import CartSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter

# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['collection_id','unit_price']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields= ['title','description']
    ordering_fields = ['unit_price','last_update']
    def get_serializer_context(self):
            return {'request': self.request}

    def delete(self, request, pk):
        product= get_object_or_404(Product, pk=pk)
        if product.orderitems.count()> 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order'})
        product.delete()



    # def destroy(self, request, *args, **kwargs):
    #     if OrderItem.objects.filter(product_id= kwargs['pk']).count()>0:
    #         return Response({'error':'Product cannot be deleted because it is associated with order item.'})
    #     return super().destroy(request, *args, **kwargs)  



class CollectionViewSet(ModelViewSet):
    queryset= Collection.objects.annotate(products_count= Count('featured_product')).all() 
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
            return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(featured_product_id= kwargs['pk']).count()>0:
            return Response({'error':'Collection cannot be deleted because it is associated with a product.'})
        return super().destroy(request, *args, **kwargs)      



class ReviewViewSet(ModelViewSet):

    serializer_class= ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id= self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}     



class CartViewSet(ModelViewSet):

    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class= CartSerializer
    




