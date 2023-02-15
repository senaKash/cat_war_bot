from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from threading import Thread
import re
import datetime
#from datetime import datetime, date

vk_session = VkApi(token = "dfad8d11d321d20a634d2290b6c117eb02c43e50a8449d25c993d95dd12c36491b2f7bda1183bdf91924f")
longpoll = VkBotLongPoll(vk_session, 188445979)
vk = vk_session.get_api()


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

def dozor_check(text):

    time = [int(s) for s in re.findall(r'\b\d+\b', text)]
    now_time = []
    current_date = datetime.datetime.now()
    now_time.append(current_date.hour)
    now_time.append(current_date.minute)
    print(now_time, time)
    if(time[0]-now_time[0] == 0 and abs(time[1]-now_time[1]) < 5):
        ms_send(event.chat_id, "принято")
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

def check_pattern(event, text):
    if 'дозор (предпустынье)' in text:
        #print(dozor_check(text))
        ms_send(event.chat_id, dozor_check(text))
    elif 'помощь' in text:
        ms_send(event.chat_id, "тут будет хелп")
    elif 'дозор (активный)' in text:
        #print(dozor_check(text))
        ms_send(event.chat_id, dozor_check(text))
    elif 'дозор (дерево)' in text:
        #print(dozor_check(text))
        ms_send(event.chat_id, dozor_check(text))
    elif 'сбор со дна' in text:
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")

    elif ('унес ресурсы с мели') in text:
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")

    elif ('унесла ресурсы с мели') in text:
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")    

    elif ('унес ресурсы со дна') in text:
        print(1234567)
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")

    elif ('унесла ресурсы со дна') in text:
        print(1234567)
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")

    elif 'сбор с гнёзд' in text:
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")

    elif ('сбор с дупла') in text:
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")

    elif ('сбор с расщелины') in text:
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")

    elif 'сбор' in text:
        res = res_counter(text)
        ms_send(event.chat_id, f"вы собрали {res} ресурсов")
    
    elif 'патруль за камнями (ночёвка)' in text:
        uchi = []
        voda, count, uchi = name_found(text)
        ms_send(event.chat_id, f"ведущий - {voda}")
        names = ""
        for i in range(count):
            names += uchi[i]
            names += ', '  
        ms_send(event.chat_id, f"участники: {names}")

    elif 'патруль за камнями (сокращённый)' in text:
        uchi = []
        voda, count, uchi = name_found(text)
        ms_send(event.chat_id, f"ведущий - {voda}")
        names = ""
        for i in range(count):
            names += uchi[i]
            names += ', '  
        ms_send(event.chat_id, f"участники: {names}")       
        #ms_send(event.chat_id, "вы собрали ресурсов")
    
    elif 'охота' in text:
        ms_send(event.chat_id, "охота засчитана")
    
    elif ('сопроводил речных до ск') in text:
        ms_send(event.chat_id, "сопровождение засчитано")

    elif ('сопроводила речных до ск') in text:
        ms_send(event.chat_id, "сопровождение засчитано")

    elif ('сопроводил речных домой') in text:
        ms_send(event.chat_id, "сопровождение засчитано")
    elif ('сопроводила речных домой') in text:
        ms_send(event.chat_id, "сопровождение засчитано")
    
    elif ('сопроводил союзников до лагеря') in text:
        ms_send(event.chat_id, "сопровождение засчитано")
    elif ('сопроводила союзников до лагеря') in text:
        ms_send(event.chat_id, "сопровождение засчитано")

    elif ('сопроводил союзников до предгорий') in text:
        ms_send(event.chat_id, "сопровождение засчитано")
    elif ('сопроводила союзников до предгорий') in text:
        ms_send(event.chat_id, "сопровождение засчитано")

    elif 'рейд к лисобойной' in text:
        count, reiders = reid(text)
        names = ""
        for i in range(count):
            names += reiders[i]
            names += ', '
        ms_send(event.chat_id, f"участники рейда: {reiders}") 

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

        