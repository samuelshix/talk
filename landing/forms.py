from django import forms
from .models import *

class PostImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description','image_url']

class CreatePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['name', 'description','page_img']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['bio', 'picture']

class RegisterProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_name', 'product_description', 'product_price', 'product_image'] 