from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"

    def get_queryset(self, *args, **kwargs):
        return Post.published.all()
    

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     import pdb; pdb.set_trace()
    #     context['now'] = timezone.now()
    #     return context

class DetailPostView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"