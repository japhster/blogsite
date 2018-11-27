import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)
    join_date = models.DateTimeField('join date', default=timezone.now)
    
    def joined_recently(self):
        now = timezone.now()
        return now >= self.join_date >= now - datetime.timedelta(days=30)
    
    def __str__(self):
        return self.name
        
    joined_recently.admin_order_field = 'join_date'
    joined_recently.boolean = True
    joined_recently.short_description = 'Joined recently?'

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def was_published_today(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)
        
    def format_published(self): 
        if self.was_published_today():
            return "at " + self.pub_date.strftime("%H:%M")
        
        return "on " + self.pub_date.strftime("%d/%m/%y")
        
    def __str__(self):
        return self.title
        
    was_published_today.admin_order_field = 'pub_date'
    was_published_today.boolean = True
    was_published_today.short_description = 'Published recently?'
        
class Comment(models.Model):
    body = models.TextField(max_length=2000)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    
    def was_published_today(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)
        
    def format_published(self): 
        print()
        if self.was_published_today():
            return "at " + self.pub_date.strftime("%H:%M")
        
        return "on " + self.pub_date.strftime("%d/%m/%y")
        
    def __str__(self):
        return "Comment on: " + self.post.title
