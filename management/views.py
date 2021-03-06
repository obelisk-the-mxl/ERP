#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-07-26 11:41
# Last modified: 2016-09-11 12:38
# Filename: views.py
# Description:
# coding: UTF-8
from django.shortcuts import render, redirect
from const.forms import InventoryTypeForm
from django.template import RequestContext
from django.views.decorators import csrf
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
import json
from django.db import transaction
from django.contrib.auth.models import User

from news.forms import NewsForm, MessageForm
from news.models import News, DocumentFile, NewsCategory, Message, MessageBox
import datetime
from forms import GroupForm, NewsCateForm
#from users.models import Title, Group
from const import NEWS_CATEGORY_COMPANYNEWS

from backend.utility import getContext
#from const.forms import AuthorTypeForm
from users.models import *

def titleSettingViews(request):
    """
    JunHU
    """
    user_id = request.GET.get("user_id")
    user = User.objects.get(id = user_id)
    group_form = GroupForm(request = request)
    context = {
        "setting_user": user,
        "group_form": group_form,
    }
    return render(request, "management/title_setting.html", context)


def userManagementViews(request):
    """
    JunHU
    """
    form = GroupForm()
    context = {
            "form": form,
    }
    return render(request, "management/user_management.html", context)


def groupManagementViews(request):
    """
    JunHU
    """
    context = {}
    return render(request, "management/group_management.html", context)


def titleManagementViews(request):
    """
    JunHU
    """
    form = GroupForm(request = request)
    context = {
            "form": form,
        }
    return render(request, "management/title_management.html", context)


def messageManagementViews(request):
    """
    BinWu
    """
    if request.method == 'POST':
        files = request.FILES.getlist("message_document")
        print("++++++++++++++++++++++++")
        print(files)
        messageform = MessageForm(request.POST)
        if messageform.is_valid():
            new_message = Message(title = messageform.cleaned_data["message_title"],
                                  content = messageform.cleaned_data["message_content"],
                                  writer = request.user,
                                  time = datetime.datetime.now()
                                 )
            new_message.save()
            if files:
                for file in files:
                    new_doc = DocumentFile(news_document = file,
                                           message = new_message)
                    new_doc.save()
            
            
            for user_iterator in User.objects.all():
               
                for group_id in messageform.cleaned_data["message_groups"]:
                    #queryset =  Title.objects.filter(users=user_iterator,group=group_id)
                    queryset = None
                    if (queryset.count() > 0):
                        new_box = MessageBox(user = user_iterator,
                                             message = new_message,
                                             read = False)
                        new_box.save()
    messageform = MessageForm(request=request)
    #message_list = Message.objects.filter(writer = request.user)
    print(request.user)
    context = {
        "messageform": messageform,
        #"message_list": message_list,
        "loguser":request.user
    }
    return render(request, "management/message_management.html", context)


def controlManagementViews(request):
    """
    JunHU
    """
    role_id = request.GET.get("role_id")
    #title = Title.objects.get(id = title_id)
    role = Role.objects.get(id=role_id)
#    auth_type_form = AuthorTypeForm()
    context = {
            "role": role,
#            "auth_type_form": auth_type_form,
        }
    return render(request, "management/control_management.html", context)


def newsReleaseViews(request):
    """
    mxl
    """
    if request.method == 'POST':
        files = request.FILES.getlist("news_document")
        newsform = NewsForm(request.POST)
        if newsform.is_valid():
            new_news = News(news_title = newsform.cleaned_data["news_title"],
                             news_content = newsform.cleaned_data["news_content"],
                             news_date = newsform.cleaned_data["news_date"],
                             news_category = NewsCategory.objects.get(id = newsform.cleaned_data["news_category"])
                            )
            new_news.save()
        if files:
            for f in files:
                doc = DocumentFile(news_document = f,
                                    news = new_news)
                doc.save()
        # return redirect("/news/newslist/%s" % new_news.id)
        return redirect("/management/newsManagement")
    else:
        newsform = NewsForm()
        context = {
            'newsform' : newsform
        }
        return render(request, "management/news_release.html", context)


def newsManagementViews(request):
    """
    mxl
    """
    form = NewsCateForm()
    # news_cate = NEWS_CATEGORY_COMPANYNEWS
    # news_list = News.objects.filter(news_category__category = news_cate).order_by('-news_date')
    # context = getContext(news_list, 1, 'news')
    # context["form"] = form
    context = {
        'form' : form
    }
    return render(request, "management/news_management.html", context)


def authorityManagementViews(request):
    context = {}
    return render(request, "management/authority_management.html", context)
