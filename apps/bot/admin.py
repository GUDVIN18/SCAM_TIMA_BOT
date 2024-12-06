# Register your models here.
from django.contrib import admin
from .models import *




# admin.site.register(FSM_Controller)




@admin.register(TelegramBotConfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    fields = [
        "bot_token",
        'is_activ',
    ]
    list_display = (
        "id",
        "bot_token",
        'is_activ',
    )
    list_filter = (
        "bot_token",
        'is_activ',
    )
    search_fields = (
        "bot_token",
    )


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {  # Основная информация
            "fields": ("tg_id", "first_name", "last_name", "username", "language", "premium", "state"),
        }),
        ("Settings Project", {  # Группа для кастомных полей
            "fields": (
                "status",
                "data_register",
                "project_percentage",
                "today_profit_count",
                "today_profit_amount",
                "total_profit_count",
                "total_profit_amount",
                "has_mentor",
                "payment_wallet",
                "token_temporary",
            ),
        }),
    )

    list_display = (
        "tg_id",
        "first_name",
        "username",
        "state",
    )
    list_filter = (
        "tg_id",
        "username",
    )
    search_fields = (
        "tg_id",
        "username",
        "id",
    )




class Bot_ButtonStackedInline(admin.StackedInline):
    model = Bot_Button
    extra = 1
    fields = (
        ('text', 'data', 'btn_type'),
    )


@admin.register(Bot_Message)
class Bot_MessageAdmin(admin.ModelAdmin):
    inlines = [Bot_ButtonStackedInline]
    fields = [
        "text",
        "current_state",
        "next_state",
        "anyway_link",
        "handler",
    ]
    list_display = (
        "text", 
        "current_state",
        "next_state",
        "handler",
    )
    list_filter = (
        "handler",
    )
    search_fields = (
        "handler",
    )



@admin.register(Bot_Commands)
class Bot_CommandsAdmin(admin.ModelAdmin):
    fields = [
        "text",
        "trigger",
    ]
    list_display = (
        "text",
        "trigger",
    )
    list_filter = (
        "text",
        "trigger",
    )
    search_fields = (
        "text",
        "trigger",
    )






@admin.register(Bot_Button)
class Bot_ButtonAdmin(admin.ModelAdmin):
    fields = [
        "text",
        "message_trigger",
        "data"
    ]
    list_display = (
        "text",
        "message_trigger",
    )
    list_filter = (
        "text",
        "message_trigger",
    )
    search_fields = (
        "text",
        "message_trigger",
    )





@admin.register(Mentors)
class MentorsAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "username",
        "desciptions",
    ]
    list_display = (
        "name",
        "username",
    )
    list_filter = (
        "name",
        "username",

    )
    search_fields = (
        "name",
        "username",
    )




@admin.register(Profit)
class ProfitAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "price",
        "data",
    ]
    list_display = (
        "user",
        "price",
        "data"
    )
    list_filter = (
        "data",

    )
    search_fields = (
        "user",
        "price",
        "data",
    )


@admin.register(Referal)
class ProfitAdmin(admin.ModelAdmin):
    fields = [
        "user_main",
        "user_invite",
    ]
    list_display = (
        "user_main",
        "user_invite",
    )






class Country_SitesStackedInline(admin.StackedInline):
    model = Country_Sites
    extra = 1
    fields = (
        ('name_country', 'name', 'url', 'is_active'),
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [Country_SitesStackedInline]
    fields = [
        "name",
    ]
    list_display = (
        "name",
    )
    list_filter = (
        "name",
    )
    search_fields = (
        "name",
    )



from django.contrib import admin
# from .models import Domain

# @admin.register(Domain)
# class DomainAdmin(admin.ModelAdmin):
#     list_display = ('name', 'is_active', 'created_at')



@admin.register(DataUserSite)
class DataUserSiteAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "token",
        "product_name",
        "url",
        "scam_url",
        "service",
        "price",
        "image",
        "name",
        "address",
        "last_active",
        "data_json",
        "support_json",
    ]
    list_display = (
        "user",
        "token",
    )
    list_filter = (
        "user",
        "token",
    )
    search_fields = (
        "user",
        "token",
    )






@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    fields = [
        "username",
        "password",
        "proxy_host",
        "proxy_port",
    ]
    list_display = (
        "username",
        "password",
        "proxy_host",
        "proxy_port",
    )
    list_filter = (
        "proxy_host",
    )
    search_fields = (
        "username",
        "password",
        "proxy_host",
        "proxy_port",
    )
