from django.shortcuts import render
import json
from django.shortcuts import redirect
import json
import os
from robot_communication.models import Sys_user, Communication,Communication_2
from django.contrib.auth.models import User
from django.contrib import auth
# import tensorflow as tf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect,HttpResponseRedirect
from django.http import JsonResponse,HttpResponse
import copy
import datetime
import collections
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# Create your views here.
import csv
import re

from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import ALS,Rating
from pyspark.mllib.recommendation import MatrixFactorizationModel

def get_csv_list(file_path):
    with open(file_path, "r", encoding='utf-8') as csvreader:
        reader = csv.reader(csvreader)
        rowlist = [row for row in reader]
        return rowlist

def csv_map_key(file_path,reverse=False):
    row_list=get_csv_list(file_path)
    result_dict={}
    for row in row_list[1:]:
        if reverse==False:
            result_dict[row[0]]=row[1]
        else:
            result_dict[row[1]] = row[0]
    return result_dict


spark_context = SparkContext("local", "Test")
model = MatrixFactorizationModel.load(spark_context, os.path.join(rootPath, 'data', 'als-model'))
spark_context.stop()

movie_dict = csv_map_key(os.path.join(rootPath, 'data', 'movies.csv'))

def index(request):
    if request.method=='GET':
        return render(request,'login.html', {'wrong': 0})


def loginf(request):
    if request.method == "POST":
        loginname = request.POST['username']
        loginpassword = request.POST['pwd']
        user = auth.authenticate(username=loginname, password=loginpassword)
        # print(loginname)
        # print(loginpassword)
        if user is not None:
            login(request, user)
            sys_user = Sys_user.objects.get(user=user)
            communication_list = Communication.objects.order_by("date")
            for communnication in communication_list:
                #print(communnication.com_content)
                communnication.com_content=communnication.com_content.replace("<br>",";  ")
                #print(communnication.com_content)
            communication_list_2 = Communication_2.objects.order_by("date")
            for communnication_2 in communication_list_2:
                #print(communnication.com_content)
                communnication_2.com_content=communnication_2.com_content.replace("<br>",";  ")
            # for i in communication_list:
            #     print(i.com_content)
            return render(request, 'index.html',{'user': user, 'sys_user': sys_user, 'communication_list': communication_list,'communication_list_2': communication_list_2})
        else:
            return render(request, 'login.html', {'wrong': 1})

def regist(request):
    if request.method=='GET':
        return render(request, 'regist.html')
    if request.method=='POST':
        registnum = request.POST['username']
        todouser = User.objects.filter(username=registnum)
        if todouser.exists():
            logininfo = "same_error"
            return render(request, 'regist.html', {'logininfo': logininfo})
        else:
            registpassword = request.POST['pwd']
            nicheng = request.POST['nicheng']
            registemail = request.POST['email']
            # print(sex)
            # print(profession)
            if User.objects.filter(email=registemail):
                logininfo = "repeate"
                return render(request, 'regist.html', {'logininfo': logininfo})

            else:
                try:
                    validate_email(registemail)
                    todo = User.objects.create_user(registnum, registemail, registpassword)
                    todo.save()
                    todom = Sys_user(user=todo, name=nicheng,email=registemail)
                    todom.save()
                    loginflag = 'regist_sucsess'
                    return render(request, 'login.html', {'loginflag': loginflag , 'loginnum':registnum })
                except ValidationError:
                    logininfo = 'wrong'
                    return render(request, 'regist.html', {'logininfo': logininfo})



def robot_response(request):
    dt = datetime.datetime.now()
    #print(dt)
    if request.method=='GET':
        # print("get了")
        my_text=request.GET.get("my_text")    #此处为算法输入
        print(my_text)
        new_content_my = Communication(com_type="human",com_content=my_text)
        new_content_my.save()

        # candidate_list=['感冒','发烧','腮腺炎']
        # import random
        # robot_responses=random.choice(candidate_list)

        number_list=re.findall(r"\d+",my_text)
        #print(number_list)

        if len(number_list)!=2:
            robot_responses="请您输入正常的格式！"
        elif len(number_list)==2:
            userId=int(number_list[0])
            movie_num=int(number_list[1])
            if userId<1 or userId>610:
                robot_responses="用户ID不存在！"
            else:
                robot_responses=""
                spark_context = SparkContext("local", "Test")
                model = MatrixFactorizationModel.load(spark_context, os.path.join(rootPath, 'data', 'als-model'))
                rate_list=model.recommendProducts(userId, movie_num)
                for index in range(len(rate_list)):
                    item=rate_list[index]
                    movie_name_Id=str(item.product)
                    movie_name=movie_dict[movie_name_Id]
                    robot_responses+="为用户"+str(userId)+"推荐第"+str(index+1)+"部电影：《"+movie_name+"》，评分为"+str(item.rating)
                    if index != len(rate_list):
                        robot_responses+="<br>"
                spark_context.stop()

        new_content_robot = Communication(com_type="robot", com_content=robot_responses)
        new_content_robot.save()
        # from django.core import serializers
        # new_content_robot = serializers.serialize("json", new_content_robot)
        # new_content_robot=json.dumps(new_content_robot)
        # print(new_content_robot.date)
        content_time=str(new_content_robot.date).split('.')[0].replace('\t',' ')
        ret={
            'time':content_time,
            'content':new_content_robot.com_content
        }
        return JsonResponse(ret,safe=False)

