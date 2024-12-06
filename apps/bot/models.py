from django.db import models
from datetime import date
from django.utils.timezone import now


class TelegramBotConfig(models.Model):
    bot_token = models.CharField(max_length=100)
    is_activ = models.BooleanField(null=False, blank=False, default=False, verbose_name="Is active")

    def __str__(self):
        return f'{self.bot_token}'

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"





class BotUser(models.Model):
    tg_id = models.BigIntegerField(unique=True, verbose_name="ID Telegram")
    first_name = models.CharField(max_length=250, verbose_name="Имя пользователя", blank=True, null=True)
    last_name = models.CharField(max_length=250, verbose_name="Фамилия пользователя", blank=True, null=True)
    username = models.CharField(max_length=250, verbose_name="Username пользователя", blank=True, null=True)
    language = models.CharField(max_length=250, verbose_name="Язык пользователя", blank=True, null=True)
    premium = models.BooleanField(verbose_name="Имеет ли пользователь премиум-аккаунт", default=False, blank=True, null=True)
    state = models.CharField(max_length=255, help_text='Состояние')

    #Кастомные настройки под проект
    status = models.CharField(max_length=100, verbose_name="Статус", null=True, blank=True)
    data_register = models.DateField(verbose_name="Дней в проекте", null=True, blank=True, default=date.today)

    project_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент в проекте", null=True, blank=True,  default=0)

    today_profit_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Сегодняшнее количество профитов", default=0)

    today_profit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Сумма профитов за сегодня (USD)", default=0)

    total_profit_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Общее количество профитов", default=0)
    total_profit_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Общая сумма профитов (USD)", default=0)
    has_mentor = models.CharField(max_length=255, verbose_name="Есть ли наставник", null=True, blank=True)
    payment_wallet = models.CharField(max_length=255, null=True, blank=True, verbose_name="Кошелёк для выплат")
    tokensmartsupp = models.CharField(max_length=255, null=True, blank=True, verbose_name="tokensmartsupp")
    activate_account = models.BooleanField(default=False)
    token_temporary = models.CharField(max_length=255, verbose_name="Временный токен для передачи", null=True, blank=True)
    # service_display_enabled = models.BooleanField(default=True, verbose_name="Отображение сервиса залета")


    def __str__(self):
        return f"user_object {self.tg_id} {self.username}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"






class Bot_Message(models.Model):
    text = models.TextField(verbose_name="Текст сообщения")
    current_state =  models.CharField(max_length=110, verbose_name="К какому состоянию привязана?", default=None, unique=True)
    next_state = models.CharField(max_length=255, verbose_name="Ссылка на состояние при вводе", default=None, null=True, blank=True)
    anyway_link = models.CharField(max_length=110, help_text="На какое состояние пебрасывает пользователя", null=True, blank=True, unique=True)
    handler = models.CharField(max_length=255, verbose_name="Имя функции обработчика", null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.text[:50]}... (Состояние: {self.current_state if self.current_state is not None else self.anyway_link})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"



class Bot_Commands(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст команды")
    trigger = models.ForeignKey(Bot_Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='triggered_commands', verbose_name="Связанное сообщение")

    def __str__(self):
        return f"{self.text} (Триггер: {self.trigger})"

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"



class Bot_Button(models.Model):
    MONTH_CHOICES = (
        ("Inline", "Inline"),
        ("Reply", "Reply"),
    )

    btn_type = models.CharField(max_length=128, choices=MONTH_CHOICES, default="Inline", help_text="Тип кнопки")
    text = models.CharField(max_length=255, verbose_name="Текст кнопки")
    message_trigger = models.ForeignKey(Bot_Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='message_triggered', verbose_name="Связанное сообщение")
    data = models.CharField(max_length=255, verbose_name='Данные', default='')

    def __str__(self):
        return f"{self.text} (Триггер: {self.message_trigger})"

    class Meta:
        verbose_name = "Кнопку"
        verbose_name_plural = "Кнопки"






class Mentors(models.Model):
    name = models.CharField(max_length=255, help_text="Имя", null=True, blank=True)
    username = models.CharField(max_length=255, help_text="@username", null=True, blank=True)
    desciptions = models.TextField(help_text="Описание", null=True, blank=True)
    

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Наставника"
        verbose_name_plural = "Наставники"




class Profit(models.Model):
    user = models.ForeignKey(to=BotUser, null=True, blank=True, help_text="Стоимость", on_delete=models.SET_NULL, related_name="profit_user")
    price = models.FloatField(null=True, blank=True, help_text="Стоимость")
    data = models.DateField(null=True, blank=True, help_text="Дата получения")

    def __str__(self):
        return f"{self.user} получил {self.price} в {self.data}"


class Referal(models.Model):
    user_invite = models.ForeignKey(to=BotUser, null=True, blank=True, help_text="Кто пришел", on_delete=models.SET_NULL, related_name="ref_user_invite", verbose_name="Кто перешел")
    user_main = models.ForeignKey(to=BotUser, null=True, blank=True, help_text="Отправитель", on_delete=models.SET_NULL, related_name="ref_user_main", verbose_name="Отправитель")

    def __str__(self):
        return f"{self.user_main} пригласил {self.user_invite}"







class Country(models.Model):
    name = models.CharField(max_length=255, help_text='Название страны', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Страну"
        verbose_name_plural = "Страны"



class Country_Sites(models.Model):
    name_country = models.ForeignKey(to=Country, null=True, blank=True, help_text="К какой стране привязка", on_delete=models.SET_NULL, related_name="country_sites")
    name = models.CharField(max_length=255, help_text='Название Сайта', null=True, blank=True)
    url = models.CharField(
        max_length=555,  # Максимальная длина URL, по умолчанию 555 символов
        help_text="Введите URL-адрес",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.url}"
    
    class Meta:
        verbose_name = "Сайты стран"
        verbose_name_plural = "Сайты стран"




class DataUserSite(models.Model):
    user = models.ForeignKey(to=BotUser, null=True, blank=True, help_text="Пользователь", on_delete=models.SET_NULL, related_name="DataUserSite")
    token = models.CharField(max_length=255, null=True, blank=True, help_text="Уникальный токен для идентификации.")
    url = models.URLField(null=True, blank=True, help_text="Ориг. ссылка")
    scam_url = models.URLField(null=True, blank=True, help_text="Скам ссылка")
    product_name = models.TextField(null=True, blank=True, help_text="Наименование товара")
    service = models.CharField(max_length=255, help_text='Название сервиса', null=True, blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Цена (в формате 0.00).")
    price = models.CharField(max_length=255, null=True, blank=True, help_text="Цена (в формате 0.00).")
    image = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Изображение")
    name = models.CharField(max_length=255, null=True, blank=True, help_text="Имя продавца")
    address = models.TextField(null=True, blank=True, help_text="Адрес доставки")
    last_active = models.DateTimeField(default=now)
    data_json = models.JSONField(null=True, blank=True, help_text='json для кнопок')
    support_json = models.JSONField(null=True, blank=True, help_text='json поддержки')



    def __str__(self):
        return f"{self.token}"
    
    class Meta:
        verbose_name = "Данные пользовательской страницы"
        verbose_name_plural = "Данные пользовательской страницы"




class Proxy(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    proxy_host = models.CharField(max_length=255)
    proxy_port = models.CharField(max_length=255)

    def __str__(self,):
        return f"http://{self.username}:{self.password}@{self.proxy_host}:{self.proxy_port}"




# class Domain(models.Model):
#     """
#     Модель домена в базе данных Django
#     """
#     name = models.CharField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=now)

#     def __str__(self):
#         return self.name