from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='',widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('body',)
