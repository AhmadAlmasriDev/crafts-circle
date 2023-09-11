from .models import Comment, Post, ContactMessage
from crispy_forms.helper import FormHelper
from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group
from django_summernote.widgets import SummernoteWidget
from crispy_forms.layout import Layout, Div, Field



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_body'].label = ''


class AddItemForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget, label="Content", required=True)

    class Meta:
        model = Post
        fields = ('title', 'slider_image', 'listing_image', 'category', 'content', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('title', css_class='form-left-container'),
            Div('slider_image', 'listing_image', css_class='form-right-container'),
            Div('content', css_class='form-content-container'),
            Div('status', css_class='form-status-container'),
        )   

class CustomSignupForm(SignupForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    # username = forms.CharField(max_length=30, label='username')
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        group = self.cleaned_data['group']
        user.groups.add(group)
        # user.name = self.cleaned_data['username']
        # user.save()
        return user
   
# class CustomSigninForm(LoginForm):
    
#     def save(self, request):
#         user = super(CustomSigninForm, self).save(request)
      
#         user.save()
#         return user

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('user_name', 'user_email', 'message_body')
    def __init__(self, *args, **kwargs):
        super(ContactMessageForm, self).__init__(*args, **kwargs)
        self.fields['message_body'].label = 'Message'
        self.fields['user_name'].label = 'Name'
        self.fields['user_email'].label = 'Email'
