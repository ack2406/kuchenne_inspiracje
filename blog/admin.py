from django.contrib import admin
from .models import Post, Comment, Profile

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_date')
    search_fields = ('content',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
