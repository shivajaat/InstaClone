from django.conf.urls import url
from django.contrib import admin
from instaclone.views import signup,login,feed_view,post_view,like_view,comment_view,images_tags,detail
urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^post/', post_view),
    url(r'feed/', feed_view),
    url(r'login/', login),
    url(r'comment/', comment_view),
    url(r'like/', like_view),
    url(r'^nature',images_tags,name='images_tags'),
    url(r'(?P<tag>[0-9]+)/nature/',detail,name='detail'),
    #url(r'^mountain',detail,name='details'),
    #url(r'(?P<tag>[0-9]+)/mountain/',detail,name='detail'),
    url('', signup),

]