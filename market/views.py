import json
from django.http import JsonResponse
# from .models import PriceHistory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import SupermarketChain, Store, Product, PriceHistory, CustomUser, UserStorePreference
from django.db.models import Q
from django.shortcuts import render


#SupermarketChain Views
# List all SupermarketChains
class SupermarketChainListView(ListView):
    model = SupermarketChain
    template_name = 'market/supermarketchain_list.html'

# View details of a SupermarketChain
class SupermarketChainDetailView(DetailView):
    model = SupermarketChain
    template_name = 'market/supermarketchain_detail.html'

# Create a new SupermarketChain
class SupermarketChainCreateView(CreateView):
    model = SupermarketChain
    fields = ['chain_name']
    template_name = 'market/supermarketchain_form.html'

# Update an existing SupermarketChain
class SupermarketChainUpdateView(UpdateView):
    model = SupermarketChain
    fields = ['chain_name']
    template_name = 'market/supermarketchain_form.html'

# Delete a SupermarketChain
class SupermarketChainDeleteView(DeleteView):
    model = SupermarketChain
    template_name = 'market/supermarketchain_confirm_delete.html'
    success_url = reverse_lazy('supermarket-chain-list')

#Store Views
# List all Stores
class StoreListView(ListView):
    model = Store
    template_name = 'market/store_list.html'
    context_object_name = 'stores'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        region = self.request.GET.get('region')
        
        if query:
            queryset = queryset.filter(
                Q(store_name__icontains=query) |
                Q(store_address__icontains=query)
            )
        
        if region:
            queryset = queryset.filter(store_region__icontains=region)
        
        return queryset

class StoreListView(ListView):
    model = Store
    template_name = 'market/store_list.html'
    context_object_name = 'stores'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        region = self.request.GET.get('region')
        
        if query:
            queryset = queryset.filter(
                Q(store_name__icontains=query) |
                Q(store_address__icontains=query)
            )
        
        if region:
            queryset = queryset.filter(store_region__icontains=region)
        
        return queryset

    

# View details of a Store
class StoreDetailView(DetailView):
    model = Store
    template_name = 'market/store_detail.html'

# Create a new Store
class StoreCreateView(CreateView):
    model = Store
    fields = ['store_name', 'store_address', 'store_region', 'chain']
    template_name = 'market/store_form.html'

# Update an existing Store
class StoreUpdateView(UpdateView):
    model = Store
    fields = ['store_name', 'store_address', 'store_region', 'chain']
    template_name = 'market/store_form.html'

# Delete a Store
class StoreDeleteView(DeleteView):
    model = Store
    template_name = 'market/store_confirm_delete.html'
    success_url = reverse_lazy('store-list')

#Product Views
# List all Products
class ProductListView(ListView):
    model = Product
    template_name = 'market/product_list.html'

# View details of a Product
class ProductDetailView(DetailView):
    model = Product
    template_name = 'market/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['price_history'] = PriceHistory.objects.filter(product=product).order_by('date')
        return context
    
# Create a new Product
class ProductCreateView(CreateView):
    model = Product
    fields = ['product_name', 'product_image', 'unit_type', 'store', 'product_code', 'unit_price', 'on_sale']
    template_name = 'market/product_form.html'

# Update an existing Product
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['product_name', 'product_image', 'unit_type', 'store', 'product_code', 'unit_price', 'on_sale']
    template_name = 'market/product_form.html'

# Delete a Product
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'market/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

#PriceHistory Views
# List all PriceHistory records
class PriceHistoryListView(ListView):
    model = PriceHistory
    template_name = 'market/pricehistory_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        product_name = self.request.GET.get('product_name')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if product_name:
            queryset = queryset.filter(product__product_name__icontains=product_name)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset
    

class PriceHistoryDetailView(DetailView):
    model = PriceHistory
    template_name = 'market/pricehistory_detail.html'

# View details of a PriceHistory record
class PriceHistoryDetailView(DetailView):
    model = PriceHistory
    template_name = 'market/pricehistory_detail.html'

# Create a new PriceHistory record
class PriceHistoryCreateView(CreateView):
    model = PriceHistory
    fields = ['product', 'price', 'on_sale']
    template_name = 'market/pricehistory_form.html'

# Update an existing PriceHistory record
class PriceHistoryUpdateView(UpdateView):
    model = PriceHistory
    fields = ['product', 'price', 'on_sale']
    template_name = 'market/pricehistory_form.html'

# Delete a PriceHistory record
class PriceHistoryDeleteView(DeleteView):
    model = PriceHistory
    template_name = 'market/pricehistory_confirm_delete.html'
    success_url = reverse_lazy('pricehistory-list')

#User views
# List all Users
class UserListView(ListView):
    model = CustomUser
    template_name = 'market/user_list.html'

# View details of a User
class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'market/user_detail.html'

# Create a new User
class UserCreateView(CreateView):
    model = CustomUser
    fields = ['name', 'username', 'password', 'email', 'user_type']
    template_name = 'market/user_form.html'

# Update an existing User
class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ['name', 'username', 'password', 'email', 'user_type']
    template_name = 'market/user_form.html'

# Delete a User
class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'market/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')

#UserStorePreference views
# List all UserStorePreferences
class UserStorePreferenceListView(ListView):
    model = UserStorePreference
    template_name = 'market/userstorepreferance_list.html'

# View details of a UserStorePreference
class UserStorePreferenceDetailView(DetailView):
    model = UserStorePreference
    template_name = 'market/userstorepreferance_detail.html'

# Create a new UserStorePreference
class UserStorePreferenceCreateView(CreateView):
    model = UserStorePreference
    fields = ['user', 'store']
    template_name = 'market/userstorepreferance_form.html'

# Update an existing UserStorePreference
class UserStorePreferenceUpdateView(UpdateView):
    model = UserStorePreference
    fields = ['user', 'store']
    template_name = 'market/userstorepreferance_form.html'

# Delete a UserStorePreference
class UserStorePreferenceDeleteView(DeleteView):
    model = UserStorePreference
    template_name = 'market/userstorepreferance_confirm_delete.html'
    success_url = reverse_lazy('userstorepreferance-list')

