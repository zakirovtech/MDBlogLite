from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest, Http404
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic, View
import markdown
from typing import Any

from apps.blog.models import Bio, Post, Ip
from config import settings
from apps.blog.forms import BioForm, PostForm
from apps.blog.utils import PostViewsCounterMixin, CommonContextMixin


class HomeView(CommonContextMixin, generic.TemplateView):
    template_name = "home.html"
    
    def get_queryset(self):
        return Post.objects.annotate(views=Count("ips")).filter(is_active=True).order_by("-views")[:3]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())

        object_list = self.get_queryset()
        markdown_posts = [mark_safe(markdown.markdown(post.body)) for post in object_list]
        most_viewed_posts = list(zip(markdown_posts, object_list))

        context.update({"most_viewed_posts": most_viewed_posts})
        return context

    
class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        print(request.GET   )
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
        context.update(self.get_common_context())
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        markdown_posts = [mark_safe(markdown.markdown(post.body)) for post in self.object_list]
        self.object_list = list(zip(markdown_posts, self.object_list))  
        
        context = self.get_context_data()
        return self.render_to_response(context)


class PostDetailView(PostViewsCounterMixin, CommonContextMixin, generic.DetailView):
    model = Post
    template_name = "post_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        address = self.get_client_address(request=request)
        ip, _ = Ip.objects.get_or_create(ip=address)
        
        if not self.object.ips.filter(id=ip.id).exists(): # Unique views
            self.object.ips.add(ip)
        
        post_markdown = mark_safe(markdown.markdown(self.object.body))
        context = self.get_context_data(object=self.object, post_markdown=post_markdown)
        return self.render_to_response(context)


class PostCreateView(CommonContextMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        post = Post.objects.create(author=request.user, header=request.POST.get("header"), body=request.POST.get("body"))
        return redirect("post-detail", id=post.id )


class PostUpdateView(CommonContextMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = "id"
    template_name = "post_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
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


class BioShowView(CommonContextMixin, View):
    template_name = "bio.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        bio = Bio.objects.first() # By default that model contains jone object
        
        if not bio and request.user.is_authenticated:
            return redirect('bio-init')
        
        if not bio and not request.user.is_authenticated:
            raise Http404("Author has not created a bio yet")
    
        context = {
            "title": "About me",
            "bio": bio,
            "bio_markdown": mark_safe(markdown.markdown(bio.body))    
        }
        context.update(self.get_common_context())

        return render(request, template_name=self.template_name, context=context)
    

class BioInitView(CommonContextMixin, View):
    template_name = "bio_init.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        form = BioForm()
        
        context = {"title": "Create your bio", 'form': form}
        context.update(self.get_common_context())
        
        return render(request, self.template_name, context=context)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        form = BioForm(request.POST, request.FILES)
        
        context = {"title": "Create your bio", 'form': form}
        context.update(self.get_common_context())

        if form.is_valid():
            form.save()
            return redirect('bio')
        
        return render(request, self.template_name, context=context)
    
class BioUpdateView(CommonContextMixin, View):
    template_name = "bio_update.html"
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        obj = Bio.objects.first()
        form = BioForm(instance=obj)
        
        context = {"title": "Update your bio", 'form': form}
        context.update(self.get_common_context())
        return render(request, self.template_name, context=context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any):
        obj = Bio.objects.first()
        form = BioForm(request.POST, request.FILES, instance=obj)
        
        context = {"title": "Update your bio", 'form': form}
        context.update(self.get_common_context())
        
        if form.is_valid():
            form.save()
            return redirect('bio')
        
        return render(request, self.template_name, context=context)
