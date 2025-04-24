from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import News, Comment, NewsCategory
from django.views.decorators.http import require_POST
from django.db import models
from django.contrib.auth.models import User
import datetime


@login_required
def index(request):
    """Display all news items (newsletters and alerts)"""
    news_list = News.objects.filter(is_published=True)

    # Apply category filter
    category = request.GET.get("category")
    if category:
        news_list = news_list.filter(category=category)

    # Apply news_category filter
    news_category = request.GET.get("news_category")
    if news_category:
        news_list = news_list.filter(news_category__id=news_category)

    # Apply search filter
    search = request.GET.get("search")
    if search:
        news_list = news_list.filter(
            models.Q(title__icontains=search) | models.Q(content__icontains=search)
        )

    # Apply author filter
    author = request.GET.get("author")
    if author:
        news_list = news_list.filter(author__id=author)

    # Apply date filter
    date_str = request.GET.get("date")
    if date_str:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            news_list = news_list.filter(created_at__date=date_obj)
        except ValueError:
            pass

    # Annotate like/dislike status
    news_list = news_list.annotate(
        is_liked_by_current_user=models.Exists(
            News.likes.through.objects.filter(
                news_id=models.OuterRef("pk"), user_id=request.user.id
            )
        ),
        is_disliked_by_current_user=models.Exists(
            News.dislikes.through.objects.filter(
                news_id=models.OuterRef("pk"), user_id=request.user.id
            )
        ),
    )

    # Fetch categories and authors for filters
    categories = NewsCategory.objects.all()
    authors = User.objects.filter(news__is_published=True).distinct()

    context = {
        "news_list": news_list,
        "title": "News",
        "categories": categories,
        "authors": authors,
    }
    return render(request, "news/index.html", context)


@login_required
def detail(request, news_id):
    """Display a specific news item"""
    news = get_object_or_404(News, pk=news_id, is_published=True)
    context = {
        "news": news,
        "title": news.title,
    }
    return render(request, "news/detail.html", context)


@login_required
@require_POST
def like_news(request, news_id):
    """Handle like action for a news item"""
    news = get_object_or_404(News, pk=news_id)
    user = request.user
    # Toggle like status
    has_liked = news.likes.filter(id=user.id).exists()
    if has_liked:
        news.likes.remove(user)
        has_liked = False
    else:
        # Remove from dislikes if it exists there
        if news.dislikes.filter(id=user.id).exists():
            news.dislikes.remove(user)
        news.likes.add(user)
        has_liked = True
    # Return JSON response for Alpine.js
    return JsonResponse(
        {
            "like_count": news.likes.count(),
            "dislike_count": news.dislikes.count(),
            "has_liked": has_liked,
        }
    )


@login_required
@require_POST
def dislike_news(request, news_id):
    """Handle dislike action for a news item"""
    news = get_object_or_404(News, pk=news_id)
    user = request.user
    # Toggle dislike status
    has_disliked = news.dislikes.filter(id=user.id).exists()
    if has_disliked:
        news.dislikes.remove(user)
        has_disliked = False
    else:
        # Remove from likes if it exists there
        if news.likes.filter(id=user.id).exists():
            news.likes.remove(user)
        news.dislikes.add(user)
        has_disliked = True
    # Return JSON response for Alpine.js
    return JsonResponse(
        {
            "like_count": news.likes.count(),
            "dislike_count": news.dislikes.count(),
            "has_disliked": has_disliked,
        }
    )


@login_required
@require_POST
def add_comment(request, news_id):
    """Add a comment to a news item"""
    news = get_object_or_404(News, pk=news_id)
    content = request.POST.get("content", "").strip()
    if content:
        comment = Comment.objects.create(
            news=news, author=request.user, content=content
        )
        # For HTMX response, render just the new comment
        if request.headers.get("HX-Request"):
            return render(request, "components/comment_item.html", {"comment": comment})
    # For regular requests or empty content, redirect back to the page
    return redirect("news:detail", news_id=news_id)
