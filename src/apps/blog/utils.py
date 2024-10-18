from config import settings


class PostViewsCounterMixin:
    def get_client_address(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class CommonContextMixin:
    def get_common_context(self, *args, **kwargs):
        context = {"blogname": settings.config("BLOG_NAME")} 
        if args:
            context.update({"extra_args": args})
        if kwargs:
            context.update(**kwargs)
        return context
