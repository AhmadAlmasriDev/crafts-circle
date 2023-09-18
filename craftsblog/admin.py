from django.contrib import admin
from .models import Post, Comment, Message, ContactMessage
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'slug', 'get_tags', 'status', 'created_on')
    search_fields = ['title', 'content', 'category']
    list_filter = ('status', 'created_on', 'category')
    prepopulated_fields = {'slug': ('title',)}
    summernotefields = ('content')

    def get_tags(self, obj):
        return ", ".join( o for o in obj.tags.names())


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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'message_body', 'created_on', 'read')
    list_filter = ('read', 'created_on')
    search_fields = ('user_name', 'message_body')
    actions = ['message_read']

    def message_read(self, request, queryset):
        queryset.update(read=True)
