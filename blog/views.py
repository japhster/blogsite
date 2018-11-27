from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Author, BlogPost, Comment

import markdown

def get_author(name):
    try:
        author = Author.objects.all().get(name=name)
    except Author.DoesNotExist:
        author = Author.objects.create(name=name)

    return author

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'blogposts'
    
    def get_queryset(self):
        """return the 10 last published blogposts won't include those set to be published in the future"""
        return BlogPost.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]     

def search_results(request):
    search_string = request.POST["search"]
    q1 = BlogPost.objects.filter(body__icontains=search_string,pub_date__lte=timezone.now())
    q2 = BlogPost.objects.filter(title__icontains=search_string,pub_date__lte=timezone.now())
    relevant_posts = q1.union(q2).order_by("-pub_date")
    return render(request, "blog/index.html", {"blogposts": relevant_posts})

def blogpost(request, post_id):
    queryset = BlogPost.objects.filter(pub_date__lte=timezone.now())
    blogpost = get_object_or_404(queryset,pk=post_id)
    print(blogpost.comment_set.all())
    comments = blogpost.comment_set.all().order_by("pub_date")
    return render(request, "blog/post.html", {"blogpost": blogpost, "body": markdown.markdown(blogpost.body), "comments":comments})

def deleted(request, post_id):
    blogpost = get_object_or_404(BlogPost,pk=post_id)
    print(blogpost.author.name, request.user.username)
    if blogpost.author.name == request.user.username:
        print("hmm")
        title = blogpost.title
        body = blogpost.body
        blogpost.delete()
        return render(request, "blog/deleted.html", {"title": title,"body": body})
    else:
        return HttpResponseRedirect(reverse('blog:blogpost', args=(post_id,)))


class EditPostView(LoginRequiredMixin, generic.edit.UpdateView):
    model = BlogPost
    fields = ['title','body']
    template_name = 'blog/edit.html'

class NewPostView(LoginRequiredMixin, generic.edit.CreateView):
    model = BlogPost
    fields = ['title','body']
    template_name = 'blog/new.html'

def change(request, post_id):
    blogpost = get_object_or_404(BlogPost, pk=post_id)
    blogpost.title = request.POST['title']
    blogpost.body = request.POST['body']
    blogpost.pub_date = timezone.now()
    blogpost.save()
    return HttpResponseRedirect(reverse('blog:blogpost', args=(post_id,)))


class OwnedPostsByUserView(LoginRequiredMixin,generic.ListView):
    template_name = 'blog/ownposts.html'
    context_object_name = 'blogposts'
    
    def get_queryset(self):
        author = get_author(self.request.user.username)
        return author.blogpost_set.all().order_by("-pub_date")
        

class OwnedCommentsByUserView(LoginRequiredMixin,generic.ListView):
    template_name = 'blog/owncomments.html'
    context_object_name = 'comments'
    
    def get_queryset(self):
        author = get_author(self.request.user.username)
        print(author.comment_set.all()[1].post.id)
        return author.comment_set.all().order_by("-pub_date")
    
    
def create(request):
    title = request.POST['title']
    body = request.POST['body']
    pub_date = timezone.now()
    author = get_author(request.user.username)
    new_post = BlogPost(title=title,body=body,author=author)
    new_post.save()
    return HttpResponseRedirect(reverse('blog:blogpost', args=(new_post.pk,)))
    
def comment(request, post_id):
    body = request.POST['body']
    pub_date = timezone.now()
    blogpost = get_object_or_404(BlogPost, pk=post_id)
    author = get_author(request.user.username)
    new_comment = Comment(body=body, pub_date=pub_date, author=author, post=blogpost)
    new_comment.save()
    return HttpResponseRedirect(reverse('blog:blogpost', args=(post_id,)))
    
def edit_comment(request,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.body = request.POST['body']
    comment.save()
    return HttpResponseRedirect(reverse('blog:blogpost', args=(comment.post.id,)))
    
def deleted_comment(request, comment_id):
    comment = get_object_or_404(Comment,pk=comment_id)
    if comment.author.name == request.user.username:
        comment.delete()        
    return HttpResponseRedirect(reverse('blog:blogpost', args=(comment.post.id,)))

