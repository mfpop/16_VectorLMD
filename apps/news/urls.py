from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    # Add news_list as an alias to the index view
    path("list/", views.index, name="news_list"),
    # Also add a URL pattern without namespace for compatibility
    path("<int:news_id>/", views.detail, name="detail"),
    path("<int:news_id>/like/", views.like_news, name="like"),
    path("<int:news_id>/dislike/", views.dislike_news, name="dislike"),
    path("<int:news_id>/comment/", views.add_comment, name="add_comment"),
]
