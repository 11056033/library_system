from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Mood, Profile, Book  
from .forms import ContactForm, PostForm, UserRegisterForm, LoginForm, ProfileForm
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic import ListView


# Create your views here.
def index(request):
    posts = Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods = Mood.objects.all()
        
    if request.method == 'GET':
        return render(request, 'myform.html', locals())
    elif request.method == 'POST':
        user_id = request.POST['user_id']
        user_pass = request.POST['user_pass']
        user_post = request.POST['user_post']
        user_mood = request.POST['mood']
        mood = Mood.objects.get(status=user_mood)
        post = Post(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = f'成功儲存！請記得你的編輯密碼[{user_pass}]!，訊息需經審查後才會顯示。'
        return render(request, 'myform.html', locals())
    else:
        message = 'post/get 出現錯誤'
        return render(request, 'myform.html', locals())
    
def delpost(request, pid): #delpost() got multiple values for argument 'pid'
    if pid:
        try:
            post = Post.objects.get(id=pid)
            post.delete()
        except:
            print('刪除錯誤!! pid=',pid)
            pass
    return redirect("/test")

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'myContact.html', locals())
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_message = form.cleaned_data['user_message']
            print('user_name:', user_name)
            print('user_message:', user_message)
        return render(request, 'myContact.html', locals())
    else:
        message = "ERROR"
        return render(request, 'myContact.html', locals())
    
def post2db(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'myPost2DB.html', locals())
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            form = PostForm()
            message = f'成功儲存！請記得你的編輯密碼!，訊息需經審查後才會顯示。'
        return render(request, 'myPost2DB.html', locals())
    else:
        message = "ERROR"
        return render(request, 'myPost2DB.html', locals())
    
from django.contrib.auth.models import User

def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'register.html', locals())
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_email = form.cleaned_data['user_email']
            user_password = form.cleaned_data['user_password']
            user_password_confirm = form.cleaned_data['user_password_confirm']
            if user_password == user_password_confirm:
                user = User.objects.create_user(user_name, user_email, user_password)
                message = f'註冊成功！'
            else:
                message = f'兩次密碼不一致！'    
        return render(request, 'register.html', locals())
    else:
        message = "ERROR"
        return render(request, 'register.html', locals())
    
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_password = form.cleaned_data['user_password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    message = '成功登入了'
                    return redirect('/')
                else:
                    message = '帳號尚未啟用'
            else:
                message = '登入失敗'

        return render(request, 'login.html', locals())
    else:
        message = "ERROR"
        return render(request, 'login.html', locals())
   
@login_required(login_url='/login/') 
def profile(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            username = request.user.username
            try:
                user = User.objects.get(username=username)
                userinfo = Profile.objects.get(user=user)
                form = ProfileForm(instance=userinfo)
            except:
                form = ProfileForm()
        return render(request, 'userinfo.html', locals())
    elif request.method == 'POST':
        username = request.user.username
        user = User.objects.get(username=username)
        try:
            userinfo = Profile.objects.get(user=user)
            form = ProfileForm(request.POST, instance=userinfo)
            form.save()
            message = f'成功更新個人資料！'
        except:
            form = ProfileForm(request.POST)
            userinfo = form.save(commit=False)
            userinfo.user = user
            userinfo.save()
            message = f'成功新增！'    
        return render(request, 'userinfo.html', locals())
    else:
        message = "ERROR"
        print('出錯回首頁')
        redirect("/")
# 新增注销功能
def user_logout(request):
    logout(request)
    return redirect('/')

def logout_view(request):
    logout(request)
    # 跳轉到你希望的頁面，例如首頁
    return redirect('homepage')

# 新增查看个人发表的留言功能
@login_required(login_url='/login/') 
def user_posts(request):
    user = request.user
    posts = Post.objects.filter(nickname=user.username).order_by('-pub_time')
    return render(request, 'user_posts.html', {'posts': posts})

# 新增修改留言功能
@login_required(login_url='/login/') 
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.nickname:
        if request.method == 'GET':
            form = PostForm(instance=post)
        elif request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('user_posts')
        return render(request, 'edit_post.html', {'form': form})
    else:
        return HttpResponseForbidden("You don't have permission to edit this post.")

# 新增删除留言功能
@login_required(login_url='/login/') 
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.nickname:
        post.delete()
        return redirect('user_posts')
    else:
        return HttpResponseForbidden("You don't have permission to delete this post.")

from django.views.generic import ListView
from django.shortcuts import redirect

class BookListView(ListView):
    model = Post
    template_name = 'book_list.html'
    context_object_name = 'books'

def keyword_search(request, keyword):
    # 构建重定向的 URL
    redirect_url = f'/post/book_{keyword}/'
    
    # 执行重定向
    return redirect(redirect_url)

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

