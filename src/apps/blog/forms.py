from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

from apps.blog.models import Bio, Post, Tag


class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ["body", "image"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "You can use markdown or html filling this space",
                    "id": "body-field",
                    "aria-describedby": "basic-addon2",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "id": "image-field",
                    "aria-describedby": "basic-addon3",
                }
            ),
        }


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input me-1",
            }
        ),
        required=False,
    )

    class Meta:
        model = Post
        fields = ["header", "body", "image", "is_active", "tags"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "What's happening?",
                    "id": "body-field",
                    "aria-describedby": "basic-addon2",
                }
            ),
            "header": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name the post",
                    "id": "header-field",
                    "aria-describedby": "basic-addon2",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "id": "image-field",
                    "aria-describedby": "basic-addon3",
                }
            ),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name the tag",
                    "id": "header-field",
                    "aria-describedby": "basic-addon2",
                }
            )
        }


class InvisibleRecaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
