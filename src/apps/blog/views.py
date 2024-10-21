from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, Http404
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from typing import Any
from urllib.parse import quote

from apps.blog.models import Bio, Post, Ip
from config import settings
from apps.blog.forms import BioForm, PostForm
from apps.blog.utils import PostViewsCounterMixin, CommonContextMixin


class HomeView(CommonContextMixin, generic.TemplateView):
    template_name = "home.html"
    
    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(is_active=True).annotate(views=Count("ips")).prefetch_related("ips").order_by("-views")[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Home"))

        object_list = self.get_queryset()
        context.update({"most_viewed_posts": object_list})
        return context

    
class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = quote(request.GET.get('q'))

        if query:
            google_search_url = f"https://www.google.com/search?q={settings.config('SITE_DOMAIN')}: {query}"
            return redirect(google_search_url)
        return redirect('/')


class PostListView(CommonContextMixin, generic.ListView):
    model = Post
    paginate_by = 5
    context_object_name = "posts"
    template_name = "post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Blog"))
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_active=True).annotate(views=Count("ips"))


class PostDetailView(PostViewsCounterMixin, CommonContextMixin, generic.DetailView):
    model = Post
    template_name = "post_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        return context

    def get_queryset(self):
        return super().get_queryset().annotate(views=Count("ips"))
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        address = self.get_client_address(request=request)
        ip, _ = Ip.objects.get_or_create(ip=address)
        
        if not self.object.ips.filter(id=ip.id).exists(): # Unique views
            self.object.ips.add(ip)
        
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
        post.save()
        return redirect("post-detail", id=post.id)


class PostUpdateView(CommonContextMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = "id"
    template_name = "post_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context(title="Update current post"))
        return context

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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


class BioShowView(CommonContextMixin, generic.TemplateView):
    template_name = "bio.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        bio = Bio.objects.first() # By default that model contains just one object
        
        if not bio:
            if request.user.is_authenticated:
                return redirect('bio-init')
            else:
                raise Http404("Author has not created a bio yet")
    
        context = self.get_context_data(title="About me", bio=bio)
        context.update(self.get_common_context())

        return render(request, template_name=self.template_name, context=context)
    

class BioInitView(CommonContextMixin, generic.TemplateView):
    template_name = "bio_init.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Create your bio",
            "form": kwargs.get("form", BioForm())
        })
        context.update(self.get_common_context())
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        form = BioForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('bio')
        
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)
    

class BioUpdateView(CommonContextMixin, generic.TemplateView):
    template_name = "bio_update.html"
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Upadate your bio"
        })
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
            return redirect('bio')
        
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