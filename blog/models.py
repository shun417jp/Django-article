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
    

    def __str__(self):
        return self.title


# ユーザー登録時にプロフィール自動作成
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
