from django.urls import path
from apps.blog.views import ( 
    HomeView, SearchView, BioShowView, BioInitView, BioUpdateView, BioDeleteView,
    PostListView, PostDetailView, PostUpdateView, PostCreateView, PostDeleteView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search/", SearchView.as_view(), name="search"),
    path("bio/", BioShowView.as_view(), name="bio"),
    path("bio/init", BioInitView.as_view(), name="bio-init"),
    path("bio/update", BioUpdateView.as_view(), name="bio-update"),
    path("bio/delete", BioDeleteView.as_view(), name="bio-delete"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:id>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/update/<int:id>/", PostUpdateView.as_view(), name="post-update"),
    path("posts/delete/<int:id>/", PostDeleteView.as_view(), name="post-delete")
]
