from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from taggit.models import Tag

from .forms import EmailPostForm, CommentPostForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        tag = None
        return Post.published.all()

    def get(self, request, tag_slug=None, *args, **kwargs):
        super(PostListView, self).get(request, tag_slug=None, *args, **kwargs)
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            import pdb; pdb.set_trace()
            self.object_list = self.object_list.filter(tags__in=[tag])
        context = self.get_context_data()
        context["tag"] = tag
        return render(request, self.template_name, context)


class DetailPostView(View):
    model = Post
    template_name = "blog/post_detail.html"
    form_class = CommentPostForm

    def get_object(self, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs["slug"])
        return post

    def get_context_data(self, *args, **kwargs):
        post = self.get_object(*args, **kwargs)
        comments = post.comments.filter(active=True)
        context_data = {"post": post, "comments": comments}
        return context_data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(*args, **kwargs)
        context_data["comment_form"] = self.form_class(request.GET)
        return render(request, self.template_name, context_data)

    def post(self, request, *args, **kwargs):
        context_data = self.get_context_data(*args, **kwargs)
        post = self.get_object(*args, **kwargs)
        comment_form = self.form_class(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = self.form_class
        context_data["form"] = comment_form
        return render(request, self.template_name, context_data)


class SharePostView(View):
    form_class = EmailPostForm
    template_name = "blog/post_share.html"

    def get_object(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs["post_id"], status="published")
        return post

    def get(self, request, *args, **kwargs):
        post = self.get_object(*args, **kwargs)
        form = self.form_class(request.GET)
        return render(request, self.template_name, {"form": form, "post": self.post})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post = self.get_object(*args, **kwargs)
        sent = False
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
