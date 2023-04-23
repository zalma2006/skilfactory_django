from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment, News, Users
from markdownx.admin import MarkdownxModelAdmin


# class PostAdmin(admin.ModelAdmin):
#     list_display = ('author',
#                     'date',
#                     'title',
#                     'text',)
#     list_filter = ('author',
#                    'date',
#                    'title',
#                    'text',)
#     search_fields = ('author',
#                      'date',
#                      'title',
#                      'text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text',
                    'date',
                    'post',
                    'user',)
    list_filter = ('text',
                   'date',
                   'post',
                   'user')
    search_fields = ('text',
                     'date',
                     'post',
                     'user')


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(News)
admin.site.register(Users)