def logoutf(request):
    logout(request)
    return render(request, 'login.html')

def delete_all(request):
    global first_diag, diag_len, need_check, iteration
    if request.method=='GET':
        user=request.user
        Communication.objects.all().delete()
        sys_user = Sys_user.objects.get(user=user)
        communication_list = Communication.objects.order_by("date")
        communication_list_2 = Communication_2.objects.order_by("date")
        # for i in communication_list:
        #     print(i.com_content)
        new_welcome_robot = Communication(com_type="robot", com_content="您好！请输入为哪个用户推荐几部电影")
        new_welcome_robot.save()
        first_diag=""
        diag_len=0
        need_check = ""
        iteration = 0

        content_time = str(new_welcome_robot.date).split('.')[0].replace('\t', ' ')
        #return render(request, 'index.html', {'user': user, 'sys_user': sys_user, 'communication_list': communication_list,'communication_list_2': communication_list_2})
        ret={
            'time': content_time,
            'content': "您好！请输入为哪个用户推荐几部电影"
        }
        return JsonResponse(ret,safe=False)
        #注意传给index的变成了四个参数

# def ajax_demo1(request):
#     return render(request, "ajax_demo1.html")
#
#
# def ajax_add(request):
#     i1 = int(request.GET.get("i1"))
#     i2 = int(request.GET.get("i2"))
#     ret = i1 + i2
#     return JsonResponse(ret, safe=False)

def delete_all_2(request):
    if request.method=='GET':
        user=request.user
        Communication_2.objects.all().delete()
        sys_user = Sys_user.objects.get(user=user)
        communication_list = Communication.objects.order_by("date")
        communication_list_2 = Communication_2.objects.order_by("date")
        # for i in communication_list:
        #     print(i.com_content)
        new_welcome_robot = Communication_2(com_type="robot", com_content="您好！请输入将哪个电影推荐给几个用户")
        new_welcome_robot.save()
        content_time = str(new_welcome_robot.date).split('.')[0].replace('\t', ' ')
        #return render(request, 'index.html', {'user': user, 'sys_user': sys_user, 'communication_list': communication_list,'communication_list_2': communication_list_2})
        ret={
            'time': content_time,
            'content': "您好！请输入将哪个电影推荐给几个用户"
        }
        return JsonResponse(ret,safe=False)

def robot_response_2(request):
    dt = datetime.datetime.now()
    print(dt)

    if request.method=='GET':
        # print("get了")
        my_text=request.GET.get("my_text")    #此处为算法输入
        print(my_text)
        new_content_my = Communication_2(com_type="human",com_content=my_text)
        new_content_my.save()

        # candidate_list=['感冒','发烧','腮腺炎']
        # import random
        # robot_responses=random.choice(candidate_list)

        number_list=re.findall(r"\d+",my_text)
        #print(number_list)

        if len(number_list)!=2:
            robot_responses="请您输入正常的格式！"
        elif len(number_list)==2:
            movieId=int(number_list[0])
            user_num=int(number_list[1])
            if str(movieId) not in list(movie_dict.keys()):
                robot_responses="电影ID不存在！"
            else:
                robot_responses=""
                spark_context = SparkContext("local", "Test")
                model = MatrixFactorizationModel.load(spark_context, os.path.join(rootPath, 'data', 'als-model'))
                rate_list=model.recommendUsers(movieId, user_num)
                for index in range(len(rate_list)):
                    item=rate_list[index]
                    movie_name_Id=str(item.product)
                    movie_name=movie_dict[movie_name_Id]
                    robot_responses+="为用户"+str(item.user)+"推荐电影：《"+movie_name+"》，评分为"+str(item.rating)
                    if index != len(rate_list):
                        robot_responses+="<br>"
                spark_context.stop()
        #print("第二个场景：",robot_response)
        new_content_robot = Communication_2(com_type="robot", com_content=robot_responses)
        new_content_robot.save()
        # from django.core import serializers
        # new_content_robot = serializers.serialize("json", new_content_robot)
        # new_content_robot=json.dumps(new_content_robot)
        # print(new_content_robot.date)
        content_time=str(new_content_robot.date).split('.')[0].replace('\t',' ')
        ret={
            'time':content_time,
            'content':new_content_robot.com_content
        }
        return JsonResponse(ret,safe=False)
