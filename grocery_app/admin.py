from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_tag')
    search_fields = ('name',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height:60px; max-width:60px;" />'
        return ""
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'order_date', 'status', 'total_amount')
    list_filter = ('status', 'order_date')
    search_fields = ('customer_name', 'customer_email')
    inlines = [OrderItemInline]
