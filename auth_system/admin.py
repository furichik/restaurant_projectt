from django.contrib import admin
from .models import Post, Comment, Rating

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rating)

class PostAdmin(admin.ModelAdmin):

    list_display = ("title", "author", "created_at")

    search_fields = ("title",)

    list_filter = ("created_at",)


admin.site.register(Post, PostAdmin)