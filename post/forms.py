from .models import Post, Comment
from django import forms 
#import tinymce

# class TinyMCEWidget(tinymce):
#     def use_required_attribute(self, *args):
#         return False 

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4',
    }))
    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4',
    }))
    class Meta:
        model = Comment
        fields = ('content',)