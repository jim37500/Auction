from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    watch_list = models.ManyToManyField("Listing", related_name="watchlist", blank=True)
    


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", default=None)
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now=True)
    img_url = models.URLField()
    category = models.CharField(max_length=64, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", default=None)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=8)
    count = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.product} {self.price}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author", default=None)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f""


