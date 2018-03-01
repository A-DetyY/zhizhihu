# coding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.db import connection
import random
import json
import time
import math

class Topic:
    def __init__(self,id,name,num,focus):
        self.tid = id;
        self.name = name
        self.quenum = num
        self.focus = focus


class Question:
    def __init__(self,qid,title,content,time,ideanum):
        self.qid = qid
        self.title = title
        self.content = content
        self.time = time
        self.ideanum = ideanum


class Idea:
    def __init__(self,id,content,time,commentnum,good,bad,uid,nickname):
        self.iid = id
        self.content = content
        self.time = time
        self.commentnum = commentnum
        self.good = good
        self.bad = bad
        self.uid = uid
        self.nickname = nickname


class Comment:
    def __init__(self,name,content,time,good,bad):
        self.nickname = name
        self.content = content
        self.time = time
        self.good = good
        self.bad = bad


class User:
    def __init__(self,id,account,password,nickname):
        self.uid = id
        self.account = account
        self.password = password
        self.nickname = nickname


class People:
    def __init__(self,id,nickname,answer,ask,focus):
        self.uid = id
        self.nickname = nickname
        self.answer = answer
        self.ask = ask
        self.focus = focus


class Index:
    def __init__(self,tid,name,qid,question,id,content,time,commentnum,good,bad,uid,nickname):
        self.tid = tid
        self.name = name
        self.qid = qid
        self.question = question
        self.idea = Idea(id,content,time,commentnum,good,bad,uid,nickname)


def signin_index(request):
    return render(request,'page/login(1).html')


def create_user(request):
    if request.method == 'POST':
        #uid = request.POST.get('uid')
        nickname = request.POST.get('nickname1')
        account = request.POST.get('account1')
        password = request.POST.get('password1')
        password3 = request.POST.get('password3')

        if password!=password3:
            return render(request,'page/registered_wrong.html',{'message': '两次密码不一致'})

        response = add_user(nickname,account,password)
        if response == "fail":
            return render(request, 'page/registered_wrong.html', {'message': '该账号已被注册'})
        else:
            return HttpResponseRedirect('/page/index/%s/' % (response))


def sign_in(request):
    if request.method == 'POST':
        account = request.POST.get('account2')
        password = request.POST.get('password2')
        back = get_password(request,account)
        if password == back:
            uid = str(get_uid(account))
            return HttpResponseRedirect('/page/index/%s/' % (uid))
        elif back == 'wrong account':
            return render(request,'page/wrong.html',{'message': back})
        else:
            return render(request,'page/wrong.html',{'message': 'wrong password'})


def add_user(nickname,account,password):
    cursor = connection.cursor()
    sql = "select count(*) from users"
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    sql = "insert into users(uid,account,password,nickname) values(%d,'%s','%s','%s')" \
            %(id+1,account,password,nickname)
    try:
        cursor.execute(sql)
        return str(id+1)
    except:
        return "fail"


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


def get_uid(account):
    cursor = connection.cursor()
    sql = "select uid from users where account='%s'" % (account)
    cursor.execute(sql)
    uid = cursor.fetchone()[0]
    return uid


def get_account(uid):
    cursor = connection.cursor()
    sql = "select account from users where uid=%d" % (uid)
    cursor.execute(sql)
    account = cursor.fetchone()[0]
    return account


def get_nickname(uid):
    cursor = connection.cursor()
    sql = "select nickname from users where uid=%d" % (uid)
    cursor.execute(sql)
    nickname = cursor.fetchone()[0]
    return nickname


def index(request, uid):
    uid = int(uid)
    account = get_account(uid)

    if uid == 5 and account == "123":
        return HttpResponseRedirect('/page/index/manage/')

    lists = []
    lists = get_intersted(uid)
    nickname = get_nickname(uid)
    if len(lists) == 0:
        return HttpResponseRedirect('/page/index/%d/topics/' % (uid))
    else:
        return render(request, 'page/zhihu(1).html',{
            'uid': uid,
            'account': account,
            'nickname': nickname,
            'lists': lists }
        )


