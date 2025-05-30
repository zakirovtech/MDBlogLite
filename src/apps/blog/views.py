import base64
import json
import logging
import os
from typing import Any
from urllib.parse import quote, unquote_plus

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import FileResponse, Http404, HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View, generic

from apps.blog.forms import AchievementForm, BioForm, PostForm, TagForm
from apps.blog.models import Achievement, Bio, Ip, Post, Tag
from apps.blog.utils import (
    BioConvertMixin,
    CommonContextMixin,
    PostViewsCounterMixin,
)

logger = logging.getLogger("blog")


def locked_out(request):
    """Temporary ban view for limited logins"""
    return render(request, "lock.html", status=403)


class AchievementListView(CommonContextMixin, generic.ListView):
    model = Achievement
    template_name = "achievement_list.html"
    context_object_name = "achievements"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Achievements"))
        return context


class AchievementDetailView(CommonContextMixin, generic.DeleteView):
    model = Achievement
    template_name = "achievement_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "ach"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_common_context(title=f"{context['ach'].header}")
        )
        return context


class AchievementUpdateView(CommonContextMixin, generic.UpdateView):
    model = Achievement
    form_class = AchievementForm
    pk_url_kwarg = "id"
    template_name = "achievement_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Edit achievement"))
        return context

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AchievementCreateView(CommonContextMixin, generic.CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = "achievement_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Add new achievement"))
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ach = form.save(commit=False)

        try:
            ach.save()
            return redirect("achievements-detail", id=ach.id)
        except Exception as e:
            logger.error(f"Failed to add achievement: {e}")
            form.add_error(
                None,
                "An error occurred while saving the achievement. Please try again.",
            )
            return self.form_invalid(form)


class AchievementDeleteView(CommonContextMixin, generic.DeleteView):
    model = Achievement
    template_name = "achievement_delete.html"
    success_url = reverse_lazy("achievements-list")
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            self.get_common_context(title="Delete current achievement")
        )
        return context


class HomeView(CommonContextMixin, generic.TemplateView):
    template_name = "home.html"

    def get_queryset(self) -> QuerySet[Any]:
        return (
            Post.objects.filter(is_active=True)
            .prefetch_related("tags")
            .annotate(views=Count("ips"))
            .order_by("-views")[:3]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = self.get_queryset()

        # Temporary logic of banner viewing
        if os.path.exists(
            os.path.join(settings.MEDIA_ROOT, "banner/banner.gif")
        ):
            with open(
                os.path.join(settings.MEDIA_ROOT, "banner/banner.gif"), "rb"
            ) as blob:
                banner_data = base64.b64encode(blob.read()).decode("utf-8")
                banner = f"data:image/gif;base64,{banner_data}"
        else:
            banner = None

        context.update(
            self.get_common_context(
                title="Home", most_viewed_posts=object_list, banner=banner
            )
        )
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = quote(request.GET.get("q"))

        if query:
            google_search_url = f"https://www.google.com/search?q={query} site:{settings.SITE_DOMAIN}"
            return redirect(google_search_url)
        return redirect("/")


class PostListView(CommonContextMixin, generic.ListView):
    model = Post
    paginate_by = 5
    context_object_name = "posts"
    template_name = "post_list.html"
    cache_key = "post_list_cache"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        context.update(self.get_common_context(title="Blog", tags=tags))
        return context

    def get_queryset(self) -> QuerySet[Any]:
        object_list = cache.get(self.cache_key)
        tag = self.kwargs.get("tag")

        if tag is not None:
            tag = unquote_plus(tag)

        if object_list is None:
            object_list = (
                super()
                .get_queryset()
                .filter(is_active=True)
                .annotate(views=Count("ips"))
                .prefetch_related("tags")
                .order_by("-date_created")
            )
            cache.set(
                self.cache_key,
                object_list,
                timeout=int(settings.CACHE_TIMEOUT),
            )

        if tag is not None:
            return object_list.filter(tags__name=tag)

        return object_list


class PostDetailView(
    PostViewsCounterMixin, CommonContextMixin, generic.DetailView
):
    model = Post
    template_name = "post_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        return context

    def set_cache_key(self):
        return f"post_{self.kwargs.get('id')}_detail_cache"

    def track_unique_view(self, request):
        address = self.get_client_address(request=request)
        ip, _ = Ip.objects.get_or_create(ip=address)

        if not self.object.ips.filter(id=ip.id).exists():
            self.object.ips.add(ip)

    def get_queryset(self):
        return super().get_queryset().annotate(views=Count("ips"))

    def get(self, request, *args, **kwargs):
        cache_key = self.set_cache_key()
        self.object = cache.get(cache_key)

        if self.object is None:
            queryset = self.get_queryset()
            self.object = self.get_object(queryset)

            self.track_unique_view(request)

            cache.set(
                cache_key, self.object, timeout=int(settings.CACHE_TIMEOUT)
            )
        else:
            self.track_unique_view(request)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostCreateView(CommonContextMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Create new post"))
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        post = form.save(commit=False)
        post.author = self.request.user
        try:
            post.save()
            form.save_m2m()
            return redirect("post-detail", id=post.id)
        except Exception as e:
            logger.error(f"Failed to create post: {e}")
            form.add_error(
                None,
                "An error occurred while saving the post. Please try again.",
            )
            return self.form_invalid(form)


class PostUpdateView(CommonContextMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = "id"
    template_name = "post_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Update current post"))
        return context

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(CommonContextMixin, generic.DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("post-list")
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Delete current post"))
        return context


class TagCreateView(CommonContextMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tag_create.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Create a new tag"))
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        try:
            super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "Tag with this name is already exists")
            return self.form_invalid(form)
        return redirect("post-list")

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        # Here you can add additional context if needed
        return self.render_to_response(self.get_context_data(form=form))


class TagDeleteView(CommonContextMixin, View):
    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Delete current tag"))
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        tag_name = data.get("name")

        if tag_name:
            tag = get_object_or_404(Tag, name=tag_name)
            tag.delete()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "failed"})


