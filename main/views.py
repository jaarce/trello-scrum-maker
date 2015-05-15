from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from main.models import *
import requests
import json

def home(request):
    # article = get_object_or_404(Article, slug=slug)
    # context = {'article': article}
    
    return render(request, 'base.html', {})


@csrf_exempt
def name(request):
    account = get_object_or_404(Accounts, name=request.POST.get('name'))
    token = request.POST.get('token')

    query = 'https://api.trello.com/1/members/' + account.name + '?key=e42346614529e890c100cd4ab4235bac&token=' + token
    req = requests.get(query)
    user_id = json.loads(req.content)['id']

    query = 'https://api.trello.com/1/boards/%s?lists=open&key=e42346614529e890c100cd4ab4235bac&token=%s' % (account.taken_from_id, token)
    req = requests.get(query)
    lists = json.loads(req.content)['lists']
    for item in lists:
        # progress
        if 'progress' in item['name'].lower():
            account.today_id = item['id']
            account.save()
        if 'completed' in item['name'].lower():
            account.yesterday_id = item['id']
            account.save()

    # completed already.
    my_yesterday = []
    query = 'https://api.trello.com/1/lists/%s/cards?key=e42346614529e890c100cd4ab4235bac&token=%s' % (account.yesterday_id, token)
    req = requests.get(query)
    lists = json.loads(req.content)
    counter = 0

    for item in lists:
        if counter > 0:
            my_yesterday.append(item['name'])
        counter += 1


    # in progress.
    my_progress = []
    query = 'https://api.trello.com/1/lists/%s/cards?key=e42346614529e890c100cd4ab4235bac&token=%s' % (account.today_id, token)
    req = requests.get(query)
    lists = json.loads(req.content)
    counter = 0

    for item in lists:
        if counter > 0:
            my_progress.append(item['name'])
        counter += 1


    json_data = {
        'today': my_progress,
        'yesterday': my_yesterday,
    }

    today_board = []
    query = 'https://api.trello.com/1/lists/%s/cards?key=e42346614529e890c100cd4ab4235bac&token=%s' % (account.store_to_id, token)
    req = requests.get(query)
    lists = json.loads(req.content)
    for item in lists:
        if item['subscribed']:
            requests.delete('https://api.trello.com/1/cards/%s?key=e42346614529e890c100cd4ab4235bac&token=%s' % (item['id'], token))

    for progress in my_progress:
        payload = {'name': progress, 'desc': '', 'due': 'null', 'idMembers': user_id}
        requests.post(query, payload)

    
    return HttpResponse(json.dumps(json_data), mimetype="application/json")