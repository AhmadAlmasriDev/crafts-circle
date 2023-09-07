from .models import Comment, Post
from crispy_forms.helper import FormHelper
from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.models import Group

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body',)
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_body'].label = ''

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','author','slider_image','listing_image','category','content','status')
    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        # self.fields['comment_body'].label = ''


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
   
class CustomSigninForm(LoginForm):
    
    def save(self, request):
        user = super(CustomSigninForm, self).save(request)
      
        user.save()
        return user