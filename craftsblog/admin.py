from django.contrib import admin
from .models import Post, Comment, Message 
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content', 'category']
    list_filter = ('status', 'created_on', 'category')
    prepopulated_fields = {'slug': ('title',)}
    
    summernotefields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'comment_body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('user_name', 'comment_body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)  

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_body', 'post', 'created_on', 'read')
    list_filter = ('read', 'created_on')
    search_fields = ('user', 'message_body')
    actions = ['message_read']
    
    def message_read(self, request, queryset):
        queryset.update(read=True)


