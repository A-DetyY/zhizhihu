from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url,static
from django.conf import settings
import page.views

urlpatterns = [
    url(r'^index/$',page.views.signin_index),
    url(r'^registered/$',page.views.create_user),
    url(r'^signin/$',page.views.sign_in),
    url(r'^index/(?P<uid>\d+)/$',page.views.index),
    url(r'^index/(?P<uid>\d+)/topics/$',page.views.show_topics),
    url(r'^index/(?P<uid>\d+)/topics/(?P<tid>\d+)/$',page.views.show_topic),
    url(r'^index/(?P<uid>\d+)/question/(?P<qid>\d+)/$',page.views.show_question),
    url(r'^index/(?P<uid>\d+)/question/(?P<qid>\d+)/idea/(?P<iid>\d+)/$',page.views.show_certain_idea),
    url(r'^index/(?P<uid>\d+)/question/(?P<qid>\d+)/idea/(?P<iid>\d+)/comments/$',page.views.show_comment),
    url(r'^index/(?P<uid>\d+)/mine/$',page.views.mine),
    url(r'^index/(?P<uid>\d+)/other/(?P<other>\d+)/$',page.views.other),
    url(r'^index/(?P<uid>\d+)/ask/$',page.views.ask_question),
    url(r'^index/ask_over/$',page.views.create_question),
    url(r'^index/make_idea/$',page.views.create_idea),
    url(r'^index/make_comment/$',page.views.create_comment),
    url(r'^index/add_good/',page.views.add_good),
    url(r'^index/cancel_good/',page.views.cancel_good),
    url(r'^index/add_bad/',page.views.add_bad),
    url(r'^index/cancel_bad/',page.views.cancel_bad),
    url(r'index/add_focus/',page.views.add_focus),
    url(r'index/cancel_focus/',page.views.cancel_focus),
    url(r'^index/changequestion/(?P<uid>\d+)-(?P<qid>\d+)/$',page.views.change_question),
    url(r'^index/(?P<uid>\d+)/savequestion/(?P<qid>\d+)/$',page.views.save_question),
    url(r'^index/deletequestion/(?P<uid>\d+)-(?P<qid>\d+)/$',page.views.delete_question),
    url(r'^index/changeidea/(?P<uid>\d+)-(?P<iid>\d+)/$',page.views.change_idea),
    url(r'^index/(?P<uid>\d+)/saveidea/(?P<iid>\d+)/$',page.views.save_idea),
    url(r'^index/deleteidea/(?P<uid>\d+)-(?P<iid>\d+)/$',page.views.delete_idea),
    url(r'^index/(?P<uid>\d+)/search/',page.views.search),
    url(r'^index/manage/$',page.views.manage),
    url(r'^index/deletetopic/(?P<tid>\d+)/$',page.views.delete_topic),
    url(r'^index/addtopic/$',page.views.add_topic),
]