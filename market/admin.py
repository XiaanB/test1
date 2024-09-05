from django.contrib import admin
from .models import SupermarketChain, Store, Product, PriceHistory, CustomUser, UserStorePreference

# Inline class to manage related models in the admin interface
class StoreInline(admin.TabularInline):
    model = Store
    extra = 1
    fields = ('store_name', 'store_region', 'chain')

# Register your models here
@admin.register(SupermarketChain)
class SuperAdmin(admin.ModelAdmin):
    list_display = ("chain_id", "chain_name")
    list_filter = ("chain_name",)
    search_fields = ["chain_name"]
    list_editable = ('chain_name',)
    ordering = ["chain_name"]
    fieldsets = (
        ("Supermarket Chain Information", {'fields': ("chain_name",)}),
    )
    inlines = [StoreInline]  # Inline added here to show related stores

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("store_id", 'store_name', 'store_address', 'store_region', 'chain') 
    list_filter = ("store_name", "store_region", "chain")
    search_fields = ["store_name", "store_region", "chain__chain_name"]
    ordering = ["store_name"]
    fieldsets = (
        ("Store Information", {'fields': ("store_name", "store_address", "store_region", "chain")}),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_id", 'product_name', 'unit_type', 'store', 'product_code', 'unit_price', 'on_sale')   
    list_filter = ("product_name", "store", "on_sale")
    search_fields = ["product_name", "product_code", "store__store_name"]
    ordering = ["product_name", "product_code"]
    fieldsets = (
        ("Product Details", {'fields': ("product_name", "product_code", "store", "unit_type", "unit_price", "on_sale")}),
    )

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("price_history_id", "product", 'date', 'price', 'on_sale')   
    list_filter = ("product", "date", "on_sale")
    search_fields = ["product__product_name", "price", 'on_sale']
    ordering = ["product", "date"]
    fieldsets = (
        ("Price History Details", {'fields': ("product", "price", "on_sale")}),
    )

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", 'email', 'user_type') 
    list_filter = ("username", "user_type")
    search_fields = ["username", "email", "user_type"]
    ordering = ["username", "user_type"]
    fieldsets = (
        ("User Details", {'fields': ("username", "name", "email", "user_type")}),
    )

@admin.register(UserStorePreference)
class UserStorePreferenceAdmin(admin.ModelAdmin):
    list_display = ("usp_id", "user", 'store')   
    list_filter = ("user", "store")
    search_fields = ["user__username", "store__store_name"]
    ordering = ["user", "store"]
    fieldsets = (
        ("User Store Preference", {'fields': ("user", "store")}),
    )
