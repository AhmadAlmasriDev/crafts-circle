from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Post, CATEGORY, Comment, ContactMessage
from django.db.models import Count
from .forms import CommentForm, ContactMessageForm, AddItemForm
from django.utils.text import slugify
import random

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    context_object_name = "post_list"
    # template_name = "index.html"
    paginate_by = 4


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())

        context['slider_posts'] = random.sample(items, 5)
        context['top_posts'] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[1:5]
        context['featured_post'] = Post.objects.annotate(num_likes=Count('likes')).latest('num_likes')
        context['categories'] = CATEGORY
        
               
        return context

    def get_template_names(self):
        if self.request.htmx:
            
            return "partials/post_list_items.html"
           
        return "index.html"
        

class CategoryFilter(generic.ListView):
    model = Post


    # def get(self, request, *args, **kwargs):
    #     category = kwargs['category']
        
    #     queryset = Post.objects.filter(category=category).order_by("-created_on")
    #     return queryset


    # def get_queryset(self):
    #     category1 = self.request.GET.get('category')
    #     print(category1)
    #     queryset = Post.objects.filter(category=category1).order_by("-created_on")
    #     return queryset


    # context_object_name = "post_list"
    # template_name = "index.html"
    paginate_by = 4


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        
        category = self.kwargs['category']
        
        queryset = Post.objects.filter(category=category).order_by("-created_on")

        context['slider_posts'] = random.sample(items, 3)
        context['top_posts'] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[1:5]
        context['featured_post'] = Post.objects.annotate(num_likes=Count('likes')).latest('num_likes')
        context['categories'] = CATEGORY
        context['post_list'] = queryset
        
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


class AboutPage(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).annotate(num_likes=Count('likes')).order_by('-num_likes')[0:5]
    context_object_name = "sliders"
    template_name = "about.html"
    

class FavoritePage(generic.ListView):
    model = Post
    def get_queryset(self):
        # queryset = Post.objects.filter(author=self.request.user).order_by("-created_on")
        # queryset = Post.objects.filter(liked_by=self.request.user).order_by("-created_on")
        user=self.request.user
        queryset = user.item_likes.all()
        return queryset
    # context_object_name = "post_list"
    paginate_by = 6



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        
        context['top_posts'] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[0:5]
        
        context['categories'] = CATEGORY
                       
        return context

    def get_template_names(self):
        if self.request.htmx:
            
            return "partials/post_list_items.html"
           
        return "favorite.html"
        


class ContactPage(View):
    
    def get(self, request):
        top_posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[0:5]
        
        contact_message_form = ContactMessageForm()

        return render(
            request,
            "contact.html",
            {
                "sliders": top_posts,
                "contact_message_form": contact_message_form,
            },
        )

    def post(self, request):
        top_posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[0:5]
        
        contact_message_form = ContactMessageForm(data=request.POST)
        if contact_message_form.is_valid():
            
            message = contact_message_form.save(commit=False)
            
            message.save()
            
            return HttpResponseRedirect(reverse('contact_page'))
        else:
            contact_message_form = ContactMessageForm()

        return render(
            request,
            "contact.html",
            {
                "sliders": top_posts,
                "contact_message_form": contact_message_form,
            },
        )

class AddItem(View):
    
    def get(self, request):
              
        add_item_form = AddItemForm()

        return render(
            request,
            "add_item.html",  
            {
                "add_item_form": add_item_form,
                },
        )

    def post(self, request):
        add_item_form = AddItemForm(request.POST, request.FILES)        
       
        if add_item_form.is_valid():
            add_item_form.instance.author = request.user
            add_item_form.instance.slug = slugify(request.POST.get('title'))
            item = add_item_form.save(commit=False)
            item.save()

           
            
            return HttpResponseRedirect(reverse('add_item'))
        else:
            add_item_form = AddItemForm()

        return render(
            request,
            "add_item.html",
            {
                
                "add_item_form": add_item_form,
            },
        )

