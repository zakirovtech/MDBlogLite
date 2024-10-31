from apps.blog.forms import InvisibleRecaptchaForm


def recaptcha_form(request):
    return {
        'recaptcha_form': InvisibleRecaptchaForm()
    }
