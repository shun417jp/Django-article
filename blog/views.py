from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .models import Article
from .forms import ArticleForm
from .forms import SignUpForm
from .forms import ProfileForm
from django.http import JsonResponse

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})


def article_list(request):
    articles = Article.objects.all().select_related('author')
    user = request.user
    for article in articles:
        article.likes_count = article.likes.count()
        if user.is_authenticated:
            article.liked_by_user = article.likes.filter(id=user.id).exists()
        else:
            article.liked_by_user = False
    context = {
        'articles': articles,
    }
    return render(request, 'blog/article_list.html', context)

# filepath: c:\Users\tomak\Desktop\Django\kiji\blog\views.py
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, published=True)
    article.likes_count = article.likes.count()
    article.liked_by_user = False
    if request.user.is_authenticated:
        article.liked_by_user = article.likes.filter(id=request.user.id).exists()
    return render(request, 'blog/article_detail.html', {'article': article})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author:
        return HttpResponseForbidden("この操作は許可されていません。")

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)

    # GET時 または POSTでformが無効な時
    return render(request, 'blog/article_edit.html', {'form': form, 'article': article})
    
@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article,pk=pk)
    
    if request.user != article.author:
        return HttpResponseForbidden("この操作は許可されていません。")
    
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    
    return render(request, 'blog/article_confirm_Delete.html', {'article': article})
        
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後自動ログイン
            return redirect('article_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/edit_profile.html', {'form': form})

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    articles = user.article_set.filter(published=True).order_by('-created_at')
    return render(request, 'blog/profile_detail.html', {
        'profile_user': user,
        'articles': articles,
    })
    
def user_article_list(request,username):
    user = get_object_or_404(User,username=username)
    article = Article.objects.filter(author=user, punlished=True).order_by('-created_at')
    return render(request,'blog/user_article_list.html',{'profile_user':user,'article':article})

from django.http import JsonResponse

@login_required
def toggle_like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    user = request.user

    if user in article.likes.all():
        article.likes.remove(user)
        liked = False
    else:
        article.likes.add(user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': article.likes.count()})
    return redirect('article_detail', pk=article_id)