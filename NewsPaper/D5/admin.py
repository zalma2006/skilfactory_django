from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment, MyModel
from modeltranslation.admin import TranslationAdmin


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


class CategoryTranslationAdmin(TranslationAdmin):
    model = Category


class MyModelTranslationAdmin(TranslationAdmin):
    model = MyModel


admin.site.register(Category, CategoryTranslationAdmin)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MyModel, MyModelTranslationAdmin)
