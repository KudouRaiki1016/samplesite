from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('partypost/create/', views.create_post, name='create-partypost'), #編成投稿
    path('folder/', views.folderlist_view, name='list-folder'), #フォルダ一覧
    path('create/folder/', views.CreateFolderView.as_view(), name='create-folder'), #フォルダ作成
    path('folder/<int:folder_id>/partypost', views.partypost_save_in_folder_view, name='list-partypost_in_folder'), #フォルダ内編成一覧
    path('folder/orderchange/', views.orderchange_folder, name='orderchange-folder'), #フォルダ並び替え
    path('folder/<int:pk>/delete/', views.DeleteFolderView.as_view(), name='delete-folder'), #フォルダ削除
    path('like_for_partypost/', views.like_for_partypost, name='like_for_partypost'), #いいね処理
    path('update_comment', views.update_comment, name='update-comment'), #コメント編集処理
    path('delete_comment', views.delete_comment, name='delete-comment'), #コメント削除処理
    path('partypost/detail/<int:partypost_id>/', views.detail_partypost_view, name='detail-partypost'), #編成詳細
    path('reply_acquisition/', views.reply_acquisition_view, name='reply-acquisition'), #リプライ情報取得処理
    path('folder/<int:folder_id>/partypost/append/', views.append_partypost_in_folder, name='append-partypost_in_folder'), #フォルダに保存
    path('folder/<int:folder_id>/partypost/delete/', views.delete_partypost_in_folder, name='delete-partypost_in_folder'), #フォルダから削除
    path('aaaaa/<int:profile_id>/', views.sample_view, name='sample'), #あとで消す
    path('', views.top_view, name='top-page'), #トップページ
]