from django.shortcuts import render
from django.views import generic
from .models import Post


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    context_object_name = "post_list"
    # template_name = "index.html"
    paginate_by = 8

    def get_template_names(self):
        if self.request.htmx:
            return "partials/post_list_items.html"
        return "index.html"

