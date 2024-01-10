from django.contrib import admin
from django.urls import path
from mysite import views as mv
from mytest import views as testv
from library_search import views as tv
from django.urls import path
from mytest.views import BookListView, keyword_search
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mv.homepage, name="homepage"),
    path('post/<slug:slug>/', mv.showpost, name="showpost"),
    path('post/', mv.show_all_posts, name="show-all-posts"),
    path('post/<int:post_id>/comments', mv.show_comments, name='show-comments'),
    path('about/', mv.about),
    path('about/<int:num>', mv.about, name='about'),
    path('carlist/', mv.carlist),
    path('carlist/<int:maker>/', mv.carlist, name='carlist-url'),
    path('post/new', mv.new_post, name="post-new"),
    path('test/', testv.index, name="test-new"),
    path('test/delpost/<int:pid>/', testv.delpost),
    path('test/contact', testv.contact),
    path('post2db/', testv.post2db),
    path('register/', testv.register, name='register'), 
    path('login/', testv.login_view, name='login'),
    path('profile/', testv.profile),
    path('logout/', testv.user_logout, name='logout'),
    path('user_posts/', testv.user_posts, name='user_posts'),
    path('edit_post/<int:post_id>/', testv.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', testv.delete_post, name='delete_post'),
    path('search/<str:keyword>/', keyword_search, name='keyword_search'),
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('search_books/', tv.search_books, name='search_books'),
    ]



