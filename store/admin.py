from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from django import models


# Register your models here.

class TagInline(GenericTabularInline):
    model = TaggedItem

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
 
    autocomplete_fields = ['collection']
    prepopulated_fields= {
        'slug':['title']
    }
    actions= ['clear_inventory']
    inlines= [TagInline]
    list_display =['title','unit_price',
    'inventory_status','collection_title']

    list_editable = ['unit_price']

    list_filter= ['collection','last_update',InventoryFilter]