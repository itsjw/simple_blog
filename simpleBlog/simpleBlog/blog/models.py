from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


# Model Managers
class PostPublishedManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(PostPublishedManager, self).get_queryset(
            *args, **kwargs).filter(status="published")

# Models


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "draft"),
        ("published", "published")
    )

    # managers
    published = PostPublishedManager()
    objects = models.Manager()
    # fields

    author = models.ForeignKey(User, on_delete=models.PROTECT)

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-publish"]

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,
                                                 self.publish.strftime("%m"),
                                                 self.publish.strftime("%d"),
                                                 self.slug])

    def __str__(self):
        return self.title
