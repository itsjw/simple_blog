from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import EmailPostForm
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


class SharePostView(View):
    form_class = EmailPostForm
    template_name = "blog/post_share.html"

    def get_object(self):
        # post = Post.objects.get(id=self.kwargs["post_id"], status="published")

        return self.post

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs["post_id"], status="published")
        form = self.form_class(request.GET)
        return render(request, self.template_name, {"form": form, "post": self.post})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, id=self.kwargs["post_id"], status="published")
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{} ({}) encourages you to read '{}'".format(cd["name"], cd["email"], post.title)
            message = "Read the post '{}' at the site {}\n\n Comment added by {}: {}".format(
                post.title, post_url, cd["name"], cd["comments"])
            send_mail(subject, message, "aboutmemeabout@gmail.com", [cd["to"]])
            sent = True
        else:
            form = self.form_class
        return render(request, self.template_name, {"post": post, "form": form, "sent": sent})
