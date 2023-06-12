from django.db import models
from django_mysql.models import ListTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone


# ----------↓耐性の選択項目をリストで定義↓----------
skillboost_num_list = [(num + 1, f'{num + 1}個') for num in range(100)]
sealed_resistance_num_list = [(0, '0%'),(20, '20%'),(40, '40%'),(50, '50%'),(60, '60%'),(70, '70%'),(80, '80%'),(90, '90%'),(100, '100%')]
poison_resistance_num_list = [(0, '0%'),(20, '20%'),(40, '40%'),(50, '50%'),(60, '60%'),(70, '70%'),(80, '80%'),(90, '90%'),(100, '100%')]
obstacle_resistance_num_list = [(0, '0%'),(20, '20%'),(40, '40%'),(50, '50%'),(60, '60%'),(70, '70%'),(80, '80%'),(90, '90%'),(100, '100%')]
darkness_resistance_num_list = [(0, '0%'),(20, '20%'),(40, '40%'),(50, '50%'),(60, '60%'),(70, '70%'),(80, '80%'),(90, '90%'),(100, '100%')]
operation_resistance_choice = ((True, '○'),(False, '×'))
cloud_resistance_choice = ((True, '○'),(False, '×'))
# ----------

# -----↓覚醒スキル↓-----
class Awakening(models.Model):
    skillboost = models.IntegerField(choices=skillboost_num_list)
    sealed_resistance = models.IntegerField(choices=sealed_resistance_num_list)
    poison_resistance = models.IntegerField(choices=poison_resistance_num_list)
    obstacle_resistance = models.IntegerField(choices=obstacle_resistance_num_list)
    darkness_resistance = models.IntegerField(choices=darkness_resistance_num_list)
    operation_resistance = models.BooleanField(choices=operation_resistance_choice)
    cloud_resistance = models.BooleanField(choices=cloud_resistance_choice)
    operation_time = models.IntegerField()
# -----

# -----↓投稿↓-----
class PartyPost(models.Model):
    title = models.CharField(max_length = 100)
    thumbnail = models.ImageField()
    awakenings = models.ForeignKey(Awakening, on_delete=models.CASCADE)
    # !バッジも追加する!
    text = models.TextField(max_length=1000)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
# -----


release_choice = ((True, '公開'),(False, '非公開'))
# ----------フォルダ機能----------
class Folder(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(null=True, blank=True)
    release = models.BooleanField(choices=release_choice)
    # -----編成情報を詰め込んでいくリスト-----
    post_list = ListTextField(
        base_field=models.IntegerField(), # これで数値型で管理できるようになる？
        size=100,  # Maximum of 100 ids in list(要素数は100個まで？)
        )
    # -----
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

@receiver(post_save, sender=Folder)
# ↑sender(User)をsave()した時に↓（append_userfolders）が実行されるようになる（DjangoでUser登録した際は必ずその情報をsaveするように設定されているため、その際に実行させる）
def append_folders(sender, instance, created, **kwargs):
    if created:
        # -----↓Profileモデルを、userフィールドにinstance情報を積めながらcreate(新規作成)する
        instance.user.profile.folders.append(instance.id)
        # instance...saveしたデータ（新規作成したFolder情報）が代入されてくる
    instance.user.profile.save()

# ----------投稿に対するいいね----------
class LikeForPartyPost(models.Model):
    target = models.ForeignKey(PartyPost, on_delete=models.CASCADE) # いいね対象書籍
    user = models.ForeignKey(User, on_delete=models.CASCADE) # いいねしたUser
    timestamp = models.DateTimeField(default=timezone.now) # いいねしたタイミング
# ----------

# ----------投稿に対するコメント----------
class Comment(models.Model):
    text = models.TextField('本文')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(PartyPost, on_delete=models.CASCADE, verbose_name='対象投稿') #verbose_name...モデルフィールドの名前を指定する（日本語が使えるのがメリット）
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id)
# ----------
# ----------コメントに対するコメント（リプライ）----------
class Reply(models.Model):
    text = models.TextField('本文')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id)
# ----------