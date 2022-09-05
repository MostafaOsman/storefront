from django.contrib import admin, messages

from tags.models import TaggedItem
from . import models
from django.db.models import Count
from django.db.models.query import QuerySet




class InventoryFilter(admin.SimpleListFilter):
    title= 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)



#Register your models here.
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields={
        'slug':['title']
    }

    actions= ['clear_inventory']
    list_display= ['title','unit_price','inventory_status','collection_title']
    list_editable= ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    search_fields= ['title']

    def collection_title(self,product):
        return product.collection.title


    @admin.display(ordering='inventory')
    def inventory_status(self, product):
            if product.inventory < 10:
                return 'Low'
            return 'OK'

    #custom actions
    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset):
        #request: which represents the current http request
        #queryset : which represents the objects the user has selected
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['first_name','last_name','membership']
    search_fields=['first_name','last_name']
    list_editable = ['membership']
    list_select_related= ['user']
    ordering= ['user__first_name','user__last_name']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        return collection.products_count

    def get_queryset(self, request):
         return super().get_queryset(request).annotate(products_count= Count('product'))

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num=1
    max_num=10
    model = models.OrderItem
    extra=0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline] 
    list_display= ['id','placed_at','customer']
   
