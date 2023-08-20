from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0,"Draft"),(1,"Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="item_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    image_1 = CloudinaryField('image', default='placeholder')
    image_2 = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices = STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='item_likes', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment: {self.body}\nBy: {self.user.name}"


class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_messages")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)   
    read = models.BooleanField(default=False)   
    
    class meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Message: {self.body}\nFrom: {self.user.name}"