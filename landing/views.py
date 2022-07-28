from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import connection
import datetime
from landing import unified_return_format as re
import json
from django.views import View
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, response
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect

now = timezone.now()
User = get_user_model()

from .models import Post, Comment, Notifications, Page

def list_usernames():
    return list(User.objects.all().values_list('username', flat=True)) 

def list_users():
    return list(User.objects.all()) 

def search(request):
    title = request.GET.get("q")
    users = [user.username for user in User.objects.all()]
    posts = [post.title for post in Post.objects.all()]
    if title in users and title not in posts:
        return HttpResponseRedirect(reverse("user",args=[title]))
    # elif title in posts and title not in users:
    #     return HttpResponseRedirect("posts/"+Post.objects.get(title=title).id)
    else:
        user_results = []
        post_results = []
        for entries in list(User.objects.all()):
            if str(title) in entries.username:
                user_results += [entries.username]
        for entries in list(Post.objects.all()):
            if str(title) in entries.title:
                post_results += [entries]
        return render(request, "landing/search.html", {
            "user_results": user_results,
            "post_results": post_results
        })

def index(request, *args, **kwargs):
    CurrentUser = request.user
    if request.GET.get("q"):
        return search(request)
    postlist = list(Post.objects.all())
    postlist.reverse()
    pages=list(Page.objects.all())
    return render(request, 'landing/index.html', {
        "user": CurrentUser,
        "userlist": list(User.objects.all()),
        "posts": postlist,
        "pages": pages
    })

def room(request, room_name):
    if request.GET.get("q"):
        return search(request)
    url = request.build_absolute_uri()

    current_user = request.user
    users = room_name.split('a')
    if request.user.id == int(users[0]):
        to_user_id = int(users[1])
    else:
        to_user_id = int(users[0])
    to_user = User.objects.get(id=to_user_id)
    if to_user.is_authenticated: status = 0 
    else: status = 1
    # User.objects.get(id='')
    return render(request, 'landing/room.html', {
        'room_name': room_name,
        'user': request.user,
        'to_user': to_user,
        'status': status
        # 'sender': 
    })

def profile(request):
    user=request.user
    friends = user.friends.all()
    if request.GET.get("q"):
        return search(request)
    if request.method == "POST": 
        if request.POST.get("theme"):
            print(request.POST.get("theme"))
            setattr(request.user, 'theme', request.POST.get("theme"))
            request.user.save()
    try:
        posts = list(Post.objects.filter(user=user))
        try:
            friend_reqs = list(Friend_request.objects.filter(to_user=request.user))
        except:
            friend_reqs = ""
        if len(posts) == 0:
            noposts="No posts yet!"
        else:
            noposts=""
        return render(request, "landing/profile.html",{
            "user":user,
            "posts": posts,
            "noposts": noposts,
            "num_posts":len(posts),
            "friend_reqs": friend_reqs,
            "friend_list": friends
        } )
    except:
        return render(request, "landing/profile.html",{
            "user":user,
            "noposts":noposts,
            "num_posts":0,
            "friend_reqs": friend_reqs,
            "friend_list": friends
        } )

from .forms import *
def post(request):
    if request.GET.get("q"):
        return search(request)
    elif request.method == 'POST':
        image_form = PostImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_form.instance.user = request.user
            image_form.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        image_form = PostImageForm()
        return render(request, 'landing/post.html', {'image_form': image_form})

def create_page(request):
    if request.GET.get("q"):
        return search(request)
    elif request.method == 'POST':
        page_form=CreatePageForm(request.POST, request.FILES)
        if page_form.is_valid():
            page_form.instance.user = request.user
            page = page_form.save()
            page.created_by=str(request.user)
            page.save()
            request.user.pages.add(page)
            request.user.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        page_form = CreatePageForm()
        return render(request, "landing/create_page.html", {"page_form": page_form})

def get_pages(request):
    print("I am in get_pages function")
    if request.GET.get("q"):
        pages = list(Page.objects.all())
        print(pages)
        return render((request, "landing/index.html", {"pages" : pages}))
  
  
def success(request):
    return HttpResponse('successfully uploaded')



def innerpost(request,post_id):
    if request.GET.get("q"):
        return search(request)
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST": 
        if request.POST.get("comment"):
            post.comments+=1
            post.save()
            comment = Comment(description=request.POST.get("comment"),post=post,time=str(now)[:16],user=request.user)
            comment.save()
        elif request.POST.get("like"):
            post.likes+=1
            post.liked_users.add(request.user)
            post.save()
            # request.user.likes.add(post)
            # request.user.save()
        elif request.POST.get("unlike"):
            post.likes-=1
            post.liked_users.remove(request.user)
            post.save()
            # request.user.likes.remove(post)
            # request.user.save()
        return HttpResponseRedirect(reverse("innerpost",args=[post.id]))
    return render(request, "landing/innerpost.html", {
        "post": post,
        "comments": list(comments),
        "liked_users": list(post.liked_users.all())
    })

