from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField


class Author(models.Model):
    person_id = AutoOneToOneField(User, on_delete=models.CASCADE)
    rank_user = models.IntegerField(default=0)

    def update_rating(self):
        post_rank_sum = sum([list(d.values())[0] for d in Post.objects.filter(
            author_id=self.id).filter(changes='art').values('rank_post')])
        sum_comment = sum([list(d.values())[0] for d in Comment.objects.filter(
            user_id_id=self.id).values('rank_comment')])
        Post.objects.filter(comment__user_id_id=self.id).filter(
            changes__contains='art').values('comment__rank_comment')

        sum_comment_art = sum([list(d.values())[0] for d in Post.objects.filter(
            comment__user_id_id=self.id).filter(changes__contains='art').values('comment__rank_comment')])
        self.rank_user = post_rank_sum + sum_comment + sum_comment_art
        self.save()


class Category(models.Model):
    name_category = models.CharField(unique=True, max_length=255)


class Post(models.Model):
    news = 'nws'
    article = 'art'
    change = [(news, 'Новость'), (article, 'Статья')]
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    changes = models.CharField(choices=change, max_length=3)
    dt_create = models.DateTimeField(auto_now_add=True)
    category_id = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rank_post = models.IntegerField(default=0)

    def like(self):
        self.rank_post += 1
        self.save()

    def dislike(self):
        self.rank_post -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'{self.changes}: {self.title}, \n ({self.text})'


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    dt_text_comment = models.DateTimeField(auto_now_add=True)
    rank_comment = models.IntegerField(default=0)

    def like(self):
        self.rank_comment += 1
        self.save()

    def dislike(self):
        self.rank_comment -= 1
        self.save()