from django.db import models
from django_mysql.models import ListTextField
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 一つのユーザーはプロフィールを一つしか持てない
    name = models.CharField(max_length=20)
    image = models.ImageField(null=True, blank=True)
    self_introduction_text = models.TextField(max_length=200, null=True, blank=True)
    # -----フォルダのidを詰め込むリスト-----
    folders = ListTextField(
        base_field=models.IntegerField(), # これで数値型で管理できるようになる？
        size=100,  # Maximum of 100 ids in list(要素数は100個まで？)
        null=True,
        blank=True,
    )
    # -----
    def __str__(self):
        return str(self.user)

# @receiver(post_save, sender=User)
# # ↑sender(User)をsave()した時に↓（create_profile）が実行されるようになる（DjangoでUser登録した際は必ずその情報をsaveするように設定されているため、その際に実行させる）
# def create_profile(sender, instance, created, **kwargs):
#     if created: #新規作成時の分岐
#         # -----↓Profileモデルを、userフィールドにinstance情報を積めながらcreate(新規作成)する
#         Profile.objects.create(user=instance)
#         # -----↑user...Profileで作成したuserフィールド
#         # instance...saveしたデータ（新規作成した一人分のUser情報）が代入されてくる
#     instance.profile.save()

#フォローモデル
class Connection(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.id} : {self.following.id}"