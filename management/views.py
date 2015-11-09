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
from forms import GroupForm
from users.models import Title, Group

def userManagementViews(request):
    """
    JunHU
    """
    context = {}
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
    form = GroupForm()
    context = {
            "form": form,
        }
    return render(request, "management/title_management.html", context)

def messageManagementViews(request):
    """
    JunHU
    """
    if request.method == 'POST':
        messageform = MessageForm(request.POST)
        if messageform.is_valid():
            new_message = Message(title = messageform.cleaned_data["message_title"],
                                  content = messageform.cleaned_data["message_content"],
                                  writer = request.user,
                                  time = datetime.datetime.now()
                                 )
            new_message.save()
            for user_iterator in User.objects.all():
                for group_id in messageform.cleaned_data["message_groups"]:
                    group = Group.objects.get(id = int(group_id))
                    if (user_iterator.title_set.filter(group = group).count() > 0):
                        new_box = MessageBox(user = user_iterator,
                                             message = new_message,
                                             read = False)
                        new_box.save()
    else:
        messageform = MessageForm()
        context = {
            "messageform": messageform
        }
        return render(request, "management/message_management.html", context)

def authorityManagementViews(request):
    """
    JunHU
    """
    title_id = request.GET.get("title_id")
    title = Title.objects.get(id = title_id)
    context = {
            "title": title,
        }
    return render(request, "management/authority_management.html", context)


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
        return redirect("/news/newslist/%s" % new_news.id)
    else:
        newsform = NewsForm()
        context = {
            'newsform' : newsform
        }
        return render(request, "management/news_release.html", context)
