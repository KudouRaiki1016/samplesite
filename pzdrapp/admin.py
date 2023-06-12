from django.contrib import admin
from .models import PartyPost, Awakening, Folder, LikeForPartyPost, Comment, Reply

admin.site.register(PartyPost)
admin.site.register(Awakening)
admin.site.register(Folder)
admin.site.register(LikeForPartyPost)
admin.site.register(Comment)
admin.site.register(Reply)
