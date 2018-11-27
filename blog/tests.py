import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import BlogPost,Author


# Create your tests here.

def create_post(days=0,minutes=0,seconds=0,title="Title",body="body of post"):
    time = timezone.now() + datetime.timedelta(days=days,minutes=minutes,seconds=seconds)
    author = Author.objects.create(name="Japhy")
    return BlogPost.objects.create(title=title,body=body,pub_date=time,author=author)

class BlogPostModelTests(TestCase):

    def test_was_published_today_with_future_post(self):
        """
        was_published_today() returns False for questions whose pub_date is in the future.
        """
        future_post = create_post(days=30)
        self.assertIs(future_post.was_published_today(), False)
        
    def test_was_published_today_with_old_post(self):
        """
        was_published_today() returns False for questions whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_post = create_post(days=-1,seconds=-1)
        self.assertIs(old_post.was_published_today(), False)
        
    def test_was_published_today_with_recent_question(self):
        """
        was_published_today() returns True for questions whose pub_date is within the last day.
        """
        recent_post = create_post(days=-1,seconds=1)
        self.assertIs(recent_post.was_published_today(), True)

        
class PostIndexViewTests(TestCase):

    def test_no_posts(self):
        """If no posts exist, an appropriate message is displayed."""
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No blogposts are available.")
        self.assertQuerysetEqual(response.context['blogposts'],[])  
        
    def test_past_post(self):
        """Posts with a pub_date in the past are displayed on the index page."""
        create_post(days=-30,title="past post")
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['blogposts'], ['<BlogPost: past post>'])
        
    def test_future_question(self):
        """Posts with a pub_date in the future aren't displayed on the index page."""
        create_post(title="future post", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, "No blogposts are available.")
        self.assertQuerysetEqual(response.context['blogposts'], [])
    
    def test_future_and_past_posts(self):
        """Even if both past and future posts exist, only past posts are displayed."""
        create_post(title="past post", days=-30)
        create_post(title="future post", days=30)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['blogposts'], ['<BlogPost: past post>'])

    def test_two_past_posts(self):
        """The questions index page may display multiple posts."""
        create_post(title="past post 1", days=-30)
        create_post(title="past post 2", days=-5)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['blogposts'],['<BlogPost: past post 2>', '<BlogPost: past post 1>'])
        
        
class PostDetailViewTests(TestCase):

    def test_future_post(self):
        """The detail view of a post with a pub_date in the future returns a 404 not found."""
        future_post = create_post(title='future post', days=5)
        url = reverse('blog:blogpost', args=(future_post.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_post(self):
        """The detail view of a post with a pub_date in the past displays the question's text."""
        past_post = create_post(title='past post', days=-5)
        url = reverse('blog:blogpost', args=(past_post.id,))
        response = self.client.get(url)
        self.assertContains(response, past_post.title)


class PostSearchViewTests(TestCase):

    def test_future_post(self):
        """Posts with a pub_date in the future aren't displayed in the search results."""
        future_post = create_post(title="future post", days=5)
        url = reverse('blog:search_results')
        response = self.client.post(url,{'search':'future post'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['blogposts'],[])
  
    def test_search_in_title(self):
        """Posts with the search string in their title are displayed in the searh results."""
        future_post = create_post(title="past post", days=-5)
        url = reverse('blog:search_results')
        response = self.client.post(url,{'search':'past post'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['blogposts'],['<BlogPost: past post>'])
  
    def test_search_in_body(self):
        """Posts with the search string in their body are displayed in the searh results."""
        future_post = create_post(title="Title", body="past post", days=-5)
        url = reverse('blog:search_results')
        response = self.client.post(url,{'search':'past post'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['blogposts'],['<BlogPost: Title>'])
