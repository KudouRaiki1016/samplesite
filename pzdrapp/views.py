from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PartyPost, Awakening, Folder, LikeForPartyPost, Comment, Reply
from . import forms
from django.conf import settings
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.contrib import messages
import sys
sys.path.append('../')
from accounts.models import Profile

from django.contrib.auth.decorators import login_required # ログイン必須

import time

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# ----------トップページ----------
def top_view(request):
    object_list = PartyPost.objects.all()
    context = {
        'object_list': object_list
    }
    return render(request, 'pzdrapp/top.html', context)


def detail_partypost_view(request, partypost_id):
    object = PartyPost.objects.get(pk = partypost_id)
    if request.method == 'POST':
        comment_text = request.POST['comment']
        if comment_text != '':
            Comment.objects.create(
                text = comment_text,
                user = request.user,
                target = object,
            )
            messages.add_message(request, messages.SUCCESS, "SUCCESS")
            return redirect('detail-partypost', partypost_id)
        else:
            messages.add_message(request, messages.ERROR, "ERROR")
        return redirect('detail-partypost', partypost_id)
    # -----↓コメント&それに対するリプライ情報の取得↓-----
    comment_list = Comment.objects.filter(target__id = partypost_id)
    reply_for_comment_dic = {}
    for com in comment_list:
        # 対象コメントに返信（Reply）があるかどうか
        if com.reply_set.filter(target=com).exists():
            reply_for_comment_dic[com.id] = {'len': len(com.reply_set.filter(target=com)), 'exists': True, 'list': Reply.objects.filter(target=com)}
        else:
            reply_for_comment_dic[com.id] = {'len': 0, 'exists': False, 'list': []}
    print(reply_for_comment_dic)
    # reply_for_comment_dic...{1: {'len': 1, 'exists': True, 'list': <QuerySet [<Reply: 1>]>}, 2: {'len': 0, 'exists': False, 'list': []}} リプライ数、リプライが存在するか、リプライのリストを格納している
    # -----↑コメントの取得↑-----
    # -----↓いいね情報の取得↓-----
    like_for_partypost_count = object.likeforpartypost_set.count()
    # ログイン中のユーザーがイイねしているかどうか
    if object.likeforpartypost_set.filter(user=request.user).exists():
        is_user_liked_for_partypost = True
    else:
        is_user_liked_for_partypost = False
    like_for_partypost_count = object.likeforpartypost_set.count()
    if object.likeforpartypost_set.filter(user=request.user).exists():
        is_user_liked_for_partypost = True
    else:
        is_user_liked_for_partypost = False
    # -----↑いいね情報の取得↑-----
    context = {
        'object': object,
        'like_for_partypost_count': like_for_partypost_count,
        'is_user_liked_for_partypost': is_user_liked_for_partypost,
        'comment_list': comment_list,
        'reply_for_comment_dic': reply_for_comment_dic,
    }
    return render(request, 'pzdrapp/detail_partypost_view.html', context)

def update_comment(request):
    object = Comment.object.get(pk=comment_id)
    print(object)
    context = {
        'object': object
    }
    return JsonResponse(context)
def delete_comment(request):
    comment_pk = request.POST.get('comment_pk') #コメントのpk(id)をhtmlから受け取る
    object = Comment.objects.get(pk=comment_pk).delete()
    return JsonResponse()

@login_required
def folderlist_view(request):
    object_list = Folder.objects.all()
    profile1 = Profile.objects.get(pk = request.user.profile.id)
    folders_dict = dict([(folder.id, folder) for folder in object_list]) # [id: そのidのfolderデータ]という形で辞書に収める
    # print(folders_dict)
    folder_list = [] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をfolder_listに積めていく
    for id in profile1.folders:
        try:
            folder_list.append(folders_dict[id])
        except KeyError: #KeyErrorがおこる⇨そのデータは存在しない（削除された）ため、そのidは削除しておく
            profile1.folders.remove(int(id))
            profile1.save()
            print(f'{id}は存在しないため削除しました')
    context = {
        'object_list': object_list,
        'folder_list': folder_list,
    }
    return render(request, 'pzdrapp/folderlist_view.html', context)

