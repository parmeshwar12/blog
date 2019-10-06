from django.shortcuts import render, get_object_or_404, redirect, reverse 
from .models import Post, Author, PostView
from marketing.models import Signup 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, PostForm
from django.db.models import Count, Q 

# Create your views here.
def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None 

def search(request):
    queryset = Post.objects.all() 
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    content = {
        'queryset': queryset
    }
    return render(request, 'post/search_results.html', content)

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset


def home(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email =  request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    content = {
        'object_list': featured,
        'latest': latest 
    }
    return render(request, 'post/index.html', content)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[0:3]
    
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post 
            form.save()
            return redirect(reverse("post:post", kwargs={
                'id': post.pk, 
            }))
    content = {
        'form': form,
        'post': post,
        'latest': latest,
        'category_count': category_count
        }
    return render(request, 'post/post.html', content)

def post_create(request):
    title = "Create"
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post:post', kwargs={
                'id': form.instance.id
            }))
    content = {
        'title': title,
        'form': form
    }
    return render(request, 'post/post_create.html', content)

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post:post', kwargs={
                'id': form.instance.id
            }))
    content = {
        'title': title,
        'form': form
    }
    return render(request, 'post/post_create.html', content)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('post:home')

def blog(request):
    post_list = Post.objects.all()
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[0:3]
    paginator = Paginator(post_list, 3)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    content = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'category_count': category_count
    }
    return render(request, 'post/blog.html', content)

def contact(request):
    return render(request, 'post/contact.html', {})