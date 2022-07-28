from django.urls import path
from landing import views
from social import views as soview
from django.conf.urls import include
from django.contrib import admin
from social.templates.event import urls as us
urlpatterns = [
    path('', views.index, name='index'),
    # path('user_list', views.user_list, name='templates/user_list.html'),
    # path('add_superuser', views.add_superuser),
    # path('add_user', views.add_user, name='templates/index.html'),
    # path('login', views.login, name='templates/index.html'),
    # path('friend_request', soview.friend_request, name='templates/index.html'),
    # path('accept_request', soview.accept_request, name='templates/index.html'),
    # path('if_friend', soview.if_friend, name='templates/index.html'),
    # path('edit_profile', soview.edit_profile, name='templates/index.html'),
    # path('get_profile', soview.get_profile, name='templates/index.html'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('profile', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('post', views.post, name='post'),
    path('add_post', soview.add_post, name='add_post'),
    path('show_post', soview.show_post, name = 'show_post'),
    path('post', soview.show_post, name = 'show_post'),
    path('posts/<int:post_id>', views.innerpost,name='innerpost'),
    path('users/users/<str:username>/', views.user,name='user'),
    path('profile/edit/<str:username>/', views.ProfileEditView, name='profile-edit'),
    path('send_friend_request/<int:id>/', views.send_friend_request,name='send friend request'),
    path('accept_friend_request/<int:id>/', views.accept_friend_request,name='accept friend request'),
    path('pages/pay/<int:page_id>', views.pages_pay,name='pages_pay'),
    path('product/pay/<int:product_id>', views.products_pay,name='products_pay'),
    path('create_page', views.create_page, name='create_page'),
    path('pages', views.get_pages, name='templates/index.html'),
    path('pages/<int:page_id>', views.page_detail, name='page_detail'),
    path('payment_successfull', views.payment_successfull, name='payment_successfull'),
    path('profile_edit',views.ProfileEditView, name='profile_edit'),
    path('marketplace_main', views.marketplace_main, name='marketplace_main'),
    path('register_product', views.register_product, name='register_product'),
    path('product_detail<int:product_id>', views.product_detail, name='product_detail'),
    path('notifications', views.notifications, name='notifications'),
    # path('admin/', admin.site.urls),
    # path('event/', include(('social.templates.event.urls', 'social'), namespace='event')),
] 