@login_required
def profile_postedlist_view(request):
    object_list = PartyPost.objects.filter(user = request.user).order_by('id')
    context = {
        'object_list': object_list
    }
    return render(request, 'pzdrapp/profile', context)

@login_required
def partypost_save_in_folder_view(request, folder_id):
    object_list = PartyPost.objects.all()
    folder = Folder.objects.get(pk=folder_id)
    save_partypost_id_list = folder.post_list # 対象フォルダの投稿の並び順をidで取得する
    # print(f'フォルダに保存された投稿データのid:{save_partypost_id_list}')
    # ----------↓設定されている順番に並び替える↓----------
    posts_dict = {}
    like_for_partypost = {}
    for partypost in object_list:
        posts_dict[partypost.id] = partypost
    sorted_partyposts = []
    for id in save_partypost_id_list:# 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_partypostsに積めていく
        try:
            sorted_partyposts.append(posts_dict[id])
        except KeyError: #KeyErrorがおこる⇨そのデータは存在しない（削除された）ため、そのidは削除しておく
            folder.post_list.remove(int(id))
            folder.save()
            print(f'{id}は存在しないため削除しました')
    print(f"並び替えられた書籍データ:{sorted_partyposts}")
    # ----------↑設定されている順番に並び替える↑----------

    liked_dic = {}
    for partypost in sorted_partyposts:
        like_for_partypost_count = partypost.likeforpartypost_set.count()
        if partypost.likeforpartypost_set.filter(user=request.user).exists():
            is_user_liked_for_partypost = True
        else:
            is_user_liked_for_partypost = False
        liked_dic[partypost.pk] = {'count': like_for_partypost_count, 'is_user_liked_for_partypost': is_user_liked_for_partypost}
    print(f'いいねのために格納した辞書データ...{liked_dic}')
    # liked_dic ... {7: {'count': 10, 'is_user_liked_for_partypost': False}, 9: ...}

    context ={
        "folder": folder,
        "sorted_partyposts": sorted_partyposts,
        "like_for_partypost": like_for_partypost,
        "liked_dic": liked_dic,
    }
    return render(request, 'pzdrapp/partypost_save_in_folder.html', context)

# ----------投稿処理----------
@login_required
def create_post(request):
    # ----------submit(送信ボタン)が押されてリクエストされた場合の分岐----------
    if request.method == 'POST':
        print(request.POST)
        # -----覚醒情報の整理-----
        awakening_obj = Awakening()
        awakeningform = forms.AwakeningForm(request.POST, instance=awakening_obj)
        if awakeningform.is_valid():
            awakening = Awakening.objects.create(
                skillboost = request.POST['skillboost'],
                sealed_resistance = request.POST['sealed_resistance'],
                poison_resistance = request.POST['poison_resistance'],
                obstacle_resistance = request.POST['obstacle_resistance'],
                darkness_resistance = request.POST['darkness_resistance'],
                operation_resistance = request.POST['operation_resistance'],
                cloud_resistance = request.POST['cloud_resistance'],
                operation_time = request.POST['operation_time'],
            )
            awakeningform.save()
            awakening.save()
        # --↓formに入力された情報を受け取り↓--
        title = request.POST['title']
        thumbnail = request.FILES['thumbnail']
        text = request.POST['text']
        partypost = PartyPost.objects.create(
            title = title,
            thumbnail = thumbnail,
            awakenings = awakening,
            text = text,
            user = request.user,
            )
        partypost.save()
        return redirect('top-page')
    # ----------

    partypostform = forms.PartyPostForm()
    awakeningform = forms.AwakeningForm()
    context = {
        'partyform': partypostform,
        'awakeningform': awakeningform,
    }
    return render(request, 'pzdrapp/create_partypost.html', context)

