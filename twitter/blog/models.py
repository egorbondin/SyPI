from django.conf import settings
from django.db import models

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=70)
    content = models.TextField('Текст', max_length=2000)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    POST_CHOICES = (
        ('personal', 'personal'),
        ('teacher', 'teacher'),
        ('group', 'group'),
        ('admin', 'admin'),
    )

    post_type = models.CharField(max_length=10, choices=POST_CHOICES)
    
    @property
    def get_likes_count(self):
        return self.likes.count()
    
    @property
    def get_comments_count(self):
        return self.comments.count()

    @property
    def get_short_content(self):
        return self.content[:50] + '...'
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
class Comment(models.Model):
    content = models.TextField('Текст', max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content[:10]}...'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, 
                             related_name='likes', 
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'Лайк от {self.user} посту {self.post}'
    
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

class Subscription(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                 related_name='followed_blogs',
                                 on_delete=models.CASCADE)
    followed_blog = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                      related_name='followers',
                                      on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower} подписан на {self.followed_blog}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

class UnconfirmedPost(models.Model):
    title = models.CharField('Заголовок', max_length=70)
    content = models.TextField('Текст', max_length=2000)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Предложенный пост'
        verbose_name_plural = 'Предложенные посты'