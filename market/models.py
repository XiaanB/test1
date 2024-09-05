from django.db import models
from django.urls import reverse

# Create your models here.
class SupermarketChain(models.Model):
    NEW_WORLD = 'Nw'
    COUNTDOWN = 'Cd'
    PAK_N_SAVE = 'Ps'
    FRESH_CHOICE = 'Fc'

    SUPERMARKET_CHAIN_CHOICES = [
        (NEW_WORLD, 'New World'),
        (COUNTDOWN, 'Countdown'),
        (PAK_N_SAVE, 'Pak n Save'),
        (FRESH_CHOICE, 'Fresh Choice'),
    ]
   
    chain_id = models.AutoField(primary_key=True)
    chain_name = models.CharField(
        max_length=2,
        choices=SUPERMARKET_CHAIN_CHOICES,
        default=COUNTDOWN,
    )

    def __str__(self) -> str:
        return self.get_chain_name_display()

    def get_absolute_url(self):
        return reverse("chain_detail", kwargs={"pk": self.pk})

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=100, help_text="Must be filled in.")
    store_address = models.TextField()
    store_region = models.CharField(max_length=50, help_text="Where in NZ")
    chain = models.ForeignKey(SupermarketChain, on_delete=models.CASCADE, null=True, blank=True, related_name='stores')

    def __str__(self) -> str:
        return self.store_name

    def get_absolute_url(self):
        return reverse("store_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    unit_type = models.CharField(max_length=50)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    product_code = models.CharField(max_length=20, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    on_sale = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name}: ${self.unit_price}"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

class PriceHistory(models.Model):
    price_history_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='price_histories')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    on_sale = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.product_name} on {self.date}: ${self.price}"

    def get_absolute_url(self):
        return reverse("price_history_detail", kwargs={"pk": self.pk})

class CustomUser(models.Model):  # Renamed to avoid clash with Django's User model
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} ({self.name})"

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})

class UserStorePreference(models.Model):
    usp_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='preferred_by')

    def __str__(self):
        return f"Preference {self.usp_id} - {self.user.username} for {self.store.store_name}"

    def get_absolute_url(self):
        return reverse("userstorepreference_detail", kwargs={"pk": self.pk})
