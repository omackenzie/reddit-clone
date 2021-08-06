from django.shortcuts import render
from posts.models import Post, PostVote


def home_page(request):
    posts = Post.objects.all()

    # Get posts the user has voted on
    if request.user.is_authenticated:
        votes = PostVote.objects.filter(user=request.user)
        voted_posts = [vote.post for vote in votes]
    else:
        votes = []
        voted_posts = []

    return render(request, 'core/home.html', {'posts': posts, 'votes': votes, 'voted_posts': voted_posts})
