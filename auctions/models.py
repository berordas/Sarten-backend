from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name


class Auction(models.Model):

    auctioneer = models.ForeignKey(
        CustomUser, related_name="auctions", on_delete=models.CASCADE
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name="auctions", on_delete=models.CASCADE
    )
    thumbnail = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name="bids", on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.CharField(max_length=100)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.bidder} - {self.price}€"
    

class Comment(models.Model):
    auction = models.ForeignKey(Auction, related_name="comment", on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)  
    modification_date = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.user} - {self.comment}€"
    
class Rating(models.Model):
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Puntuación del 1 al 5"
    )
    user = models.CharField(max_length=100)

    auction = models.ForeignKey(
        Auction,
        related_name="ratings",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-value",)

    def __str__(self):
        return f"{self.user} - {self.value}★"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar la puntuación media de la subasta
        ratings = Rating.objects.filter(auction=self.auction)
        avg_rating = ratings.aggregate(models.Avg('value'))['value__avg']
        self.auction.rating = avg_rating
        self.auction.save()
    



