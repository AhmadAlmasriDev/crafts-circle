from django.shortcuts import render, get_object_or_404 
from django.views import generic, View
from .models import Post, CATEGORY
from django.db.models import Count, Max
import random

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    context_object_name = "post_list"
    # template_name = "index.html"
    paginate_by = 8


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())

        
        # max_likes = Post.objects.annotate(num_likes=Count('likes')).latest('num_likes')
        # context['top_posts'] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[1:5]
        context['slider_posts'] = random.sample(items, 3)
        context['top_posts'] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[1:5]
        context['featured_post'] = Post.objects.annotate(num_likes=Count('likes')).latest('num_likes')
        context['categories'] = CATEGORY
               
        return context





    def get_template_names(self):
        if self.request.htmx:
            
            return "partials/post_list_items.html"
           
        return "index.html"
        



class PostDetail(View):
    
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        top_posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[0:5]
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
                "categories": CATEGORY,
                "liked": liked,
                "top_posts": top_posts
            },
        )

        