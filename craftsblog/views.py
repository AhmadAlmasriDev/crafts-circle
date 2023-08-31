from django.shortcuts import render, get_object_or_404 
from django.views import generic, View
from .models import Post
from django.db.models import Count


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    context_object_name = "post_list"
    # template_name = "index.html"
    paginate_by = 8

    def most_liked(self):
        return Post.objects.annotate(num_likes=Count('likes')).order_by('num_likes')

    def get_template_names(self):
        if self.request.htmx:

            print(self.most_liked())
            return "partials/post_list_items.html"
        return "index.html"

   

class PostDetail(View):
    

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "item.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked
            },
        )

        