from django import forms
from comment.models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 150, 'rows': 2}), label='Comment', required=False)

    class Meta:
        model = Comment
        fields = ('body',)
