from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Marketplace(models.Model):
    name = models.CharField(max_length=255)
    api_url = models.URLField(default='http://127.0.0.1:8080/api/products/')
    url = models.URLField(default='http://127.0.0.1:8080')
    token = models.CharField(max_length=100, default='sda')
    is_active = models.BooleanField(default=False) 

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def update_average_rating(self):
        # Получение среднего рейтинга с маркетплейсов
        marketplace_ratings = self.marketplaces.all()
        if marketplace_ratings.exists():
            average_rating = marketplace_ratings.aggregate(models.Avg('marketplace_rating'))['marketplace_rating__avg']
            self.average_rating = average_rating
            self.save()
        else:
            self.average_rating = None
            self.save()

class ItemMarketplace(models.Model):
    item = models.ForeignKey(Item, related_name='marketplaces', on_delete=models.CASCADE)
    marketplace = models.ForeignKey(Marketplace, related_name='items', on_delete=models.CASCADE)
    marketplace_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} at {self.marketplace.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.update_average_rating()

    def delete(self, *args, **kwargs):
        item = self.item  #Saving link on item before delt
        super().delete(*args, **kwargs)
        item.update_average_rating()

class Review(models.Model):
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.item.name}"



