from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]


class PostAdmin(admin.ModelAdmin):
    list_display = ('author_id',
                    'changes',
                    'dt_create',
                    'title',
                    'text',
                    'rank_post')
    list_filter = ('author_id',
                   'changes',
                   'dt_create',
                   'title',
                   'text',
                   'rank_post')
    search_fields = ('author_id',
                     'changes',
                     'dt_create',
                     'title',
                     'text',
                     'rank_post')


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
