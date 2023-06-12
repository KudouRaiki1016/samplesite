from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm, ProfileSettingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Profile, Connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .helpers import get_current_profile #リクエストを引数にすることでそのProfile情報を取得できる関数
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


import sys
sys.path.append('../')
from pzdrapp.models import PartyPost



# ----------サインアップ（新規ユーザー登録）----------
class SignupView(CreateView):
    model = User
    form_class = SignupForm
    # -----プロフィールのためのフォームデータも追加する-----
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profileform = ProfileSettingForm()
        print(profileform)
        context['profile_form_class'] = ProfileSettingForm
        return context
    # -----
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('top-page')
# ----------



def signup_view(request):
    # ----------↓POSTメソッドが返された場合（＝サインアップのアカウント作成ボタンが押された場合）↓----------
    if request.method == 'POST':
        userform = UserCreationForm(request.POST)
        # -----↓正常な値が代入されていた時の分岐↓-----
        if userform.is_valid():
            userform.save() #データベース登録
            # user.refresh_from_db()
            # --↓userformに入力された情報を受け取り↓--
            profilename = request.POST.get('profilename')
            profileimage = request.POST.get('profileimage')
            profiletext = request.POST.get('profiletext')
            username = userform.cleaned_data.get('username')
            raw_password = userform.cleaned_data.get('password1')
            # --↓それをDjangoのデータベースに反映↓--
            user = authenticate(username=username, password=raw_password)
            Profile.objects.create(name=profilename, image=profileimage, self_introduction_text=profiletext,  user=user)
            # --↓ログインしてトップページへ遷移↓
            login(request, user)
            return redirect('top-page')
        # -----
    # ----------
    # ----------↓その他の場合（つまりGETメソッドが返された場合）↓----------
    else:
        userform = UserCreationForm()
        profileform = ProfileSettingForm()
        print(profileform)
    # ----------↑その他の場合（つまりGETメソッドが返された場合）↑----------
    return render(request, 'accounts/signup.html', {'form': userform})
    # ----------

def profile_detail_view(request, profile_id):
    context = {}
    context['object'] = request.user.profile
    request_profile = get_current_profile(request) #リクエストユーザーのProfile情報を取得する（※1）
    # ---↓「※1」と「引数のprofile_id」を比べて、同じならconnectedがTrueになる---↓
    if profile_id is not request_profile.id:
        result = Connection.objects.filter(follower__id=request_profile.id).filter(following__id=profile_id)
        context['connected'] = True if result else False
    # ---
    context['following'] = Connection.objects.filter(follower__id=profile_id).count() #フォローしている人数をカウント
    context['follower'] = Connection.objects.filter(following__id=profile_id).count() #フォローされている人数をカウント
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

    return render(request, 'accounts/detail_profile.html', context)



class old_ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/detail_profile.html'

    # #slug_field = urls.pyに渡すモデルのフィールド名
    # slug_field = 'pk'
    # # urls.pyでのキーワードの名前
    # slug_url_kwarg = 'pk'


    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        request_profile = get_current_profile(self.request) #リクエストユーザーのProfile情報を取得する（※1）
        profile_id = context['object'].id #urlで渡されたProfileのidを取得する（※2）
        # ---↓「※1」と「※2」を比べて、同じなら---↓
        if profile_id is not request_profile.id:
            result = Connection.objects.filter(follower__id=request_profile.id).filter(following__id=profile_id)
            context['connected'] = True if result else False
        # ---
        context['following'] = Connection.objects.filter(follower__id=profile_id).count() #フォローしている人数をカウント
        context['follower'] = Connection.objects.filter(following__id=profile_id).count() #フォローされている人数をカウント
        context['partypost_list'] = PartyPost.objects.filter(user__profile__id = profile_id) #対象ユーザー（プロフィール）の投稿のみ取得

        liked_dic = {}
        for partypost in context['partypost_list']:
            like_for_partypost_count = partypost.likeforpartypost_set.count()
            if partypost.likeforpartypost_set.filter(user=self.request.user).exists():
                is_user_liked_for_partypost = True
            else:
                is_user_liked_for_partypost = False
            liked_dic[partypost.pk] = {'count': like_for_partypost_count, 'is_user_liked_for_partypost': is_user_liked_for_partypost}
        context['liked_dic'] = liked_dic

        return context



