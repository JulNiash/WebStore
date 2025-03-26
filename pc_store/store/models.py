from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Менеджер для логического удаления
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


# Абстрактная базовая модель
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)


# Модель бренда
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Модель магазина
class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Абстрактная модель товара
class ProductBase(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# Конкретные модели товаров
class Motherboard(ProductBase):
    chipset = models.CharField(max_length=255)
    socket = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)


class Processor(ProductBase):
    ghz = models.FloatField()
    cores = models.IntegerField()
    cache = models.IntegerField()


class GraphicCard(ProductBase):
    gb = models.IntegerField()
    memory_type = models.CharField(max_length=255)


class RAM(ProductBase):
    capacity = models.IntegerField()
    memory_type = models.CharField(max_length=255)
    mhz = models.FloatField()


class Storage(ProductBase):
    capacity = models.IntegerField()
    interface = models.CharField(max_length=255)


class PowerSupply(ProductBase):
    wattage = models.IntegerField()
    modular = models.BooleanField()


class Case(ProductBase):
    height = models.IntegerField()
    width = models.IntegerField()
    depth = models.IntegerField()


# Модель предложения (товар в магазине)
class Offer(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE, null=True, blank=True, related_name="motherboard_offers")
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE, null=True, blank=True, related_name="processor_offers")
    graphic_card = models.ForeignKey(GraphicCard, on_delete=models.CASCADE, null=True, blank=True, related_name="graphic_card_offers")
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE, null=True, blank=True, related_name="ram_offers")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, null=True, blank=True, related_name="storage_offers")
    power_supply = models.ForeignKey(PowerSupply, on_delete=models.CASCADE, null=True, blank=True, related_name="power_supply_offers")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True, related_name="case_offers")

    def get_product(self):
        return (
            self.motherboard or self.processor or self.graphic_card or
            self.ram or self.storage or self.power_supply or self.case
        )

    def __str__(self):
        return f"{self.get_product()} - {self.store.name} ({self.price}$)"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    is_seller = models.BooleanField(default=True)  # Всегда True, раз есть запись

    def __str__(self):
        return f"Продавец: {self.user.username}"


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="basket")

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)  # Связь с товаром в магазине
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.offer.price * self.quantity