# ~~~~~~~~~~↓フォルダ関係↓~~~~~~~~~~

class CreateFolderView(LoginRequiredMixin, CreateView):
    model = Folder
    template_name = 'pzdrapp/create_folder.html'
    fields = ['title', 'thumbnail', 'release', 'user']
    success_url = reverse_lazy('list-folder')

class DeleteFolderView(LoginRequiredMixin, DeleteView):
    model = Folder
    template_name = 'pzdrapp/delete_folder.html'
    success_url = reverse_lazy('list-folder')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj

@login_required
def orderchange_folder(request):
    # ----------↓object_listに全書籍データを代入↓----------
    object_list = Folder.objects.all()
    # ----------↓profile1にログインしているユーザーのプロフィール情報を代入↓----------
    profile1 = Profile.objects.get(pk=request.user.profile.id) # profile1に一人分のプロフィールデータが入る
    # ----------↓profile1の本の並び順を取得する↓----------
    order_list = profile1.folders
    # print(f"ユーザーの並び変え順(order_list):{order_list}")
    # ----------↓設定されている順番に並び替える↓----------
    folders_dict = dict([(folder.id, folder) for folder in object_list]) # [id: そのidのFolderデータ]という形で辞書に収める
    sorted_folders_list = [folders_dict[int(id)] for id in order_list] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_foldersに積めていく
    print(f"並び替えられた書籍データ（sorted_folders_list）:{sorted_folders_list}")
    # ----------↑設定されている順番に並び替える↑----------
    # ----------↓並び替え確定のボタンが押されてリクエストが来た時の分岐↓----------
    if (request.method == 'POST'):
        new_order = request.POST['submit'].split(",") # new_orderに並び替えた後のデータをリスト型で保管する
        profile1.folders = new_order # プロフィールのsave_folder_idに上書き
        profile1.save() # 変更を保存
        print(f"並び替え後のlist：{profile1.folders}") # profileテーブルの内容が上書きされているかを確認する
        return redirect('list-folder')
    # ----------↑並び替え確定のボタンが押されてリクエストが来た時の分岐↑----------
    # ----------↓並び替えするためにリクエストが来た時の分岐↓----------
    else:
        context = {
            "sorted_folders_list": sorted_folders_list, # 並び替え順で書籍データが詰まっている（リスト型）
        }
        return render(
        request,
        'pzdrapp/folder_orderchange.html',
        context)
    # ----------↑並び替えするためにリクエストが来た時の分岐↑----------

@login_required
def append_partypost_in_folder(request, folder_id):
    object_list = PartyPost.objects.all() # 全投稿
    profile1 = Profile.objects.get(pk=request.user.id) # 一人分のプロフィールデータ
    folder = Folder.objects.get(pk=folder_id)
    # ----------追加ボタンが押された分岐----------
    if request.method == 'POST':
        append_objs = request.POST.getlist('office')
        for obj_id in append_objs:
            folder.post_list.append(str(obj_id))
        folder.save()
        return redirect('list-partypost_in_folder', folder_id = folder.id)
    # ----------
    else:
        # ----------↓obj_li_pkに全idを詰め込む↓----------
        obj_li_pk = []
        for obj in object_list:
            obj_li_pk.append(obj.id)
        # ----------
        # ----------↓obj_li_pkの中から、既に保存しているデータは削除する↓----------
        for saved_id in folder.post_list:
            obj_li_pk.remove(int(saved_id))
        # print(f'{profile1.user}の保存していないデータ番号:{obj_li_pk}')
        objs_dict = dict([(obj.id, obj) for obj in object_list]) # [id: そのidのデータ]という形で辞書に収める
        target_object_list = [objs_dict[int(id)] for id in obj_li_pk] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をnosave_objs_listに積めていく
        # ----------↑obj_li_pkの中から、既に保存しているデータは削除する↑----------
        return render(
            request,
            'pzdrapp/append_or_delete_partypost_in_folder.html',
            {'target_object_list': target_object_list,
            'create': True}
    )

