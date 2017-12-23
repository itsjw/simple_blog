from django.contrib import admin
from django.urls import path
from .views import PostListView, DetailPostView


app_name = "blog"


urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         DetailPostView.as_view(), name="post_detail"),
]
