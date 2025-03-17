from django.urls import path

from apps.blog.views import (
    AchievementCreateView,
    AchievementDeleteView,
    AchievementDetailView,
    AchievementListView,
    AchievementUpdateView,
    BioDeleteView,
    BioDownload,
    BioInitView,
    BioShowView,
    BioUpdateView,
    HomeView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    SearchView,
    TagCreateView,
    TagDeleteView,
    locked_out,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("locked/", locked_out, name="axes-lock-view"),
    path("search/", SearchView.as_view(), name="search"),
    path("bio/", BioShowView.as_view(), name="bio"),
    path("bio/init/", BioInitView.as_view(), name="bio-init"),
    path("bio/update/", BioUpdateView.as_view(), name="bio-update"),
    path("bio/delete/", BioDeleteView.as_view(), name="bio-delete"),
    path("bio/download/", BioDownload.as_view(), name="bio-download"),
    path("tag/create/", TagCreateView.as_view(), name="tag-create"),
    path("tag/delete/", TagDeleteView.as_view(), name="tag-delete"),
    path(
        "post/tag/<str:tag>", PostListView.as_view(), name="post-list-by-tag"
    ),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:id>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "posts/update/<int:id>/", PostUpdateView.as_view(), name="post-update"
    ),
    path(
        "posts/delete/<int:id>/", PostDeleteView.as_view(), name="post-delete"
    ),
    path(
        "achievements/",
        AchievementListView.as_view(),
        name="achievements-list",
    ),
    path(
        "achievements/<int:id>/",
        AchievementDetailView.as_view(),
        name="achievements-detail",
    ),
    path(
        "achievements/create/",
        AchievementCreateView.as_view(),
        name="achievements-create",
    ),
    path(
        "achievements/update/<int:id>/",
        AchievementUpdateView.as_view(),
        name="achievements-update",
    ),
    path(
        "achievements/delete/<int:id>",
        AchievementDeleteView.as_view(),
        name="achievements-delete",
    ),
]
