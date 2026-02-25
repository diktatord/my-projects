from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm, CommentForm
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView



def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all().order_by('created_at')


    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST,request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.author = request.user
                comment.save()
                return redirect('article_detail', pk=pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})


@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        return redirect('article_list')

    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/article_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'blog/login.html'


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('article_list')
    return redirect('article_list')


