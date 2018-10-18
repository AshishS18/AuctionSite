from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class auction(models.Model):
    LOC = (
        ('BG', 'Bangalore'),
        ('MUM', 'Mumbai'),
        ('DL', 'Delhi'),
    )
    status = (
        ('A', 'Active'),
        ('U', 'Upcoming'),
        ('F', 'Finished'),
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    base_price = models.IntegerField()
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=25)
    status = models.CharField(max_length=1, default='U')
    image = models.FileField(name='image')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['end_time']


class bid(models.Model):
    auctioneer = models.ForeignKey(auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_winning = models.BooleanField(default=False)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amount
