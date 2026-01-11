"""
This module contains form classes used for handling user signups, post creation, 
and custom user registration.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from .models import Post, Profile, Comment

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a comment...'}),
        }

class PostForm(forms.ModelForm):
    """
    Form for creating and updating posts.
    It handles the title, content, and image fields for a post.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your content', 'rows': 4}),  
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        error_messages = {
            'title': {'required': 'Post title is required'},
            'content': {'required': 'Please provide some content'},
            'image': {'required': 'Please upload an image'},
        }
class SignupForm(UserCreationForm):
    """
    Form for user signup, including email field.
    """
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form with email validation and password matching.
    """
    email = forms.EmailField(required=True)  # Ensure email is required
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match. Please enter the same password.")

        return cleaned_data
