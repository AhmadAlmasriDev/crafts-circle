from .models import Comment, Post, ContactMessage
from crispy_forms.helper import FormHelper
from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group
from django_summernote.widgets import SummernoteWidget
from crispy_forms.layout import Layout, Div, Field
from taggit.forms import TagWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_body'].label = ''


class AddItemForm(forms.ModelForm):
    content = forms.CharField(
        widget=SummernoteWidget,
        label="Content",
        required=False
        )

    class Meta:
        model = Post
        fields = (
            'title',
            'slider_image',
            'listing_image',
            'category',
            'content',
            'tags',
            'status'
            )
        labels = {
            'slider_image':
            'Slider image',
            'listing_image':
            'Listing image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class CustomSignupForm(SignupForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        group = self.cleaned_data['group']
        user.groups.add(group)
        return user


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('user_name', 'user_email', 'message_body')

    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        self.fields['message_body'].label = 'Message'
        self.fields['user_name'].label = 'Name'
        self.fields['user_email'].label = 'Email'
