from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views import generic, View
from .models import Post, CATEGORY, Comment, ContactMessage
from django.db.models import Count
from .forms import CommentForm, ContactMessageForm, AddItemForm
from django.utils.text import slugify
from .mixins import CheckManagerMixin
from taggit.models import Tag
from django.contrib import messages
import random

# _____________Index page__________________________________________


class PostList(generic.ListView):
    """
    The home page list of items, in most of the views there
    is additional context for the slider and side panel to work.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        Tag.objects.filter(post=None).delete()
        tags = Tag.objects.all()
        context['slider_posts'] = random.sample(items, 5)
        context['top_posts'] = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[1:5]
        context['featured_post'] = Post.objects.annotate(
            num_likes=Count('likes')
            ).latest(
                'num_likes'
                )
        context['categories'] = CATEGORY
        context['tags'] = tags
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "partials/post_list_items.html"
        return "index.html"

# _____________Category page_______________________________________


class CategoryFilter(generic.ListView):
    """
    The category list of items shown when user clicks on a category.
    """
    model = Post
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs['category']
        queryset = Post.objects.filter(category=category).order_by(
            "-created_on"
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        category = self.kwargs['category']
        tags = Tag.objects.all()

        context['slider_posts'] = random.sample(items, 5)
        context['top_posts'] = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
        context['categories'] = CATEGORY
        context['category'] = category
        context['tags'] = tags
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "partials/post_list_items.html"
        return "index.html"

# _____________Tags page___________________________________________


class Tags(generic.ListView):
    """
    The tags list of items shown when user clicks on a tag.
    """
    model = Post
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_name = self.kwargs['tag']
        queryset = Post.objects.filter(tags__name=tag_name).order_by(
            "-created_on"
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        tag_name = self.kwargs['tag']
        tags = Tag.objects.all()

        context['slider_posts'] = random.sample(items, 5)
        context['top_posts'] = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
        context['categories'] = CATEGORY
        context['tags'] = tags
        context['tag'] = tag_name
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "partials/post_list_items.html"
        return "index.html"

# _____________Item page___________________________________________


class PostDetail(View):
    """
    The detailes page when a user clicks on an item from the list.
    The post method is used for the comments.
    """

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        top_posts = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
        comments = post.comments.filter(approved=True).order_by("-created_on")
        number_of_comments = post.comments.filter(
            approved=True
            ).order_by(
                "-created_on"
                ).count()
        not_approved_posts = post.comments.filter(
            user_name=self.request.user,
            approved=False
            )
        tags = Tag.objects.all()
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
                "tags": tags,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        top_posts = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
        comments = post.comments.filter(approved=True).order_by("-created_on")
        not_approved_posts = post.comments.filter(approved=False)
        tags = Tag.objects.all()
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
                "number_of_comments": comments.count(),
                "categories": CATEGORY,
                "commented": not_approved_posts,
                "liked": liked,
                "top_posts": top_posts,
                "comment_form": comment_form,
                "tags": tags,
            },
        )

# _____________Like item___________________________________________


class ItemLike(View):
    """
    The like functionality for an item is triggered
    when the user clicks the heart icon.
    """

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('item', args=[slug]))

# _____________About page__________________________________________


class AboutPage(generic.ListView):
    """
    The about page.
    """
    model = Post
    items = list(Post.objects.all())
    queryset = random.sample(items, 5)
    context_object_name = "sliders"
    template_name = "about.html"

# _____________Favorite page_______________________________________


class FavoritePage(generic.ListView):
    """
    The favorite page shows the items that the users liked.
    """
    model = Post
    paginate_by = 4

    def get_queryset(self):
        user = self.request.user
        queryset = user.item_likes.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        tags = Tag.objects.all()
        context['top_posts'] = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
        context['section_title'] = 'Favorite Items'
        context['categories'] = CATEGORY
        context['tags'] = tags
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "partials/post_list_items.html"
        return "favorite.html"

# _____________Contact page________________________________________


class ContactPage(View):
    """
    The contact page allows the user to send a message via the form.
    """

    def get(self, request):

        items = list(Post.objects.all())
        sliders = random.sample(items, 5)
        contact_message_form = ContactMessageForm()

        return render(
            request,
            "contact.html",
            {
                "sliders": sliders,
                "contact_message_form": contact_message_form,
            },
        )

    def post(self, request):
        top_posts = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
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

# _____________Add item page_______________________________________


class AddItem(CheckManagerMixin, View):
    """
    The add item page allows registered managers to add there items.
    """

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
            add_item_form.save_m2m()
            messages.success(request, 'Form submission successful')
            return HttpResponseRedirect(reverse('my_page'))
        else:
            messages.error(request, 'Form submission failed')
            add_item_form = AddItemForm()

        return render(
            request,
            "add_item.html",
            {
                "add_item_form": add_item_form,
            },
        )

# _____________Edit item page______________________________________


class EditItem(CheckManagerMixin, View):
    """
    The edit item page allows the users to edit the items they added.
    """
    def get(self, request, slug):
        queryset = Post.objects.filter(status=1)
        item = get_object_or_404(queryset, slug=slug)
        add_item_form = AddItemForm(instance=item)

        return render(
            request,
            "edit_item.html",
            {
                "add_item_form": add_item_form,
                },
        )

    def post(self, request, slug):
        queryset = Post.objects.filter(status=1)
        item = get_object_or_404(queryset, slug=slug)
        add_item_form = AddItemForm(
            request.POST,
            request.FILES,
            instance=item
            )
        if add_item_form.is_valid():
            add_item_form.instance.author = request.user
            add_item_form.instance.slug = slugify(request.POST.get('title'))
            item = add_item_form.save(commit=False)
            item.save()
            add_item_form.save_m2m()
            messages.success(request, 'Form submission successful')
            return HttpResponseRedirect(reverse('my_page'))
        else:
            messages.error(request, 'Form submission failed')
            add_item_form = AddItemForm(
                request.POST,
                request.FILES,
                instance=item
                )

# _____________My page_____________________________________________


class MyPage(CheckManagerMixin, generic.ListView):
    """
    My page can be accessed by registered managers
    and it contains the item they added.
    """
    model = Post
    paginate_by = 4

    def get_queryset(self):
        queryset = Post.objects.filter(
            author=self.request.user
            ).order_by(
                "-created_on"
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        tags = Tag.objects.all()
        context['top_posts'] = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
        context['section_title'] = 'My Page'
        context['categories'] = CATEGORY
        context['tags'] = tags
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "partials/post_list_items.html"
        return "favorite.html"

# _____________Search bar__________________________________________


class SearchBar(generic.ListView):
    """
    The search bar allows all the users to serch the items by the title.
    """
    model = Post
    paginate_by = 4

    def get_queryset(self):
        query_input = self.request.GET.get('query_input')
        return Post.objects.filter(
            title__icontains=query_input
            ).order_by(
                '-created_on'
                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Post.objects.all())
        tags = Tag.objects.all()
        context['top_posts'] = Post.objects.annotate(
            num_likes=Count('likes')
            ).order_by(
                '-num_likes'
                )[0:5]
        context['section_title'] = 'Search Results'
        context['categories'] = CATEGORY
        context['tags'] = tags
        return context

    def get_template_names(self):
        if self.request.htmx:
            return "partials/post_list_items.html"
        return "favorite.html"

# _____________Delete item page____________________________________


class DeleteItem(CheckManagerMixin, View):
    """
    Registered managers can delete items from my_page.
    """

    def get(self, request, slug):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "confirmation.html",
            {
                "post": post,
            },
        )

    def post(self, request, slug):
        queryset = Post.objects.filter(status=1)
        item = get_object_or_404(queryset, slug=slug)
        item.delete()
        Tag.objects.filter(post=None).delete()

        return HttpResponseRedirect(reverse('my_page'))
