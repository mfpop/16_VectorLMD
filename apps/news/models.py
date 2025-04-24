from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=20,
        default="blue",
        help_text="Color theme for this category (e.g., blue, red, green)",
    )

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"
        ordering = ["name"]
        db_table = "news_categories"  # Specify the custom table name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class News(models.Model):
    CATEGORY_CHOICES = [
        ("newsletter", "Newsletter"),
        ("alert", "Important Alert"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    # Keep the original field for backwards compatibility
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="newsletter"
    )
    # Add new relationship to NewsCategory
    news_category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_items",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    # Add fields for likes and dislikes
    likes = models.ManyToManyField(User, related_name="liked_news", blank=True)
    dislikes = models.ManyToManyField(User, related_name="disliked_news", blank=True)
    featured_image = models.ImageField(upload_to="news_images/", blank=True, null=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def display_category(self):
        """Return the category name to display"""
        if self.news_category:
            return self.news_category.name
        return self.get_category_display()

    @property
    def like_count(self):
        """Return the count of likes"""
        return self.likes.count()

    @property
    def dislike_count(self):
        """Return the count of dislikes"""
        return self.dislikes.count()

    def get_category_display(self):
        # Ensure this method exists to avoid attribute errors
        return self.category if hasattr(self, "category") else "Uncategorized"


class Comment(models.Model):
    """Model for news comments"""

    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.news.title}"
