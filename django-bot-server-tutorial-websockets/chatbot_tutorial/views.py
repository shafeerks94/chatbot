from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render
from chatbot_tutorial.models import ChatbotModel

def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)
def chatlist(request):
    context = {}
    ins_chatmodel = list(ChatbotModel.objects.values())
    # import pdb; pdb.set_trace()
    lst_table_data = {}
    for row in ins_chatmodel:
        if not row['vchr_user_name'] in lst_table_data.keys():
            lst_table_data [row['vchr_user_name']] = { 'FAT':0 , 'DUMB':0,'STUPID':0}
            lst_table_data [row['vchr_user_name']][ row['vchr_jock_type']]= 1
        else:
            lst_table_data[row['vchr_user_name']][row['vchr_jock_type']] += 1
    return render(request, 'chatbot_tutorial/chatlist.html', {'lst_table_data':lst_table_data})
# 
def respond_to_websockets(message):
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
     }

    result_message = {
        'type': 'text'
    }
    # import pdb; pdb.set_trace()
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])

    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])

    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
        return result_message
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."
        return result_message

    ins_chatmodel = ChatbotModel(
        vchr_user_name = message.get('user','anonymous').upper(),
        vchr_jock_type = message['text'].upper()
    )
    ins_chatmodel.save()
    return result_message