class BioShowView(CommonContextMixin, generic.TemplateView):
    template_name = "bio.html"
    cache_key = "bio_show_cache"

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        cached_bio = cache.get(self.cache_key)
        if cached_bio:
            bio = cached_bio
            logger.info("Bio object fetched from cache.")
        else:
            bio = Bio.objects.first()
            if not bio:  # First start, for example
                if request.user.is_authenticated:
                    return redirect("bio-init")
                else:
                    raise Http404("Author has not created a bio yet")

            cache.set(self.cache_key, bio, timeout=(60 * 60) * 24)
            logger.info("Bio cached for 24 hours")

        context = self.get_context_data(title="About me", bio=bio)
        context.update(self.get_common_context())

        return render(
            request, template_name=self.template_name, context=context
        )


class BioInitView(CommonContextMixin, BioConvertMixin, generic.TemplateView):
    template_name = "bio_init.html"

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": "Create your bio", "form": kwargs.get("form", BioForm())}
        )
        context.update(self.get_common_context())
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        form = BioForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            self.convert_md_to_pdf(request.POST["body"], logger)

            return redirect("bio")

        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)


class BioUpdateView(CommonContextMixin, BioConvertMixin, generic.TemplateView):
    template_name = "bio_update.html"

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Upadate your bio"})
        context.update(self.get_common_context())
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        obj = Bio.objects.first()
        form = BioForm(instance=obj)

        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        obj = Bio.objects.first()
        form = BioForm(request.POST, request.FILES, instance=obj)
        context = self.get_context_data(form=form)

        if form.is_valid():
            form.save()

            self.convert_md_to_pdf(request.POST["body"], logger)

            return redirect("bio")

        return render(request, self.template_name, context=context)


class BioDeleteView(CommonContextMixin, generic.DeleteView):
    model = Bio
    template_name = "bio_delete.html"
    success_url = reverse_lazy("bio-init")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Delete bio"))
        return context

    def get_object(self, queryset=None):
        bio = Bio.objects.first()
        if bio is None:
            raise Http404("Bio not found")
        return bio


class BioDownload(CommonContextMixin, generic.TemplateView):
    template_name = "bio-download.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Download PDF"))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def post(self, request):
        file_path = os.path.join(settings.MEDIA_ROOT, "pdf/cv.pdf")

        if os.path.exists(file_path):
            try:
                file = open(file_path, "rb")
                response = FileResponse(file, as_attachment=True)
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
            except Exception as e:
                raise Http404(f"Error while reading file: {str(e)}")
        else:
            raise Http404("File not found.")