def get_intersted(uid):
    cursor = connection.cursor()
    list = []
    qids = []
    sql = "select qid from questions where tid in (select tid from focus where uid=%d)" % (uid)
    cursor.execute(sql)
    for data in cursor.fetchall():
        qids.append(data[0])

    if len(qids) == 0:
        return list

    if len(qids)>=10:
        slice = random.sample(qids,10)
    else:
        slice = qids[:]


    for i in range(0,len(slice)):
        sql = "select questions.tid,topics.name,qid,title from questions,topics where topics.tid=questions.tid and qid=%d" %(slice[i])
        cursor.execute(sql)
        question = cursor.fetchone()
        iids = []
        sql = "select iid from ideas where qid=%d" %(slice[i])
        cursor.execute(sql)
        for data in cursor.fetchall():
            iids.append(data[0])
        if len(iids):
            iid = random.sample(iids,1)[0]
            sql = "select iid,content,time,commentnum,good,bad,ideas.uid,nickname from ideas,users where ideas.uid=users.uid and iid=%d" % (iid)
            cursor.execute(sql)
            data = cursor.fetchone()
            list.append(Index(question[0],question[1],question[2],question[3],data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))

    return list


def show_topics(request,uid):
    uid = int(uid)
    account = get_account(uid)
    nickname = get_nickname(uid)
    cursor = connection.cursor()

    # 获取该用户已关注的话题id
    focus = []
    sql = "select tid from focus where uid=%d" %(uid)
    cursor.execute(sql)
    for data in cursor.fetchall():
        focus.append(data[0])

    list = []
    sql = "select * from topics"
    try:
        cursor.execute(sql)
        for data in cursor.fetchall():
            if data[0] in focus:
                list.append(Topic(data[0],data[1],data[2],1))
            else:
                list.append(Topic(data[0],data[1],data[2],0))
        return render(request, 'page/topic(1).html',{
            'uid': uid,
            'account': account,
            'nickname': nickname,
            'topics': list }
        )
    except:
        return render(request,'page/wrong.html',{'message': 'wrong execute'})


def show_topic(request,uid,tid):
    uid = int(uid)
    account = get_account(uid)
    nickname = get_nickname(uid)
    tid = int(tid)
    cursor = connection.cursor()
    sql = "select name from topics where tid=%d" %(tid)
    cursor.execute(sql)
    topic = cursor.fetchone()[0]
    list = []
    others = []
    sql = "select qid,title,content,time,ideanum from questions where tid=%d" %(tid)
    cursor.execute(sql)
    for data in cursor.fetchall():
        list.append(Question(data[0],data[1],data[2],data[3],data[4]))
    sql = "select tid,name,quenum from topics order by quenum DESC"
    cursor.execute(sql)
    i = 0
    for data in cursor.fetchall():
        i+= 1
        if i==6:
            break
        others.append(Topic(data[0],data[1],data[2],1))
    return render(request,'page/question-list(1).html',{
        'uid': uid,
        'account': account,
        'nickname': nickname,
        'topic': topic,
        'tid': tid,
        'questions': list,
        'others': others
    })


def show_question(request,uid,qid):
    uid = int(uid)
    account = get_account(uid)
    nickname = get_nickname(uid)
    qid = int(qid)
    cursor = connection.cursor()
    sql = "select title,content,ideanum from questions where qid=%d" %(qid)
    cursor.execute(sql)
    data = cursor.fetchone()
    title = data[0]
    content = data[1]
    ideanum = data[2]
    list = []
    sql = "select iid,content,time,commentnum,good,bad,ideas.uid,users.nickname from ideas,users where ideas.uid=users.uid and qid=%d" %(qid)
    cursor.execute(sql)
    for data in cursor.fetchall():
        list.append(Idea(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))
    return render(request,'page/question(1).html',{
        'uid': uid,
        'account': account,
        'nickname': nickname,
        'qid': qid,
        'title': title,
        'content': content,
        'ideanum': ideanum,
        'ideas': list }
    )


def show_certain_idea(request,uid,qid,iid):
    pass


def show_comment(request,uid,qid,iid):
    uid = int(uid)
    account = get_account(uid)
    nickname = get_nickname(uid)
    qid = int(qid)
    iid = int(iid)
    cursor = connection.cursor()

    sql = "select title from questions where qid=%d" %(qid)
    cursor.execute(sql)
    title = cursor.fetchone()[0]
    sql = "select content,commentnum from ideas where iid=%d" %(iid)
    cursor.execute(sql)
    data = cursor.fetchone()
    content= data[0]
    commentnum = data[1]
    list = []
    sql = "select nickname,content,time,good,bad from users,comments where iid=%d and users.uid=comments.uid order by time DESC" %(iid)
    cursor.execute(sql)
    for data in cursor.fetchall():
        list.append(Comment(data[0],data[1],data[2],data[3],data[4]))
    return render(request,'page/comment(1).html',{
        'uid': uid,
        'account': account,
        'nickname': nickname,
        'qid': qid,
        'iid': iid,
        'title': title,
        'content': content,
        'commentnum': commentnum,
        'comments': list }
    )


