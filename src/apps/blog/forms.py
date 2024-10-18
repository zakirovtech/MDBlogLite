from django import forms
from apps.blog.models import Bio, Post


class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ['body', 'image']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Use can use markdown or html filling this space",
                'id': 'body-field',
                "aria-describedby": "basic-addon2",
                "rows": 20,
                "cols": 30,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'image-field',    
                "aria-describedby": "basic-addon3"
            })
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["header", "body", "is_active"]
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "What's happening?",
                'id': 'body-field',
                "aria-describedby": "basic-addon2",
                "rows": 20,
                "cols": 30,
            }),
            "header": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Name the post",
                "id": "header-field",
                "aria-describedby": "basic-addon2"
            })
        }
