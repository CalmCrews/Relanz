from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import ArticleForm
from .models import Article, Like, Participant
from user.models import User
from challenge.models import Challenge
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='/user/signin')
def communityHome(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    articles = Article.objects.filter(challenge=challenge) # a 챌린지의 게시물들만 가져오기
    
    paginator = Paginator(articles, 3) # 한페이지 당 사진 3개로 설정
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    res_data = {'articles': articles, 'challenge':challenge, 'page_obj':page_obj}
    return render(request, 'community/communityHome.html', res_data)

@login_required(login_url='/user/signin')
def new(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    try:
        participant = Participant.objects.get(user=request.user, challenge=challenge)
    
    # 챌린지에 참여하지 않았는데, 글을 작성하려고 할 때
    except Participant.DoesNotExist:
        return redirect('community:communityHome', challenge_id)
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = participant
            article.challenge = challenge
            article.user = request.user
            duplication_article = Article.objects.filter(author=participant, challenge=challenge)
            if duplication_article.exists():
                article.article_score = 100
            else:
                article.article_score = 500
            article.save()
            user=User.objects.get(id=request.user.id)
            user.score += article.article_score
            user.save()
            return redirect('community:detail', challenge.id, article.id)
    
    res_data = {'form':form, 'challenge':challenge}
    return render(request, 'community/new.html', res_data)

@login_required(login_url='/user/signin')
def detail(request, challenge_id, article_id):
    challenge = Challenge.objects.get(id=challenge_id)
    article = get_object_or_404(Article, pk=article_id)
    like_count = len(Like.objects.filter(article=article))
    author_nickname = article.author.user.nickname

    res_data = {'challenge':challenge, 'article':article, 'like_count':like_count, 'author_nickname':author_nickname}
    return render(request, 'community/detail.html', res_data)

@login_required(login_url='/user/signin')
def edit(request, challenge_id, article_id):
    challenge = Challenge.objects.get(id=challenge_id)
    article = get_object_or_404(Article, pk=article_id)

    form = ArticleForm(instance=article)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            article = form.save()
            return redirect('community:detail', challenge.id, article.id)
    
    res_data = {'form':form, 'challenge':challenge, 'article':article}
    return render(request, 'community/edit.html', res_data)

@login_required(login_url='/user/signin')
def delete(request, challenge_id, article_id):
    article = get_object_or_404(Article, pk=article_id)

    article.delete()

    return redirect('main:home')

@login_required(login_url='/user/signin')
def like(request, article_id):   
    article = get_object_or_404(Article, pk=article_id)

    # 이미 좋아요 누른 경우 detail로 이동, 본인 글에 좋아요 누르기 가능
    if Like.objects.filter(likedUser=request.user, article=article).exists():
        return redirect("community:detail", challenge_id=article.challenge.id, article_id=article.id)
    
    # 좋아요 아직 안 누른 경우 Like 객체 만들기
    like = Like()
    like.article = get_object_or_404(Article, pk=article_id)
    like.likedUser = request.user
    like.save()
    return redirect('community:detail', challenge_id=article.challenge.id, article_id=article.id)


# # a 참가자의 글들을 a 유저에 저장
# def save_articles(request, participant_id):
#     try:
#         participant = Participant.objects.get(id=participant_id)
#         user = participant.user

#         # participant_id의 글들 저장
#         articles = participant.article_set.all()
#         for article in articles:
#             Article.objects.create(author=participant, user=user, image=article.image)
            
#     except Participant.DoesNotExist:
#         return HttpResponse("참여자가 존재하지 않습니다")