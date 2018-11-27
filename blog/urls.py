from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:post_id>/', views.blogpost, name='blogpost'),
    path('<int:pk>/edit/', views.EditPostView.as_view(), name='edit'),
    path('new/', views.NewPostView.as_view(), name='new'),
    path('<int:post_id>/change/', views.change, name='change'),
    path('create/', views.create, name='create'),
    path('search_results/', views.search_results, name='search_results'),
    path('myposts/', views.OwnedPostsByUserView.as_view(), name='myposts'),
    path('mycomments/', views.OwnedCommentsByUserView.as_view(), name='mycomments'),
    path('<int:post_id>/comment/', views.comment, name='comment'),
    path('<int:post_id>/deleted/', views.deleted, name='deleted'),
    path('<int:comment_id>/editcomment/', views.edit_comment, name='editcomment'),
    path('<int:comment_id>/deletedcomment/', views.deleted_comment, name='deletedcomment'),
    
    
]
