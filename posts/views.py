from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from .forms import PostForm, CommentForm
from .models import Post, Comment, PostVote


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = Post(**form.cleaned_data, user=request.user)
            new_post.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'posts/view_post.html', {'post': post, 'comments': comments})


@login_required
def create_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=post_id)
            new_post = Comment(**form.cleaned_data, author=request.user, post=post)
            new_post.save()
            return HttpResponseRedirect(f'/posts/view/{post_id}')

    return render(request, 'posts/view_post.html')


@login_required
def vote(request, post_id):
    try:
        value = int(request.GET.get('value', 0))
    except ValueError:
        return HttpResponse(status=400)

    # Ensure that the vote is not an invalid amount
    if value not in [-1, 0, 1]:
        return HttpResponse(status=400)

    post = get_object_or_404(Post, pk=post_id)

    # Check that the user has not already voted on the post
    existing_votes = PostVote.objects.filter(post=post, user=request.user)
    if existing_votes:
        existing_vote = existing_votes[0]

        # If the existing vote is the same as the new vote, delete it
        if existing_vote.value == value:
            existing_vote.delete()
        else:
            existing_vote.value = value
            existing_vote.save()
    else:
        new_vote = PostVote(user=request.user, post=post, value=value)
        new_vote.save()

    return redirect(request.META.get('HTTP_REFERER', ''))
