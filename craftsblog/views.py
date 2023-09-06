from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Post, CATEGORY, Comment
from django.db.models import Count
from .forms import CommentForm
import random

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    context_object_name = "post_list"
    # template_name = "index.html"
    paginate_by = 6


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())

        
        # max_likes = Post.objects.annotate(num_likes=Count('likes')).latest('num_likes')
        # context['top_posts'] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[1:5]
        context['slider_posts'] = random.sample(items, 3)
        context['top_posts'] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[1:5]
        context['featured_post'] = Post.objects.annotate(num_likes=Count('likes')).latest('num_likes')
        context['categories'] = CATEGORY
        # context['number_of_comments'] = Post.objects.annotate(number_of_comments=Count('comments', filter=Q(comments__approved=True)))
        # context['number_of_comments'] = Post.objects.annotate(number_of_comments=Count('comments', filter=Q(comments__approved=True)))
        # context['number_of_comments'] = items.comments.all()
               
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
        number_of_comments = post.comments.filter(approved=True).order_by("-created_on").count()
        not_approved_posts = post.comments.filter(approved=False)

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        comment_form = CommentForm()

        return render(
            request,
            "item.html",
            {
                "post": post,
                "comments": comments,
                "number_of_comments": number_of_comments,
                "categories": CATEGORY,
                "commented": not_approved_posts,
                "liked": liked,
                "top_posts": top_posts,
                "comment_form": comment_form,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        top_posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[0:5]
        comments = post.comments.filter(approved=True).order_by("-created_on")
        not_approved_posts = post.comments.filter(approved=False)

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.user_name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            
            return HttpResponseRedirect(reverse('item', args=[slug]))
        else:
            comment_form = CommentForm()

        return render(
            request,
            "item.html",
            {
                "post": post,
                "comments": comments,
                "number_of_comments":comments.count(),
                "categories": CATEGORY,
                "commented": not_approved_posts,
                "liked": liked,
                "top_posts": top_posts,
                "comment_form": comment_form,
            },
        )


class ItemLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id = request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('item', args=[slug]))
