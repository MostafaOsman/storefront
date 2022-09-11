from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from core.models import User
from store.pagination import DefaultPagination
from .models import Cart, Order, Product, OrderItem, Collection, Review, CartItem, Customer
from .serializers import CreateOrderSerializer,  OrderItemSerializer, AddCartItemSerializer, CartSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, CartItemSerializer, UpdateCartItemSerializer,CustomerSerializer, OrderSerializer
from .filters import ProductFilter
from .permissions import FUllDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission

# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['collection_id','unit_price']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes  = [IsAdminOrReadOnly]


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
    


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method== 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return  UpdateCartItemSerializer
        return CartItemSerializer    


    def get_serializer_context(self):
        #Returns a dictionary containing any extra context that should be supplied to the serializer.
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
         return CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])\
            .select_related('product')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')


    @action(detail=False, methods = ['GET','PUT'], permission_classes = [IsAuthenticated])
    def me(self, request):
            (customer, created)= Customer.objects.get_or_create(user_id= request.user.id)
            if request.method == 'GET':
                serializer = CustomerSerializer(customer)
                return Response(serializer.data)
            elif request.method== 'PUT':
                serializer = CustomerSerializer(customer,data=request.data) 
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        


class OrderViewSet(ModelViewSet):


    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer= CreateOrderSerializer(data= request.data,context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order= serializer.save()
        serializer= OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer     

    def get_queryset(self):
        user= self.request.user
        if user.is_staff:
            return Order.objects.all()

        (customer_id, created) = Order.objects.only('id').get_or_create(user_id= user.id)
        return Order.objects.filter(customer_id = customer_id)



class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.prefetch_related('items__product').all()
    serializer_class = OrderItemSerializer