def user(request, username):
    if request.GET.get("q"):
        return search(request)
    user = User.objects.get(username=username)
    try:
        if (Friend_request.objects.get(from_user=request.user,to_user=user)):
            message="Friend Request Sent"
    except:
        if user.friends.filter(id = request.user.id):
            message="Friend"
        else:
            message= "Friend Request"
    try:
        posts = list(Post.objects.filter(user=user))
        if len(posts) == 0:
            noposts="No posts yet!"
        else:
            noposts=""
        return render(request, "landing/user.html",{
            "user":user,
            "posts": posts,
            "noposts": noposts,
            "message":message
        } )
    except:
        return render(request, "landing/user.html",{
            "user":user,
            "message":message
        } )

def send_friend_request(request,id):
    from_user = request.user
    to_user = User.objects.get(id=id)
    friend_request,created = Friend_request.objects.get_or_create(from_user=from_user,to_user=to_user)
    if created:
        # return render(request, "landing/user.html", {
        #   "user":to_user,
        #   "posts": list(Post.objects.filter(user=user))
        # })
        return user(request,to_user.username)

    else:
        return user(request,to_user.username)

def accept_friend_request(request,id):
    friend_request = Friend_request.objects.get(id=id)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponseRedirect(reverse("profile"))
    else:
        return HttpResponse('friend request not accepted')
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView

def ProfileEditView(request, username):
    if request.GET.get("q"):
        return search(request)
    elif request.method == 'POST':
        profile_edit_form=ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if profile_edit_form.is_valid():
            request.user.bio = profile_edit_form['bio'].value()
            # request.user.picture = profile_edit_form['picture']
            profile_edit_form.save()
            request.user.save()
        return HttpResponseRedirect(reverse("profile"))
    else:
        profile_edit_form = ProfileEditForm()
        return render(request, "landing/profile_edit.html", {"profile_edit_form": profile_edit_form})

def pages_pay(request, page_id):
    if request.GET.get("q"):
        return search(request)
    page = Page.objects.get(pk=page_id)

    if request.method == 'POST':
        n = Notifications()
        n.description= request.POST['amount']+" was donated by "+request.user.username+" to your page "+page.name
        n.time=str(now)[:16]
        end_user = User.objects.get(username=page.created_by)
        n.notification_type="Donation"
        n.save()
        end_user.notifications.add(n)
        end_user.save()
        return render(request,"landing/payment_successfull.html")
    return render(request, "landing/pay.html", {"page_name": page.name})
def products_pay(request, product_id):
        product = Product.objects.get(pk=product_id)
        comments = Comment.objects.filter(product=product)

        if request.method == 'POST':
            n = Notifications()
            n.description= request.POST['amount']+" was paid by"+request.user.username+" for your product "+product.product_name
            n.time=str(now)[:16]
            end_user = User.objects.get(username=product.user.username)
            n.notification_type="Product"
            n.save()
            end_user.notifications.add(n)
            end_user.save()
            return render(request,"landing/payment_successfull.html")

        return render(request, "landing/pay.html", {"page_name": product.product_name})

def page_detail(request, page_id):
    if request.GET.get("q"):
        return search(request)
    page = Page.objects.get(pk=page_id)
    members = list(User.objects.filter(pages=page))
    comments = list(Comment.objects.filter(page=page))

    if request.method == "POST": 
        if request.POST.get("join"):
            request.user.pages.add(page)
            request.user.save()
            return HttpResponseRedirect(reverse("page_detail",args=[page.id]))
        elif request.POST.get("comment"):
            page.comments+=1
            page.save()
            comment = Comment(description=request.POST.get("comment"),page=page,time=str(now)[:16],user=request.user)
            comment.save()
            return HttpResponseRedirect(reverse("page_detail",args=[page.id]))
        elif request.POST.get("Leave"):
            request.user.pages.remove(page)
            request.user.save()
            print(request.user.pages)
            return HttpResponseRedirect(reverse("page_detail",args=[page.id]))

    return render(request, "landing/page_detail.html", {
        "page": page,
        "members":members,
        "comments": comments
        })

def payment_successfull(request):
    if request.GET.get("q"):
        return search(request)
    return render(request, "landing/payment_successfull.html")

def marketplace_main(request):
    if request.GET.get("q"):
        return search(request)
    products = list(Product.objects.all())
    return render(request, "landing/marketplace_main.html", {"products": products})

def register_product(request):
    if request.GET.get("q"):
        return search(request)
    elif request.method == 'POST':
        product_form=RegisterProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.instance.user = request.user
            product_form.save()

        return HttpResponseRedirect(reverse("marketplace_main"))
    else:
        product_form = RegisterProductForm()
        return render(request, "landing/register_product.html", {"product_form": product_form})

def product_detail(request, product_id):
    if request.GET.get("q"):
        return search(request)
    product = Product.objects.get(pk=product_id)
    comments = Comment.objects.filter(product=product)
    if request.method == "POST": 
        if request.POST.get("comment"):
            product.comments+=1
            product.save()
            comment = Comment(description=request.POST.get("comment"),product=product,time=str(now)[:16],user=request.user)
            comment.save()
        elif request.POST.get("like"):
            product.likes+=1
            product.save()
        return HttpResponseRedirect(reverse("product_detail",args=[product.id]))

    return render(request, "landing/product_detail.html", {"product": product, "comments": comments})

def notifications(request):
    #pages=request.user.pages.all()
    notifications=request.user.notifications.all()
    if request.GET.get("q"):
        return search(request)
    return render(request, "landing/notifications.html", {"notifications":notifications})