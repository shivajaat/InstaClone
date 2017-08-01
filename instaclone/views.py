from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.http import HttpResponse
from forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm,tagsform
from models import Token,UserModel,Post,Like,Comment,tags
from django.contrib.auth.hashers import make_password,check_password
from jango786.settings import BASE_DIR
from imgurpython import ImgurClient
from clarifai import rest
from clarifai.rest import ClarifaiApp
# Create your views here.
Client_ID = '36b18adcae39de1'
Client_secret = '487e8c94337499b2d2309743dab4e33805169575'
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html', {'form':form})
        else:
            print 'Invalid'
    elif request.method == "GET":
        form = SignUpForm()
    return render(request, 'template.html', {'form': form})


def login(request):
    response_data = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()
            if user:
                if check_password(password, user.password):
                    print 'User is valid'
                    token = Token(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    print 'User is invalid'
            else:
                print 'Something Wrong!'
        else:
          print 'form not valid!'
    elif request.method == ('GET'):
        form = LoginForm()
        response_data['form'] = form
    return render(request, 'login.html',response_data)


def post_view(request):
    user = check_validation(request)
    if user:
        print 'valid user'
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                print 'valid form'
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = Post(user=user, image=image, caption=caption)
                post.save()
                print 'valid post'
                app = ClarifaiApp(api_key='c39920c18ad240df9f511511045ab2e2')
                path = str(BASE_DIR + '/' + post.image.url)
                print path
                client = ImgurClient(Client_ID, Client_secret)
                post.img_url = client.upload_from_path(path, anon=True)['link']
                print post.img_url
                post.save()
                model = app.models.get("general-v1.3")
                response = model.predict_by_url(post.img_url)
                print response
                r = response['outputs'][0]['data']['concepts']
                for i in range(len(r)):
                    p = r[i]['name']
                    print p
                    temp = tags.objects.create(post=post,tag=p)
                    temp.save()
                print 'Got Link'
                return redirect('/feed/')
        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')

def images_tags(request):
    return feed_view(request,'nature')




def detail(request,tag):
    print "okkkk...."
    tags.objects.filter(tag='nature')
    return HttpResponse("<h1>cool</h1>" + tag )


def feed_view(request,tag='all'):
    user = check_validation(request)
    print 'yes'
    if user:
        print'valid'
        if tag == 'all':
             print 'all tags used'
             posts = Post.objects.all().order_by('created_on')
        else:
            print 'not all are used'
            posts = tags.objects.filter(tag=tag)
           # p=Post.objects.filter(post_id=posts.Post.id)
        for post in posts:
            print 'posts'
            existing_like = Like.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
            print 'oh yes'
            return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = Like.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                Like.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')
def comment_view(request):
  user = check_validation(request)
  if user and request.method == 'POST':
      form = CommentForm(request.POST)
      if form.is_valid():
          post_id = form.cleaned_data.get('post').id
          comment_text = form.cleaned_data.get('comment_text')
          comment = Comment.objects.create(user=user, post_id=post_id, comment_text=comment_text)
          comment.save()
          return redirect('/feed/')
      else:
          print 'Invalid'
          return redirect('/feed/')
  else:
      print 'Something else.....'
      return redirect('/login')

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = Token.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
           return session.user
    else:
        return None