def profile_update(request, pk):
    profile1 = Profile.objects.get(pk=pk)
    context = {
        'profile': profile1,
    }
    if request.method == 'POST':
        try:
            profilename = request.POST.get('profilename')
            profiletext = request.POST.get('self_introduction_text')
            profile1.name = profilename
            profile1.self_introduction_text = profiletext
            profile1.save()
            return redirect('accounts:detail-profile')
        except:
            context['error'] = 'エラーが発生しました。正しい情報を入力してください'
            return render(request, 'accounts/edit_profile.html', context)
    else:
        return render(request, 'accounts/edit_profile.html', context)



"""フォロー"""
@login_required
def follow_view(request):
    following_pk = request.POST.get('object_pk') #フォロー対象ユーザーのpk(id)がPOSTで渡される
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    try:
        follower = Profile.objects.get(pk=request.user.profile.id) #フォローしているユーザー（プロフィールモデル）
        following = Profile.objects.get(pk=following_pk) # ※フォロー対象ユーザー（プロフィールモデル）
    # -----フォロー対象が存在しない場合のエラーを拾う（警告文をmessagesに登録）-----
    except Profile.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(following_pk)) # messagesはrequestに格納されるため、contextで伝えなくてもtemplateで扱える
    _, created = Connection.objects.get_or_create(follower=follower, following=following) #既に相手をフォローしていた場合、createdにはFalseが入る。
    print(created)
    # ---もしcreatedがTrueの場合、フォロー処理となるため、ここで処理は終了---
    if (created):
        messages.success(request, f'{following.name}をフォローしました')
        context['method'] = 'create'
    # ---もしcreatedがFalseの場合、フォロー解除の処理を行う---
    else:
        unfollow = Connection.objects.get(follower=follower, following=following)
        #フォロワー(自分)×フォロー(相手)という組み合わせを削除する。
        unfollow.delete()
        messages.success(request, 'あなたは{}のフォローを外しました'.format(following.name))
        context['method'] = 'delete'
        # ---
    print(context)
    return JsonResponse(context)



"""フォロー解除"""
@login_required
def unfollow_view(request, *args, **kwargs):
    try:
        follower = Profile.objects.get(pk=request.user.profile.id)
        following = Profile.objects.get(pk=kwargs['pk'])
        if follower == following:
            messages.warning(request, '自分自身のフォローを外せません')
        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            #フォロワー(自分)×フォロー(相手)という組み合わせを削除する。
            unfollow.delete()
            messages.success(request, 'あなたは{}のフォローを外しました'.format(following.name))
    except Profile.DoesNotExist:
        messages.warning(request, '存在しないユーザーです')
        return HttpResponseRedirect(reverse_lazy('top-page'))
    except Connection.DoesNotExist:
        messages.warning(request, 'あなたは対象ユーザーをフォローしませんでした')

    return redirect('accounts:detail-profile', pk=following.id)



# ----------↓フォローアカウント一覧画面↓----------
@login_required
def followinglist_view(request, profile_id):
    try:
        following = Profile.objects.get(pk=profile_id) #対象ユーザーのProfile
        connections = Connection.objects.filter(follower__id=profile_id)
        following_list = []
        for con in connections:
            following_list.append(con.following)
        context = {
            'following_page': True,
            'follow_list': following_list,
            'follow': following,
        }
        return render(request, 'accounts/follow_list_view.html', context)
    except Profile.DoesNotExist: # 対象のプロフィールが見つからなかった場合のエラーを拾う
        messages.warning(request, '存在しないユーザーです')


# ----------↓フォロワーアカウント一覧画面↓----------
@login_required
def followerlist_view(request, profile_id):
    try:
        follower = Profile.objects.get(pk=profile_id) #対象ユーザーのProfile
        connections = Connection.objects.filter(following__id=profile_id)
        follower_list = []
        for con in connections:
            follower_list.append(con.follower)
        context = {
            'follower_page': True,
            'follow_list': follower_list,
            'follow': follower,
        }
        return render(request, 'accounts/follow_list_view.html', context)
    except Profile.DoesNotExist: # 対象のプロフィールが見つからなかった場合のエラーを拾う
        messages.warning(request, '存在しないユーザーです')

# @login_required
# def follow(request):
#     partypost_pk = request.POST.get('partypost_pk')
#     context = {
#         'user': f'{request.user.last_name} {request.user.first_name}',
#     }
#     partypost = get_object_or_404(PartyPost, pk=partypost_pk)
#     like = LikeForPartyPost.objects.filter(target=partypost, user=request.user)

#     if like.exists():
#         like.delete()
#         context['method'] = 'delete'
#     else:
#         like.create(target=partypost, user=request.user)
#         context['method'] = 'create'

#     context['like_for_partypost_count'] = partypost.likeforpartypost_set.count()

#     return JsonResponse(context)