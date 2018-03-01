# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import connection
from page.views import Topic

def index(request):
    return render(request,'signin/index.html')


def create_user(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        nickname = request.POST.get('nickname')
        account = request.POST.get('account1')
        password = request.POST.get('password1')
        response = add_user(uid,nickname,account,password)
        if "wrong" in response:
            return render(request,'signin/wrong.html',{'message': response})
        else:
            return render(request,'signin/show.html',{'uid': uid,'nickname': nickname,'account': account,'password': password})


def sign_in(request):
    if request.method == 'POST':
        account = request.POST.get('account2')
        password = request.POST.get('password2')
        back = get_password(request,account)
        if password == back:
            return HttpResponseRedirect('/page/index/?account=%s' %(account))
        elif "wrong" in back:
            return render(request,'signin/wrong.html',{'message': back})
        else:
            return render(request,'signin/wrong.html',{'message': 'wrong password'})


def add_user(uid,nickname,account,password):
    cursor = connection.cursor()
    id = int(uid)
    sql = "insert into users(uid,account,password,nickname) values(%d,'%s','%s','%s')" \
            %(id,account,password,nickname)
    try:
        cursor.execute(sql)
        return "successful"
    except:
        return "wrong uid or account"


def get_password(request,account):
    cursor = connection.cursor()
    sql = "select password from users where account='%s'" % (account)
    try:
        s = cursor.execute(sql)
        if s:
            password = cursor.fetchone()
            return password[0]
        else:
            return "wrong account"
    except:
        return "None"