def mine(request,uid):
    uid = int(uid)
    other = uid
    account = get_account(uid)
    nickname = get_nickname(uid)
    other_nickname = nickname
    cursor = connection.cursor()

    topics = []
    sql = "select topics.tid,name,quenum from topics,focus where topics.tid=focus.tid and focus.uid=%d" % (other)
    cursor.execute(sql)
    for data in cursor.fetchall():
        topics.append(Topic(data[0], data[1], data[2], 1))

    questions = []
    sql = "select qid,title,content,time,ideanum from questions where uid=%d" % (other)
    cursor.execute(sql)
    for data in cursor.fetchall():
        questions.append(Question(data[0], data[1], data[2], data[3], data[4]))

    ideas = []
    sql = "select iid,content,time,commentnum,good,bad,ideas.uid,users.nickname,qid from ideas,users where ideas.uid=users.uid and ideas.uid=%d" % (
    other)
    cursor.execute(sql)
    datas = []
    qids = []
    for data in cursor.fetchall():
        qids.append(data[8])
        a = []
        for i in range(0, 8):
            a.append(data[i])
        datas.append(a)

    for i in range(0, len(qids)):
        sql = "select questions.tid,topics.name,qid,title from questions,topics where topics.tid=questions.tid and qid=%d" % (
        qids[i])
        cursor.execute(sql)
        question = cursor.fetchone()
        ideas.append(Index(question[0], question[1], question[2], question[3], datas[i][0], datas[i][1], datas[i][2],
                           datas[i][3], datas[i][4], datas[i][5], datas[i][6], datas[i][7]))

    return render(request, 'page/personal(1).html', {
        'uid': uid,
        'account': account,
        'nickname': nickname,
        'other_account': account,
        'other_nickname': other_nickname,
        'topics': topics,
        'questions': questions,
        'ideas': ideas}
    )


def other(request,uid,other):
    uid = int(uid)
    other = int(other)

    if uid == other:
        return HttpResponseRedirect('/page/index/%d/mine/' %(uid))

    account = get_account(uid)
    nickname = get_nickname(uid)
    other_account = get_account(other)
    other_nickname = get_nickname(other)
    cursor = connection.cursor()

    topics = []
    sql = "select topics.tid,name,quenum from topics,focus where topics.tid=focus.tid and focus.uid=%d" %(other)
    cursor.execute(sql)
    for data in cursor.fetchall():
        topics.append(Topic(data[0],data[1],data[2],1))

    questions = []
    sql = "select qid,title,content,time,ideanum from questions where uid=%d" %(other)
    cursor.execute(sql)
    for data in cursor.fetchall():
        questions.append(Question(data[0],data[1],data[2],data[3],data[4]))

    ideas = []
    sql = "select iid,content,time,commentnum,good,bad,ideas.uid,users.nickname,qid from ideas,users where ideas.uid=users.uid and ideas.uid=%d" %(other)
    cursor.execute(sql)
    datas = []
    qids = []
    for data in cursor.fetchall():
        qids.append(data[8])
        a = []
        for i in range(0,8):
            a.append(data[i])
        datas.append(a)

    for i in range(0,len(qids)):
        sql = "select questions.tid,topics.name,qid,title from questions,topics where topics.tid=questions.tid and qid=%d" %(qids[i])
        cursor.execute(sql)
        question = cursor.fetchone()
        ideas.append(Index(question[0], question[1], question[2], question[3], datas[i][0],datas[i][1],datas[i][2],datas[i][3],datas[i][4],datas[i][5],datas[i][6],datas[i][7]))

    return render(request,'page/other(1).html',{
        'uid': uid,
        'account': account,
       'nickname': nickname,
        'other_account': other_account,
        'other_nickname': other_nickname,
        'topics': topics,
        'questions': questions,
        'ideas': ideas }
    )


def ask_question(request,uid):
    return render(request,'page/ask.html',{'uid': uid})


