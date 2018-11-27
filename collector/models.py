import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Card(models.Model):
    COMMON = "C"
    RARE = "R"
    EPIC = "E"
    LEGENDARY = "L"
    RARITY_CHOICES = (
        (COMMON, "Common"),
        (RARE, "Rare"),
        (EPIC, "Epic"),
        (LEGENDARY, "Legendary"),
    )
    name = models.CharField(max_length=200)
    rarity = models.CharField(max_length=1,choices=RARITY_CHOICES,default=COMMON)
    description = models.TextField(max_length=2000)
    value = models.IntegerField(default=100)
    
    def owned_by(self, collector_name):
        print(collector_name)
        return self.collector_set.filter(name=collector_name).exists()

    def __str__(self):
        return self.name

class Collector(models.Model):
    name = models.CharField(max_length=200)
    join_date = models.DateTimeField('join date', default=timezone.now)
    collection = models.ManyToManyField(Card)
    last_collected_coins = models.DateTimeField('latest collection', default=timezone.now)
    coins = models.IntegerField(default=0)

    def get_coins_to_collect(self):
        time_since_last_collection = timezone.now() - self.last_collected_coins
        num_coins = int(time_since_last_collection.total_seconds()/60) #coins gained equivalent to number of minutes since last collection
        
        return num_coins

    def has_card(self, card_name):
        return str(self.collection.filter(name=card_name).exists())
 
    def __str__(self):
        return self.name


