# -*- coding: utf-8 -*-
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from threading import Thread
import re
import datetime
#from datetime import datetime, date
from tables_part import GoogleSheet
import random

'''
vk_session = VkApi(token = "dfad8d11d321d20a634d2290b6c117eb02c43e50a8449d25c993d95dd12c36491b2f7bda1183bdf91924f")
longpoll = VkBotLongPoll(vk_session, 188445979)
vk = vk_session.get_api()
'''

def ms_send(user_id, text, attach = None):
        vk.messages.send(
                chat_id=user_id,
                message=text,
                #reply_to = ms_id,
                attachment = attach,
                random_id=get_random_id()
                )

#запасная
def mss_send(id, text, attach = None):
    vk_session.method(
        "messages.send",
        {
            "chat_id": id,
            "message": text,
            "random_id": get_random_id(),
            "attachment": attach
        }
    )



def get_name(us_id):
        user = vk.users.get(user_id=us_id)
        return user[0]['first_name'] + ' ' + user[0]['last_name']

def dozor_check(event, text):

    time = [int(s) for s in re.findall(r'\b\d+\b', text)]
    now_time = []
    current_date = datetime.datetime.now()
    now_time.append(current_date.hour)
    now_time.append(current_date.minute)
    #now_time[0] +=3
    print(now_time, time)
    if(time[0]-now_time[0] == 0 and abs(time[1]-now_time[1]) < 5):
        gs = GoogleSheet()
        ms_send(event.chat_id, f"Дозор засчитан, {gs.findInd(event.object.message['from_id'])}")
        return True
    else:
        ms_send(event.chat_id, "поздно или рано")
        return False

def res_counter(text):
    res = [int(s) for s in re.findall(r'\b\d+\b', text)]
    count = sum(res)
    if res == 0:
        return 0
    else:
        return count

def name_found(text):
    text = text.split(':', 1)[1]
    #print(text)
    #print(text.replace('участники', ''))
    text = text.replace('участники', '')
    voda = text.partition(':')[0]
    #voda.replace(' ', '')
    voda = voda.rstrip()
    #print(f"{voda} вода")      
    text = text.replace(voda, '')
    text = text.replace(':', '')
    text = text.split('\n', 1)[1]
    uchi = text.split(',')
    for i in range(len(uchi)):
        uchi[i] = uchi[i].replace(' ', '', 1)    
    #print(f"{uchi} участники")
    return voda, len(uchi), uchi
def reid(text):
    text = text.replace("рейд к лисобойной", "")
    text = text.replace("ведущий: ", "")
    text = text.replace("следящий: ", "")
    text = text.replace("замыкающий: ", "")
    uchi = text.split('.')
    uchi = uchi[:-1]
    for i in range(len(uchi)):
        uchi[i] = uchi[i].replace(' \n', '', 1) 
    #print(uchi)
    return len(uchi), uchi
def nabludali(text):
    text = text.replace("наблюдение за звездами:", "")
    uchi = text.split(', ')
    #print(uchi)
    return len(uchi), uchi

def unesla(event, text):
    gs = GoogleSheet()
    current_date = datetime.datetime.now()
    now_time = f"{current_date.day}.{current_date.month}.{current_date.year}"
    print(text)
    if 'с дерева' in text:
        #res = res_counter(text)
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "2", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано1, {name}\nБаллов: 2")
    elif '(от ущелья до уступов)' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "3", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано2, {name}\nБаллов: 3")

    elif '(с ' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "6", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано с ущелья\уступов в лагерь, {name}\nБаллов: 6")
    elif '(из лагеря на' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "6", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано (из лагеря на ущелье/уступы), {name}\nБаллов: 6")
    elif '(спец.выход)' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "8", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано (спец.выход), {name}\nБаллов: 8")
    elif '(лагерь - ущелье)' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано (лагерь - ущелье), {name}\nБаллов: 10")
    elif '(уступы - лагерь)' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано (уступы - лагерь), {name}\nБаллов: 10")
    elif '(лагерь - скалы - лагерь)' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано (лагерь - скалы - лагерь), {name}\nБаллов: 10")
    elif '(лагерь - ущелье - уступы - лагерь)' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "12", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано (лагерь - ущелье - уступы - лагерь), {name}\nБаллов: 12")

    '''
    elif '(с ' in text:
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "6", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Что-то засчитано, {name}\nБаллов: 6")
    '''


