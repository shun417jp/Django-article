from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # ←追加
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    eyecatch = models.ImageField(upload_to='eyecatch/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    
    def likes_count(self):
        return self.likes.count()

    
    def liked_by_user(self, user):
        return self.likes.filter(user=user).exists()

    

    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')  # 同じユーザーが同じ記事に複数いいね不可

    def __str__(self):
        return f'{self.user.username} liked {self.article.title}'



# ユーザー登録時にプロフィール自動作成
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