def create_question(request):
    uid = request.POST.get('uid')
    uid = int(uid)
    title = request.POST.get('title')
    topic = request.POST.get('topic')
    content = request.POST.get('content')
    cursor = connection.cursor()
    sql = "call zhihu.add_logs('add','questions','%s','%d')" %(title,uid)
    cursor.execute(sql)
    sql = "select tid from topics where name='%s'" %(topic)
    cursor.execute(sql)
    tid = cursor.fetchone()[0]
    sql = "insert into questions(title,content,uid,tid) values('%s','%s',%d,%d)" %(title,content,uid,tid)
    cursor.execute(sql)
    return HttpResponse(json.dumps({'response': '问题提交成功'}))


def create_idea(request):
    uid = request.POST.get('uid')
    qid = request.POST.get('qid')
    uid = int(uid)
    qid = int(qid)
    content = request.POST.get('content')
    cursor = connection.cursor()
    #sql = "select title from questions where qid=%d" %(qid)
    #cursor.execute(sql)
    #title = cursor.fetchone()[0]
    sql = "call add_logs('add','ideas','%s',%d)" %(content,uid)
    cursor.execute(sql)
    sql = "insert into ideas(uid,qid,content) values(%d,%d,'%s')" %(uid,qid,content)
    cursor.execute(sql)
    return HttpResponse(json.dumps({'response': '回答提交成功'}))


def create_comment(request):
    uid = request.POST.get('uid')
    iid = request.POST.get('iid')
    uid = int(uid)
    iid = int(iid)
    content = request.POST.get('content')
    cursor = connection.cursor()
    sql = "insert into logs(operation,what,content,uid) values('add','comments','%s',%d)" %(content,uid)
    cursor.execute(sql)
    sql = "insert into comments(uid,iid,content) values(%d,%d,'%s')" %(uid,iid,content)
    cursor.execute(sql)
    return HttpResponse(json.dumps({'response': '评论提交成功'}))


def add_good(request):
    iid = request.POST.get('id')
    iid = int(iid)
    cursor = connection.cursor()
    sql = "update ideas set good=good+1 where iid=%d" %(iid)
    cursor.execute(sql)
    sql = "select good from ideas where iid=%d" %(iid)
    cursor.execute(sql)
    good = cursor.fetchone()[0]
    good = str(good)
    return HttpResponse(json.dumps({'response': good}))


def cancel_good(request):
    iid = request.POST.get('id')
    iid = int(iid)
    cursor = connection.cursor()
    sql = "update ideas set good=good-1 where iid=%d" % (iid)
    cursor.execute(sql)
    sql = "select good from ideas where iid=%d" % (iid)
    cursor.execute(sql)
    good = cursor.fetchone()[0]
    return HttpResponse(json.dumps({'response': good}))


def add_bad(request):
    iid = request.POST.get('id')
    iid = int(iid)
    iid = math.fabs(iid)
    cursor = connection.cursor()
    sql = "update ideas set bad=bad+1 where iid=%d" %(iid)
    cursor.execute(sql)
    sql = "select bad from ideas where iid=%d" % (iid)
    cursor.execute(sql)
    bad = cursor.fetchone()[0]
    return HttpResponse(json.dumps({'response': bad}))


def cancel_bad(request):
    iid = request.POST.get('id')
    iid = int(iid)
    iid = math.fabs(iid)
    cursor = connection.cursor()
    sql = "update ideas set bad=bad-1 where iid=%d" % (iid)
    cursor.execute(sql)
    sql = "select bad from ideas where iid=%d" % (iid)
    cursor.execute(sql)
    bad = cursor.fetchone()[0]
    return HttpResponse(json.dumps({'response': bad}))


def add_focus(request):
    id = request.POST.get('id')
    a = []
    a = id.split("-")
    uid = int(a[0])
    tid = int(a[1])
    cursor = connection.cursor()
    sql = "insert into focus(uid,tid) values(%d,%d)" %(uid,tid)
    cursor.execute(sql)
    return HttpResponse(json.dumps({'response': 'add focus'}))


def cancel_focus(request):
    id = request.POST.get('id')
    a = []
    a = id.split("-")
    uid = int(a[0])
    tid = int(a[1])
    cursor = connection.cursor()
    sql = "delete from focus where uid=%d and tid=%d" %(uid,tid)
    cursor.execute(sql)
    return HttpResponse(json.dumps({'response': 'cancel focus'}))


