from django.urls import path

from . import views

app_name = "collector"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:card_id>/', views.card, name='card'),
    path('buy_card/<int:card_id>', views.buy_card, name="buy_card"),
    path('buy_pack/', views.buy_pack, name="buy_pack"),
    path('search_results/', views.search_results, name="search_results"),
    path('my_collection/', views.my_collection, name="my_collection"),
    path('new_card/', views.NewCardView.as_view(), name="new_card"),
    path('create/', views.create, name='create'),
    path('collect/', views.collect, name="collect"),
]