@login_required
def delete_partypost_in_folder(request, folder_id):
    profile1 = Profile.objects.get(pk = request.user.id)
    object_list = PartyPost.objects.all() # 全投稿
    folder = Folder.objects.get(pk=folder_id)
    if profile1.id == folder.user.profile.id:
        # ----------削除ボタンが押された分岐----------
        if request.method == 'POST':
            delete_objs = request.POST.getlist('office')
            print(delete_objs)
            print(folder.post_list)
            for obj_id in delete_objs:
                folder.post_list.remove(int(obj_id))
            folder.save()
            return redirect('list-partypost_in_folder', folder_id = folder.id)
        # ----------
        else:
            # ----------↓obj_li_pkの中から、既に保存しているデータは削除する↓----------
            # print(f'{profile1.user}の保存していないデータ番号:{obj_li_pk}')
            objs_dict = dict([(obj.id, obj) for obj in object_list]) # [id: そのidのデータ]という形で辞書に収める
            target_object_list = [objs_dict[int(id)] for id in folder.post_list] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をnosave_objs_listに積めていく
            # ----------↑obj_li_pkの中から、既に保存しているデータは削除する↑----------
            return render(
                request,
                'pzdrapp/append_or_delete_partypost_in_folder.html',
                {'target_object_list': target_object_list,
                'delete': True}
        )
    else:
        raise PermissionDenied



@login_required
def like_for_partypost(request):
    partypost_pk = request.POST.get('partypost_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    print(context)
    partypost = get_object_or_404(PartyPost, pk=partypost_pk)
    like = LikeForPartyPost.objects.filter(target=partypost, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=partypost, user=request.user)
        context['method'] = 'create'
    

    context['like_for_partypost_count'] = partypost.likeforpartypost_set.count()

    return JsonResponse(context)
import json
def reply_acquisition_view(request):
    def cnvDataToJson(object):
        if(isinstance(object, id)):
            return str(object)
    comment_pk = request.POST.get('comment_pk') #コメントのpk(id)をhtmlから受け取る
    #-----↓リプライ情報を取得する↓-----
    reply_list_q = Reply.objects.filter(target__pk = comment_pk)
    print(reply_list_q[0].timestamp)
    reply_dic = {}
    for reply in reply_list_q:
        reply_dic[reply.id] = {'reply_pk': reply.pk, 'user_name': reply.user.profile.name, 'user_img_url': reply.user.profile.image.url, 'text': reply.text, 'timestamp': reply.timestamp}
    print(reply_dic)
    # reply_list = []
    # for reply in reply_list_q:
    #     reply_list.append(reply)
    print(reply_list_q)
    #-----↑リプライ情報を取得する↑-----
    context = {
        'reply_dic': reply_dic
    }
    return JsonResponse(context)


# ----------投稿一覧を表示する場合に送るべき変数『partypost_list』『liked_dic』----------
# partypost_list...表示する投稿を入れる
# liked_dic...投稿に対するいいね数と、リクエストユーザーがいいねしているか（True or False）を入れる → {7: {'count': 10, 'is_user_liked_for_partypost': False}, 9: ...}
def sample_view(request, profile_id):
    context = {}
    context['partypost_list'] = PartyPost.objects.filter(user__profile__id = profile_id) #対象ユーザー（プロフィール）の投稿のみ取得

    liked_dic = {}
    for partypost in context['partypost_list']:
        like_for_partypost_count = partypost.likeforpartypost_set.count()
        if partypost.likeforpartypost_set.filter(user=request.user).exists():
            is_user_liked_for_partypost = True
        else:
            is_user_liked_for_partypost = False
        liked_dic[partypost.pk] = {'count': like_for_partypost_count, 'is_user_liked_for_partypost': is_user_liked_for_partypost}
    context['liked_dic'] = liked_dic
    print(context)

    return render(request, 'pzdrapp/投稿リストbaseの読み込み方.html', context)