def change_question(request,uid,qid):
    uid = int(uid)
    qid = int(qid)
    account = get_account(uid)
    nickname = get_nickname(uid)
    cursor = connection.cursor()
    sql = "select questions.title,topics.name,questions.content from questions,topics where questions.tid=topics.tid and questions.qid=%d" %(qid)
    cursor.execute(sql)
    data = cursor.fetchone()
    title = data[0]
    name = data[1]
    content = data[2]
    return render(request,'page/edit-question(1).html',{
        'uid': uid,
        'qid': qid,
        'account': account,
        'nickname': nickname,
        'title': title,
        'name': name,
        'content': content}
    )


def save_question(request,uid,qid):
    uid = int(uid)
    qid = int(qid)
    cursor = connection.cursor()
    title = request.POST.get('question-title')
    name = request.POST.get('add-topic')
    content = request.POST.get('question-description')

    sql = "call add_logs('update','questions','%s',%d)" %(title,uid)
    cursor.execute(sql)
    sql = "select tid from topics where name='%s'" %(name)
    cursor.execute(sql)
    data = cursor.fetchone()
    tid = int(data[0])

    a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    sql = "update questions set title='%s',content='%s',tid=%d,time='%s' where qid=%d" %(title,content,tid,a,qid)
    cursor.execute(sql)
    return HttpResponseRedirect('/page/index/%d/mine' %(uid))


def delete_question(request,uid,qid):
    uid = int(uid)
    qid = int(qid)
    cursor = connection.cursor()
    sql = "select title from questions where qid=%d" %(qid)
    cursor.execute(sql)
    title = cursor.fetchone()[0]
    sql = "call add_logs('delete','questions','%s',%d)" %(title,uid)
    cursor.execute(sql)
    sql = "call add_logs('delete','ideas','了%s问题下的所有回答',5)" %(title)
    cursor.execute(sql)
    sql = "delete from comments where iid in (select iid from ideas where qid=%d)" %(qid)
    cursor.execute(sql)
    sql = "delete from ideas where qid=%d" %(qid)
    cursor.execute(sql)
    sql = "delete from questions where qid=%d" % (qid)
    cursor.execute(sql)
    return HttpResponseRedirect('/page/index/%d/mine' %(uid))


def change_idea(request,uid,iid):
    uid = int(uid)
    iid = int(iid)
    account = get_account(uid)
    nickname = get_nickname(uid)
    cursor = connection.cursor()
    sql = "select questions.qid,title from questions,ideas where ideas.qid=questions.qid and ideas.iid=%d" %(iid)
    cursor.execute(sql)
    data = cursor.fetchone()
    qid = data[0]
    title = data[1]
    sql = "select content from ideas where iid=%d" %(iid)
    cursor.execute(sql)
    content = cursor.fetchone()[0]

    return render(request,'page/edit-idea(1).html',{
        'uid': uid,
        'iid': iid,
        'qid': qid,
        'title': title,
        'account': account,
        'nickname': nickname,
        'content': content,
    })


def save_idea(request,uid,iid):
    uid = int(uid)
    iid = int(iid)
    content = request.POST.get('idea-of')
    a = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cursor = connection.cursor()
    sql = "call add_logs('update','ideas','%s',%d)" %(content,uid)
    cursor.execute(sql)
    sql = "update ideas set content='%s',time='%s' where iid=%d" %(content,a,iid)
    cursor.execute(sql)
    return HttpResponseRedirect('/page/index/%d/mine/' %(uid))


def delete_idea(request,uid,iid):
    uid = int(uid)
    iid = int(iid)
    cursor = connection.cursor()
    sql = "select content from ideas where iid=%d" %(iid)
    cursor.execute(sql)
    content = cursor.fetchone()[0]
    sql = "call add_logs('delete','ideas','%s',%d)" %(content,uid)
    cursor.execute(sql)
    sql = "delete from comments where comments.iid=%d" %(iid)
    cursor.execute(sql)
    sql = "delete from ideas where ideas.iid=%d" %(iid)
    cursor.execute(sql)
    return HttpResponseRedirect('/page/index/%d/mine' %(uid))


