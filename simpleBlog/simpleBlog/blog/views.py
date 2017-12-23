from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        return Post.published.all()


class DetailPostView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"