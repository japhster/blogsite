from django.contrib import admin

from .models import Author,BlogPost,Comment

# Register your models here.

#admin.site.register(Author)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    classes = ['collapse']

class BlogPostInline(admin.TabularInline):
    model = BlogPost
    extra = 0
    classes = ['collapse']
    
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name','join_date']
    inlines = [BlogPostInline,CommentInline]
    list_display = ('name','join_date','joined_recently')
    list_filter = ['join_date']
    search_fields = ['name']
    
admin.site.register(Author, AuthorAdmin)
