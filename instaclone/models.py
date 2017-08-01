from django.db import models
import uuid
# Create your models here.


class UserModel(models.Model):
  username = models.CharField(max_length=120)
  name = models.CharField(max_length=100)
  email = models.CharField(unique=True,max_length=100)
  password = models.CharField(max_length=200)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  def _str_(self):
    return self.username + ' ' + 'Created'


class Token(models.Model):
  user = models.ForeignKey(UserModel)
  session_token = models.CharField(max_length=100)
  created_on = models.DateTimeField(auto_now_add=True)
  valid = models.BooleanField(default=True)

  def create_token(self):
    self.session_token = uuid.uuid4()


class Post(models.Model):
  user = models.ForeignKey(UserModel)
  image = models.FileField(upload_to='user_images')
  img_url = models.CharField(max_length=200)
  caption = models.CharField(max_length=200)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  has_liked = False

  @property
  def like_count(self):
    return len(Like.objects.filter(post=self))

  @property
  def comments(self):
    return Comment.objects.filter(post=self).order_by('created_on')


class Like(models.Model):
  user = models.ForeignKey(UserModel)
  post = models.ForeignKey(Post)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

class Comment(models.Model):
  user = models.ForeignKey(UserModel)
  post = models.ForeignKey(Post)
  comment_text = models.CharField(max_length=555)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)


class tags(models.Model):
  post = models.ForeignKey(Post)
  tag = models.CharField(max_length=2000)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
