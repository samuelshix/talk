from django.http import response
from django.shortcuts import render
from django.db import connection
from landing import unified_return_format as re
import json
import datetime
# Create your views here.

#localhost:8000/friend_request
#Body: account1, account2
def friend_request(request):
    post = request.POST
    account1 = post['account1'] 
    account2 = post['account2']

    sql_insert = 'insert into friend_relation(account1, account2, request, is_friend) value(' + '\''+ account1 + '\', \''+account2+'\', \''+str(1)+'\',  \''+str(0)+'\')'
    print(sql_insert)
    
    mycursor = connection.cursor()
    try:      
        mycursor.execute(sql_insert)
    except:
        uni = re.format_return_value(500, 'friend_request', 'no such user in database')
        return render(request, "landing\\index.html", {'Msg': uni})
    uni = re.format_return_value(200, 'friend_request', 'successful') 
    return render(request, "landing\\index.html", {'Msg': uni})

#localhost:8000/accept_request
#Body: account1, account2, is_accept
def accept_request(request):
    post = request.POST
    account1 = post['account1'] 
    account2 = post['account2']
    sql_select = "select 1 from user_info where account = \'" +post['account1']+"\' and (select exists(select 1 from user_info where account = \'" +post['account2']+"\'))"
    print(sql_select)
    mycursor1 = connection.cursor()
    mycursor1.execute(sql_select)
    row = mycursor1.fetchone()
    if row is not None and row[0] == 1:
        is_accept = post['is_accept']
        print(is_accept)
        if is_accept == 'False':
            sql_update = "update friend_relation set request = \'"+str(0)+"\' where account1 = \'" +post['account1']+"\' and account2 = \'" +post['account2']+"\'"
        else:
            sql_update = "update friend_relation set is_friend = \'"+str(1)+"\', request = \'"+str(0)+"\' where account1 = \'" +post['account1']+"\' and account2 = \'" +post['account2']+"\'"
        print(sql_update)
        mycursor = connection.cursor()
        try:      
            mycursor.execute(sql_update)
        except:
            uni = re.format_return_value(500, 'accept_request', 'acceptance unsuccessful')
            return render(request, "landing\\index.html", {'Msg': uni})
        uni = re.format_return_value(200, 'accept_request', 'successful') 
        return render(request, "landing\\index.html", {'Msg': uni})
    else:
        uni = re.format_return_value(500, 'accept_request', 'acceptance unsuccessful')
        return render(request, "landing\\index.html", {'Msg': uni})

#localhost:8000/if_friend
#Body: account1, account2
def if_friend(request):

    post = request.POST
    _account1 = post['account1'] 
    _account2 = post['account2']
    sql_select = "select * from friend_relation where account1 = \'"+ _account1+"\' and account2 = \'" +_account2+ "\'"
    mycursor1 = connection.cursor()
    try:
        mycursor1.execute(sql_select)
        res = mycursor1.fetchone()
    except:
        uni = re.format_return_value(500, 'if_friend', 'no relationship found')
        return render(request, "landing\\index.html", {'Msg': uni})
    if res is not None:
        uni = re.format_return_value(200, 'if_friend', res[0])
        print(uni)
        return response.HttpResponse(True)
    else:
        uni = re.format_return_value(200, 'if_friend', 'no relationship found')
    print(res[0: ])
    return render(request, "landing\\index.html", {'Msg': uni})
    

#localhost:8000/get_profile?account=01
def get_profile(request):
    if request.method == 'GET':
        account = request.GET.get('account')
    sql_select = "select * from user_profile where account = \'"+ account+"\'"
    mycursor1 = connection.cursor()
    mycursor1.execute(sql_select)
    row = mycursor1.fetchone()
    if row is not None:
        user_profile = json.dumps({'account': row[1], 'name': row[2], 'description': row[3], 'photo': row[4]})
        uni = re.format_return_value(200, 'get_profile', user_profile)
        #return render(request, "landing\\index.html", {'Msg': uni})
        return response.JsonResponse({'account': row[1], 'name': row[2], 'description': row[3], 'photo': row[4]})
    else:
        uni = re.format_return_value(500, 'get_profile', 'get profile unsuccessfully')
        return render(request, "landing\\index.html", {'Msg': uni})

#localhost:8000/edit_profile
#Body: account, name, description, photo
def edit_profile(request):

    post = request.POST
    sql_select = "select 1 from user_profile where account = \'" +post['account']+"\'"
    print(sql_select)
    mycursor1 = connection.cursor()
    mycursor1.execute(sql_select)
    row = mycursor1.fetchone()
    if row is not None and row[0] == 1:
        sql_update = "update user_profile set name =  \'" +post['name']+"\' , description = \'" +post['description']+"\',photo = \'" +post['photo']+"\'   where account = \'" +post['account']+"\'"
        mycursor = connection.cursor()
        try:      
            mycursor.execute(sql_update)
        except:
            uni = re.format_return_value(500, 'edit_profile', 'edition unsuccessful')
            return render(request, "landing\\index.html", {'Msg': uni})
        uni = re.format_return_value(200, 'edit_profile', 'successful') 
        return render(request, "landing\\index.html", {'Msg': uni})
    else:
        uni = re.format_return_value(500, 'edit_profile', 'profile edition unsuccessful')
        return render(request, "landing\\index.html", {'Msg': uni})

def add_post(request):
    post = request.POST
    
    create_at = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    username = post.get('username','')
    text = post.get('text','')#must have post content
    photo = post.get('photo', '')

    if username and text:
        sql_insert = 'insert into post_list(username, text, photo, create_at) value(' + '\''+ username + '\', \''+text+'\', \''+photo+'\', \''+create_at+'\')'
    else: 
        uni = re.format_return_value(500, 'add_post', 'user post info required')

    uni = re.format_return_value(200, 'add_post', 'successful')    
    mycursor = connection.cursor()
    mycursor.execute(sql_insert)
    return response.HttpResponse(True)


def show_post(request):
    if request.method == 'GET':
        username = request.GET.get('username')
    sql_select = "select * from post_list where username = \'"+ username+"\'"
    mycursor1 = connection.cursor()
    mycursor1.execute(sql_select)
    rows = mycursor1.fetchall()
    dict_total = []
    for row in rows:
        if row is not None:
            dict = {}
            dict.update({'username': row[1]})
            dict.update({'text': row[2]})
            dict.update({'photo': row[3]})
            dict.update({'create_at': row[4]})
            dict_total.append(dict)
    return response.HttpResponse(dict_total)
        