def check_pattern(event, text):
    gs = GoogleSheet()
    current_date = datetime.datetime.now()
    now_time = f"{current_date.day}.{current_date.month}.{current_date.year}"
    name = 'Пожалуйста сообщите разработчику что функция отработала некорректно'
    #name = gs.findInd(event.object.message['from_id'])
    #'''
    #for i in range(len(text)):
        #text[i] = text[i].replace("ё", "е")
    text = re.sub('[Ёё]', 'е', text)
    #print(text)
    if text == 'отмена':
        if 'reply_message' in list(event.object.message):
        #ms_send(chat_id, str(event.object.message['reply_message']['text']))
        #ms_send(chat_id, "отменено")
        #print(event)
        #print(event.object.message['reply_message']['conversation_message_id'])
            #gs = GoogleSheet()
            gs.delFromStat(event.object.message['reply_message']['conversation_message_id'])
            ms_send(event.chat_id, "отменено")
        else:
            ms_send(event.chat_id, "пожалуйста ответьте на сообщение, которое хотите отменить")

    if 'памагите' == text:
        #print("ass")
        #gs = GoogleSheet()
        #gs.delFromStat(661)
        #gs.insertRowN()
        ms_send(event.chat_id, "жить жить")
    if 'помя мям' == text:
        mass = [81181, 62821, 4238, 81193, 81203, 72135, 73058, 72599, 72617, 72627, 72626, 72635, 62802, 62815, 65094, 65100, 50617, 50611, 4246, 4256, 77709, 83371, 83359, 83365, 83386, 83390, 83402]
        vk.messages.send(
                chat_id=event.chat_id,
                sticker_id= random.choice(mass),
                #reply_to = ms_id,
                #attachment = attach,
                random_id=get_random_id()
                )
        #vk.messages.send(peer_id=event.chat_id, sticker_id= 8102, random_id=get_random_id())
    #'''
    if 'дай мне имя' in text:
        #print(text)
        text = text.replace("дай мне имя ", "")
        print(text) 
        
        #gs = GoogleSheet()
        name = text[0].upper() + text[1:]
        count = gs.coopAdd(f"{event.object.message['from_id']}", name, "Главная.")
        count = gs.coopAdd(f"{event.object.message['from_id']}", name, "За период")
        #count = gs.addToBd(f"{event.object.message['from_id']}", name)
        if count == 1:
            ms_send(event.chat_id, f"Ваше имя изменено на {name}")
        else:
            ms_send(event.chat_id, f"Вы были добавлены в таблицу, {name}")

    if 'дай имя' in text:
        print(text)
        ms_send(event.chat_id, text)
    if 'дозор (предпустынье)' in text:
        #print(dozor_check(text))
        if(dozor_check(event, text)):
            #gs = GoogleSheet()
            
            #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "дозор (предпустынье)", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
            #gs.insertRow('Статистика!A2:F2', values)
            
            name = gs.findInd(event.object.message['from_id'])

            values = [ [ f"{name}", f"{now_time}", "Дозор (пп)", "", "2", f"{event.object.message['conversation_message_id']}" ] ]
            gs.insertRow('Статистика!A2:F2', values)
            #gs.insertInMain('P', event.object.message['from_id'], 2)
            #gs.insertInMain('H', event.object.message['from_id'], 1)

    elif 'помя стат весь' in text:
        statMass, date1, date2 = gs.stat(event.object.message['from_id'], True)
        ms_send(event.chat_id, f"Стат весь\nДозор (пп): {statMass[0][9]}\nДозор (дерево): {statMass[0][8]}\nРейд на мель: {statMass[0][7]}\nСбор (гнездо): {statMass[0][2]}\nСбор (уступы): {statMass[0][0]}\nСбор (ущелье): {statMass[0][1]}\nСбор (дупло): {statMass[0][4]}\nСбор (расщелина): {statMass[0][5]}\nСбор со дна: {statMass[0][12]}\nПатрули: {statMass[0][9]}\nХохота: {statMass[0][16]}\nВсего ресурсов: {statMass[0][13]}, Всего баллов: {statMass[0][17]}")        #ms_send(event.chat_id, dozor_check(event, text))
    elif 'помя стат' in text:
        statMass, data1, data2 = gs.stat(event.object.message['from_id'], False)
        #print(statMass)
        #print(statMass[0][8])
        ms_send(event.chat_id, f"Стат с {data1} по {data2}\nДозор (пп): {statMass[0][9]}\nДозор (дерево): {statMass[0][8]}\nРейд на мель: {statMass[0][7]}\nСбор (гнездо): {statMass[0][2]}\nСбор (уступы): {statMass[0][0]}\nСбор (ущелье): {statMass[0][1]}\nСбор (дупло): {statMass[0][4]}\nСбор (расщелина): {statMass[0][5]}\nСбор со дна: {statMass[0][12]}\nПатрули: {statMass[0][9]}\nХохота: {statMass[0][16]}\nВсего ресурсов: {statMass[0][13]}, Всего баллов: {statMass[0][17]}")
        #ms_send(event.chat_id, "Do you wanna dance, baby? I know you see me lookin' at you on the daily")
        #ms_send(event.chat_id, "прочитано")
    
    elif 'помощь' == text:
        #GoogleSheet.insertRow()
        #gs = GoogleSheet()
        #gs.insertRow()
        ms_send(event.chat_id, "дозор (предпустынье) (время)\nдозор (активный) (время)\nдозор (дерево) (время)\nсбор со дна (ресы)\nунес(ла) ресурсы с мели (ресы)\nсбор с ущелья (ресы)")
        ms_send(event.chat_id, "сбор с уступов (ресы)\nСбор с дупла (ресы\nсбор со дна (ресы)\nсбор с гнезд (ресы)\nсбор с расщелины (ресы)\nсбор со дна (ресы)\nохота\nсопровождения всех мастей\nнаблюдение за звездами: (имена через запятую)\nпомощь гостям\nунес(ла) соплеменника с дерева\nунес(ла) соплеменника (от ущелья до уступов)\nунес(ла) соплеменника (с ущелья/уступов в лагерь)\nунес(ла) соплеменника (из лагеря на ущелье/уступы)\nунес(ла) соплеменника (спец.выход)\nунес(ла) соплеменника (лагерь - ущелье/уступы - лагерь)\nунес(ла) соплеменника (лагерь - ущелье - уступы - лагерь)\n\nПатруль за камнями (ночёвка)\nВедущий: (имя)\nУчастники: (имена через запятую)\n\nПатруль за камнями (сокращенный)\nВедущий: (имя)\nУчастники: (имена через запятую)\n\nРейд к лисобойной\nВедущий: (имя).\nСледящий: (имя).\nЗамыкающий: (имя).\n\nПатрули и рейд нужно отменять 2 раза!")

    elif 'сбор с ущелья' in text:
        res = res_counter(text)
        #gs = GoogleSheet()
        
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор (ущелья)", f"{res}", f"{6 + 3*res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)

        ms_send(event.chat_id, f"Сбор с ущелья засчитан, {name}\nРесурсов: {res}\nБаллов: {3*res + 6}")

    elif 'сбор с уступов' in text:
        res = res_counter(text)
        #gs = GoogleSheet()
        
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор (уступы)", f"{res}", f"{6 + 2*res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        
        #ms_send(event.chat_id, f"вы получили {res*2 + 6} баллов")
        ms_send(event.chat_id, f"Сбор с уступов засчитан, {name}\nРесурсов: {res}\nБалло: {2*res + 6}")

    elif 'дозор (активный)' in text:
        #print(dozor_check(text))
        if(dozor_check(event, text)):
            #gs = GoogleSheet()
            
            #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "дозор (активный)", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
            #gs.insertRow('Статистика!A2:F2', values)

           
            name = gs.findInd(event.object.message['from_id'])
            values = [ [ f"{name}", f"{now_time}", "Дозор (актив)", "", "3", f"{event.object.message['conversation_message_id']}" ] ]
            gs.insertRow('Статистика!A2:F2', values)
            ms_send(event.chat_id, f"Баллов: 3")
            #gs.insertInMain('P', event.object.message['from_id'], 3)
            #gs.insertInMain('H', event.object.message['from_id'], 1)

    elif 'дозор (дерево)' in text:
        #print(dozor_check(text))
        if(dozor_check(event, text)):
            #gs = GoogleSheet()
            
            #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "дозор (дерево)", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
            #gs.insertRow('Статистика!A2:F2', values)

            
            name = gs.findInd(event.object.message['from_id'])
            values = [ [ f"{name}", f"{now_time}", "Дозор (дерево)", "", "2", f"{event.object.message['conversation_message_id']}" ] ]
            gs.insertRow('Статистика!A2:F2', values)
            ms_send(event.chat_id, f"Баллов: 2")
            #gs.insertInMain('P', event.object.message['from_id'], 2)
            #gs.insertInMain('M', event.object.message['from_id'], 1)

        #ms_send(event.chat_id, dozor_check(event, text))

    elif 'сбор со дна' in text:#########################################################################################
        res = res_counter(text)
        #gs = GoogleSheet()
        
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сбор со дна", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        #values = [ [ "Ночное Вдохновение", f"{now_time}", "Cбор со дна", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)

        
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор со дна", f"{res}", f"{1 + res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)

        #gs.insertInMain('P', event.object.message['from_id'], 1 + res)
        #gs.insertInMain('F', event.object.message['from_id'], 1)
        #gs.insertInMain('L', event.object.message['from_id'], res)
        ms_send(event.chat_id, f"Сбор со дна засчитан, {name}\nРесурсов: {res}\nБаллов: {res + 1}")
        #ms_send(event.chat_id, f"вы собрали {res} ресурсов")
##начало унёс##################################################################################################################
    elif ('унес ресурсы с мели') in text:
        res = res_counter(text)
        #gs = GoogleSheet()
      
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "унес ресурсы с мели", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)

       
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Рейд на мель", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)

        ms_send(event.chat_id, f"Рейд на мель засчитан, {name}\nЗаходов: {res}\nБаллов: {res}")

    elif ('унесла ресурсы с мели') in text:
        res = res_counter(text)
        #gs = GoogleSheet()
       
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "унесла ресурсы с мели", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
        
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Рейд на мель", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Рейд на мель засчитан, {name}\nЗаходов: {res}\nБаллов: {res}")    

    elif ('унес ресурсы со дна') in text:
        print(1234567)
        res = res_counter(text)
        #gs = GoogleSheet()
       
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "унес ресурсы со дна", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)

       
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор со дна", f"{res}", f"{1+res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)

        ms_send(event.chat_id, f"Ресурсы со дна унесены, {name}\nЗаходов: {res}\nБаллов: {res*0.5}")

    elif ('унесла ресурсы со дна') in text:
        #print(1234567)
        res = res_counter(text)
        #gs = GoogleSheet()
        
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "унесла ресурсы со дна", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)

       
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор со дна", f"{res}", f"{1+res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Ресурсы со дна унесены, {name}\nЗаходов: {res}\nБаллов: {res*0.5}")
    elif 'унес соплеменника' in text:
        text = text.replace("унес соплеменника ", "")
        unesla(event, text)

    elif 'унесла соплеменника' in text:
        text = text.replace("унесла соплеменника ", "")
        unesla(event, text)

##конец унёс###########################################################################################################################
    elif 'сбор с гнезд' in text:
        res = res_counter(text)
        #gs = GoogleSheet()
        
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сбор с гнезд", "", "6", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)

        
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор (гнездо)", f"{res}", "6", f"{event.object.message['conversation_message_id']}" ] ]
        #print(values)
        #print(name)
        gs.insertRow('Статистика!A2:F2', values)

        #gs.insertInMain('P', event.object.message['from_id'], 6)


        ms_send(event.chat_id, f"Сбор с гнезд засчитан, {name}\nРесурсов: {res}\nБаллов: 6")

    elif ('сбор с дупла') in text:
        res = res_counter(text)
        #gs = GoogleSheet()
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор (дупло)", f"{res}", f"{2 + 2*res}", f"{event.object.message['conversation_message_id']}" ] ]
        #print(values)
        #print(name)
        gs.insertRow('Статистика!A2:F2', values)
        #gs.findInd(395491169)
        #gs.insertInMain('P', event.object.message['from_id'], (6 + res*2))
        #ms_send(event.chat_id, f"вы собрали {res} ресурсов и {2+2*res} баллов")  
        ms_send(event.chat_id, f"Ресурсы с дупла унесены, {name}\nРесурсов: {res}\nБаллов: {2+2*res}")
        #ms_send(event.chat_id,  f"{2 + 2*res} баллов начислено, {name}")
        

    elif ('сбор с расщелины') in text:
        res = res_counter(text)
        #res = res_counter(text)
        #gs = GoogleSheet()

        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сбор с расщелины", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)

 
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сбор (расщелина)", f"{res}", f"{2+res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)

        ms_send(event.chat_id, f"Сбор с расщелины засчитан, {name}\nРесурсов: {res}\nБаллов: {res+2}")

    elif 'сбор1' in text: ##################################################################################################
        res = res_counter(text)
        res = res_counter(text)
        #gs = GoogleSheet()

        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "сбор", f"{res}", f"{res}", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")
    
    elif 'патруль за камнями (ночевка)' in text:
        uchi = []
        voda, count, uchi = name_found(text)
        values = [ [ f"{voda[1:]}", f"{now_time}", "Патруль", "", "20", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        #ms_send(event.chat_id, f"ведущий: {voda}")
        names = ""
        for i in range(count):
            values = [ [ f"{uchi[i]}", f"{now_time}", "Патруль", "", "20", f"{event.object.message['conversation_message_id']}" ] ]
            gs.insertRow('Статистика!A2:F2', values)
            names += uchi[i]
            names += ' '  
        ms_send(event.chat_id, f"Ведущий: {voda}, Баллов: 20\nУчастники: {names}, Каждому по 20 баллов")   
        #values = [ [ f"{name}", f"{now_time}", "Сбор (расщелина)", f"{res}", f"{2+res}", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)


    elif 'патруль за камнями (сокращенный)' in text:
        uchi = []
        voda, count, uchi = name_found(text)
        values = [ [ f"{voda[1:]}", f"{now_time}", "Патруль", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        
        names = ""
        for i in range(count):
            values = [ [ f"{uchi[i]}", f"{now_time}", "Патруль", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
            gs.insertRow('Статистика!A2:F2', values)
            names += uchi[i]
            names += ', '  
        ms_send(event.chat_id, f"Ведущий: {voda}, Баллов: 10\nУчастники: {names}, Каждому по 10 баллов")       
        #ms_send(event.chat_id, "вы собрали ресурсов")
    
    elif 'охота' in text:
        res = res_counter(text)
        #gs = GoogleSheet()
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "охота", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)

        name = gs.findInd(event.object.message['from_id'])

        values = [ [ f"{name}", f"{now_time}", "Охота", f"{res}", "7", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)

        ms_send(event.chat_id, f"Хохота засчитана, {name}\nРесурсов: {res}\nБаллов: 7")
    
    elif ('сопроводил речных до ск') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение речных до ск", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
        name = gs.findInd(event.object.message['from_id'])

        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")

    elif ('сопроводила речных до ск') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()

        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение речных до ск", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
    
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)

        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")

    elif ('сопроводил речных домой') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()
     
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение речных домой", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
        
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")

    elif ('сопроводила речных домой') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()
        
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение речных домой", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")
    
    elif ('сопроводил союзников до лагеря') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()
  
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение союзников до лагеря", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
       
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")

    elif ('сопроводила союзников до лагеря') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()
     
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение союзников до лагеря", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
       
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")

    elif ('сопроводил союзников до предгорий') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()
     
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение союзников до предгорий", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
        
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")

    elif ('сопроводила союзников до предгорий') in text:
        #res = res_counter(text)
        #gs = GoogleSheet()
       
        #values = [ [ f"{event.object.message['from_id']}", f"{now_time}", "сопровождение союзников до предгорий", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
       
        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Сопровождение", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Сопровождение засчитано, {name}\nБаллов: 10")

    elif 'рейд к лисобойной' in text:
        count, reiders = reid(text)
        names = ""
   
        for i in range(count):
            values = [ [ f"{reiders[i]}", f"{now_time}", "Рейд", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
            gs.insertRow('Статистика!A2:F2', values)
            names += reiders[i]
            names += ', '
        ms_send(event.chat_id, f"участники рейда: {names}, Каждому по 10 баллов") 
    elif 'наблюдение за звездами' in text:
        count, uchi = nabludali(text)
        names = ""

        for i in range(count):
            values = [ [ f"{uchi[i]}", f"{now_time}", "Патруль", "", "10", f"{event.object.message['conversation_message_id']}" ] ]
            gs.insertRow('Статистика!A2:F2', values)
            names += uchi[i]
            names += ', '
        ms_send(event.chat_id, f"участники рейда: {names}, Каждому по 10 баллов")
    elif 'помощь гостям' in text:

        name = gs.findInd(event.object.message['from_id'])
        values = [ [ f"{name}", f"{now_time}", "Помощь гостям", "", "5", f"{event.object.message['conversation_message_id']}" ] ]
        gs.insertRow('Статистика!A2:F2', values)
        ms_send(event.chat_id, f"Помощь засчитана, {name}\nБаллов: 5")
    
    elif 'проверка дозора' in text:
        #current_date = datetime.datetime.now()
        #now_time = f"{current_date.day}.{current_date.month}.{current_date.year}"
        #name = gs.findInd(event.object.message['from_id'])
        #values = [ [ f"{name}", f"{now_time}", "До", "", "1", f"{event.object.message['conversation_message_id']}" ] ]
        #gs.insertRow('Статистика!A2:F2', values)
        name = gs.findInd(event.object.message['from_id'])
        ms_send(event.chat_id, f"проверка засчитана, {name}\nБаллов: 1")
    

def main():
    for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                user_id = event.object.message['from_id']
                chat_id = event.chat_id
                #print(event)
                #print(event.object.message['conversation_message_id'])
                text = event.object.message['text'].lower()
                try:
                    full_inf_user = get_name(user_id)
                    full_inf_user+= ' id: '
                    full_inf_user+=str(user_id)
                    full_inf_user+=' message: '
                    full_inf_user+=text
                    #print(full_inf_user)
                    #ms_send(event.chat_id, full_inf_user)
                except:
                    print("'Err event.object.message or full_name def'")

                th = Thread(target = check_pattern, args = (event, str(text), ))
                th.start()
            '''
            if text == "отмена":

                
                if 'reply_message' in list(event.object.message):
                    #ms_send(chat_id, str(event.object.message['reply_message']['text']))
                    #ms_send(chat_id, "отменено")
                    #print(event)
                    #print(event.object.message['reply_message']['conversation_message_id'])
                    gs = GoogleSheet()
                    th = Thread(target = gs.delFromStat, args = (event.object.message['reply_message']['conversation_message_id'], event.chat_id, ))
                    th.start()    
                else:
                    ms_send(chat_id, "пожалуйста ответьте на сообщение, которое хотите отменить")
            else:
                th = Thread(target = check_pattern, args = (event, text, ))
                th.start()    
            '''


if __name__ == '__main__':
    vk_session = VkApi(token = "dfad8d11d321d20a634d2290b6c117eb02c43e50a8449d25c993d95dd12c36491b2f7bda1183bdf91924f")
    longpoll = VkBotLongPoll(vk_session, 188445979)
    vk = vk_session.get_api()
    while True:
        try:
            main()
        except:
            vk_session = VkApi(token = "dfad8d11d321d20a634d2290b6c117eb02c43e50a8449d25c993d95dd12c36491b2f7bda1183bdf91924f")
            longpoll = VkBotLongPoll(vk_session, 188445979)
            vk = vk_session.get_api()
'''
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        user_id = event.object.message['from_id']
        chat_id = event.chat_id
        #print(event)
        text = event.object.message['text'].lower()
        try:
            full_inf_user = get_name(user_id)
            full_inf_user+= ' id: '
            full_inf_user+=str(user_id)
            full_inf_user+=' message: '
            full_inf_user+=text
            #print(full_inf_user)
            #ms_send(event.chat_id, full_inf_user)
        except:
            print("'Err event.object.message or full_name def'")

        if text == "отмена":

            if 'reply_message' in list(event.object.message):
                #ms_send(chat_id, str(event.object.message['reply_message']['text']))
                ms_send(chat_id, "отменено")
            else:
                ms_send(chat_id, "пожалуйста ответьте на сообщение, которое хотите отменить")
        else:
            th = Thread(target = check_pattern, args = (event, text, ))
            th.start()    
'''
        