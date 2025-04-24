from django.contrib import admin
from .models import News, NewsCategory, Comment


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "news_category",
        "created_at",
        "is_published",
    ]
    list_filter = ["category", "news_category", "is_published", "created_at"]
    search_fields = ["title", "content"]
    date_hierarchy = "created_at"
    filter_horizontal = ["likes", "dislikes"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["news", "author", "created_at"]
    list_filter = ["news", "author", "created_at"]
    search_fields = ["content"]
    date_hierarchy = "created_at"
