from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import SignUpForm, EditProfileForm
from django.urls import reverse
from .models import Profile
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.template import loader
from movie.models import Review, Movie, Likes
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("account:login")


@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('movie:index')
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'edit_profile.html', context)


def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    # MovieBoxData
    mWatched_count = profile.watched.filter(Type='movie').count()
    sWatched_count = profile.watched.filter(Type='series').count()
    watch_list_count = profile.to_watch.all().count()
    m_reviewd_count = Review.objects.filter(user=user).count()

    context = {
        'profile': profile,
        'mWatched_count': mWatched_count,
        'sWatched_count': sWatched_count,
        'watch_list_count': watch_list_count,
        'm_reviewd_count': m_reviewd_count,
    }

    template = loader.get_template('profile.html')

    return HttpResponse(template.render(context, request))


def UserProfileMoviesWatched(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    # Movies List
    movies = profile.watched.filter(Type='movie')
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'list_title': 'Movies Watched',
    }

    template = loader.get_template('movie_list.html')

    return HttpResponse(template.render(context, request))


def UserProfileSeriesWatched(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    # Series List
    movies = profile.watched.filter(Type='series')
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'list_title': 'Series Watched',
    }

    template = loader.get_template('movie_list.html')

    return HttpResponse(template.render(context, request))


def UserProfileWatchList(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    # Watch List
    movies = profile.to_watch.all()
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'list_title': 'Watch list',
    }

    template = loader.get_template('movie_list.html')

    return HttpResponse(template.render(context, request))


def UserProfileMoviesReviewed(request, username):
    user = get_object_or_404(User, username=username)

    # reviewed List - using reverse relation

    movies = Movie.objects.filter(review__user=user)
    print(movies)
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'list_title': 'Reviewed',
    }

    template = loader.get_template('movie_list.html')

    return HttpResponse(template.render(context, request))


@login_required
def ReviewDetail(request, username, imdb_id):
    user_comment = request.user
    user = get_object_or_404(User, username=username)
    movie = Movie.objects.get(imdbID=imdb_id)
    review = Review.objects.get(user=user, movie=movie)

    # Comment stuff:
    comments = Comment.objects.filter(review=review).order_by('date')

    # Comment Form stuff:
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = user_comment
            comment.save()
            return HttpResponseRedirect(reverse('movie:user-review', args=[username, imdb_id]))
    else:
        form = CommentForm()

    context = {
        'review': review,
        'movie_data': movie,
        'comments': comments,
        'form': form,
    }

    template = loader.get_template('movie_review.html')

    return HttpResponse(template.render(context, request))


@login_required
def like(request, username, imdb_id):
    user_liking = request.user
    user_review = get_object_or_404(User, username=username)
    movie = Movie.objects.get(imdbID=imdb_id)
    review = Review.objects.get(user=user_review, movie=movie)
    current_likes = review.likes

    liked = Likes.objects.filter(
        user=user_liking, review=review, type_like=2).count()

    if not liked:
        like = Likes.objects.create(
            user=user_liking, review=review, type_like=2)
        current_likes = current_likes + 1

    else:
        Likes.objects.filter(
            user=user_liking, review=review, type_like=2).delete()
        current_likes = current_likes - 1

    review.likes = current_likes
    review.save()

    return HttpResponseRedirect(reverse('movie:user-review', args=[username, imdb_id]))


@login_required
def unlike(request, username, imdb_id):
    user_unliking = request.user
    user_review = get_object_or_404(User, username=username)
    movie = Movie.objects.get(imdbID=imdb_id)
    review = Review.objects.get(user=user_review, movie=movie)
    current_likes = review.unlikes

    liked = Likes.objects.filter(
        user=user_unliking, review=review, type_like=1).count()

    if not liked:
        like = Likes.objects.create(
            user=user_unliking, review=review, type_like=1)
        current_likes = current_likes + 1

    else:
        Likes.objects.filter(
            user=user_unliking, review=review, type_like=1).delete()
        current_likes = current_likes - 1

    review.unlikes = current_likes
    review.save()

    return HttpResponseRedirect(reverse('movie:user-review', args=[username, imdb_id]))