def search(request,uid):
    uid = int(uid)
    account = get_account(uid)
    nickname = get_nickname(uid)
    word = request.POST.get("keyword")
    keyword = word.lower()
    cursor = connection.cursor()

    topics = []
    sql = "select tid,name,quenum from topics where lower(name) like '%" + keyword + "%'"
    cursor.execute(sql)
    for data in cursor.fetchall():
        topics.append(Topic(data[0],data[1],data[2],0))

    users = []
    sql = "select uid,nickname from users where lower(nickname) like '%" + keyword + "%'"
    cursor.execute(sql)
    a = []
    for data in cursor.fetchall():
        a.append([data[0],data[1]])
    for b in a:
        sql = "select count(*) from ideas where uid=%d" %(b[0])
        cursor.execute(sql)
        answer = cursor.fetchone()[0]
        sql = "select count(*) from questions where uid=%d" % (b[0])
        cursor.execute(sql)
        ask = cursor.fetchone()[0]
        sql = "select count(*) from focus where uid=%d" % (b[0])
        cursor.execute(sql)
        focus = cursor.fetchone()[0]
        users.append(People(b[0],b[1],answer,ask,focus))

    questions = []
    sql = "select qid,title,content,time,ideanum from questions where lower(title) like '%" + keyword + "%'"
    cursor.execute(sql)
    for data in cursor.fetchall():
        questions.append(Question(data[0], data[1], data[2], data[3], data[4]))

    return render(request,'page/search(1).html',{
        'uid': uid,
        'account': account,
        'nickname': nickname,
        'keyword': keyword,
        'topics': topics,
        'users': users,
        'questions': questions}
    )


class Log:
    def __init__(self,operation,time,content,nickname):
        self.operation = operation
        self.time = time
        self.content = content
        self.nickname = nickname


def manage(request):
    questions = []
    ideas = []
    comments = []
    users = []
    topics = []

    cursor = connection.cursor()
    sql = "select logs.operation,logs.time,logs.content,users.nickname from logs,users where what='questions' and logs.uid=users.uid order by logs.time DESC"
    cursor.execute(sql)
    i = 0
    for data in cursor.fetchall():
        i += 1
        if i==6:
            break
        if data[0]=='add':
            operation = '提出'
        elif data[0]=='update':
            operation = '修改'
        else:
            operation = '删除'
        questions.append(Log(operation,data[1],data[2],data[3]))

    sql = "select logs.operation,logs.time,logs.content,users.nickname from logs,users where what='ideas' and logs.uid=users.uid order by logs.time DESC"
    cursor.execute(sql)
    i = 0
    for data in cursor.fetchall():
        i += 1
        if i == 6:
            break
        if data[0] == 'add':
            operation = '做出'
        elif data[0] == 'update':
            operation = '修改'
        else:
            operation = '删除'
        ideas.append(Log(operation, data[1], data[2], data[3]))

    sql = "select logs.operation,logs.time,logs.content,users.nickname from logs,users where what='comments' and logs.uid=users.uid order by logs.time DESC"
    cursor.execute(sql)
    i = 0
    for data in cursor.fetchall():
        i += 1
        if i == 6:
            break
        if data[0] == 'add':
            operation = '做出'
        elif data[0] == 'update':
            operation = '修改'
        else:
            operation = '删除'
        comments.append(Log(operation, data[1], data[2], data[3]))

    sql = "select tid,name,quenum from topics"
    cursor.execute(sql)
    for data in cursor.fetchall():
        topics.append(Topic(data[0],data[1],data[2],0))

    sql = "select account,nickname from users"
    cursor.execute(sql)
    for data in cursor.fetchall():
        users.append(User(9,data[0],'0',data[1]))

    return render(request,'page/manager(1).html',{
        'questions': questions,
        'ideas': ideas,
        'comments': comments,
        'topics': topics,
        'users': users,
    })


def delete_topic(request,tid):
    tid = int(tid)
    cursor = connection.cursor()
    sql = "delete from questions where tid=%d" %(tid)
    cursor.execute(sql)
    sql = "delete from topics where tid=%d" %(tid)
    cursor.execute(sql)
    return HttpResponseRedirect('/page/index/manage/')


def add_topic(request):
    name = request.POST.get('topic')
    cursor = connection.cursor()
    sql = "select max(tid) from topics"
    cursor.execute(sql)
    num = cursor.fetchone()[0]
    sql = "call add_topics('%s',%d)" %(name,num+1)
    cursor.execute(sql)
    return HttpResponse(json.dumps({'message': '添加话题成功'}))


