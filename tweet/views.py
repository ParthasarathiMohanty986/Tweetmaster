from django.shortcuts import render
from . forms import TweetForm,UserRegistrationForm
from . models import Tweet
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'index.html')

from django.shortcuts import render
from .models import Tweet  # Assuming you have a Tweet model
from django.db.models import Q  # For complex queries

def tweet_list(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter
    tweets = Tweet.objects.all()  # Default queryset

    if query:
        # Filter tweets based on the search query
        tweets = tweets.filter(
            Q(text__icontains=query) |  # Search in tweet content
            Q(user__username__icontains=query)  # Search in username (if you have a user field)
        )

    return render(request, 'tweet_list.html', {'tweets': tweets, 'query': query})


@login_required
def tweet_create(request):
    if request.method=="POST":
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
        
    else:
      form=TweetForm()

    return render(request,'tweet_form.html',{'form':form})
@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
        
    else:
            form=TweetForm(instance=tweet)


    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)  # Get the tweet by ID and check if it's the current user's tweet
    if request.method=='POST':
        tweet.delete()  # Delete the tweet
        return redirect('tweet_list')  # Redirect to the tweet list page after deleting
    
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})




def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
          
    else:
        form=UserRegistrationForm()

    return render(request,'registration/register.html',{'form':form})