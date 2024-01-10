from django.shortcuts import render
from library_search.models import Post
# Create your views here.
def search_books(request):
    if request.method == 'GET':
        search_query = request.GET.post('keyword', '')
        books = Post.objects.filter(title__icontains=search_query)
        return render(request, 'book_list.html', {'books': books})
    else:
        return render(request, 'book_list.html', {'books': []})
    

    