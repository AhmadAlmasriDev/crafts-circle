from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0,"Draft"),(1,"Published"))
CATEGORY = ((0,"Books"),(1,"Lamps"),(2,"Interior"),(3,"Other"))

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_author"
    )
    slider_image = CloudinaryField('slider_image', default='placeholder')
    listing_image = CloudinaryField('listing_image', default='placeholder')
    
    category = models.IntegerField(choices = CATEGORY)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
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

    def number_of_comments(self):
        return self.comments.filter(approved=True).count()

    def test_group(self):
        return self.author._meta.fields

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user_name = models.CharField(max_length=80)
    comment_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment: {self.comment_body} By: {self.user_name}"
    
    
  

class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_messages")
    message_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)   
    read = models.BooleanField(default=False)   
    
    class meta:
        ordering = ["created_on"]
    
    def __str__(self):
        return f"Message: {self.message_body}\nFrom: {self.user}"