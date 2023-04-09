from django.contrib import admin
from .models import MainUser, Lobby_EN, Lobby_RU
from django.contrib.auth.models import Group
from django.db.models import Max, Min
from django.db.models import Q

admin.site.unregister(Group)
# admin.site.sortkey_order = ['Пользователи', 'main.Lobby_EN', 'main.Lobby_RU']

class Lobby_ENInline(admin.TabularInline):
    model = Lobby_EN
    extra = 0
    readonly_fields = ('message_text', 'created_at')
    fields = ('created_at', 'message_text')
    can_delete = False
    ordering = ('-created_at',) 
    # CSS для админки 
    # class Media:
    #     css = {
    #         'all': ('admin.css',)
    #     }
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('-created_at')
        last_three = list(qs[:5])[::-1]
        last_three_ids = [obj.id for obj in last_three]
        return qs.filter(Q(id__in=last_three_ids))

class Lobby_RUInline(admin.TabularInline):
    model = Lobby_RU
    extra = 0
    readonly_fields = ('message_text', 'created_at')
    fields = ('created_at', 'message_text')
    can_delete = False
    ordering = ('-created_at',) 
    # CSS для админки 
    # class Media:
    #     css = {
    #         'all': ('admin.css',)
    #     }
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.order_by('-created_at')
        last_three = list(qs[:5])[::-1]
        last_three_ids = [obj.id for obj in last_three]
        return qs.filter(Q(id__in=last_three_ids))

@admin.register(MainUser)
class MainUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'messages_count', 'messages_last_created_at', 'messages_first_created_at', 'created_at', 'is_staff', 'is_superuser')
    search_fields = ('username',)
    list_filter = ('is_staff', 'created_at')
    readonly_fields = ('username', 'display_password', 'created_at')
    fieldsets = (
        (('Аутентификация'), {
            'fields': ('username', 'display_password')
        }),
        (('Права доступа'), {
            'fields': ('is_staff',)
        }),
    )
    inlines = [Lobby_ENInline, Lobby_RUInline]

    def display_password(self, obj):
        password = obj.password
        method, iterations, salt, hashed = password.split('$')
        return f'Method: {method}\nIterations: {iterations}\nSalt: {salt}\nHashed password: {hashed}\n\nFull password: {password}'
    display_password.short_description = 'Password'

    # Скрипты под вопросом 
    def messages_count(self, obj):
        return obj.messages_en.count() + obj.messages_ru.count()
    messages_count.short_description = 'Messages'

    def messages_last_created_at(self, obj):
        last_en_created_at = obj.messages_en.aggregate(Max('created_at'))['created_at__max']
        last_ru_created_at = obj.messages_ru.aggregate(Max('created_at'))['created_at__max']
        return max(last_en_created_at, last_ru_created_at) if last_en_created_at and last_ru_created_at else last_en_created_at or last_ru_created_at
    messages_last_created_at.short_description = 'Last Message Date'

    def messages_first_created_at(self, obj):
        first_en_created_at = obj.messages_en.aggregate(Min('created_at'))['created_at__min']
        first_ru_created_at = obj.messages_ru.aggregate(Min('created_at'))['created_at__min']
        return min(first_en_created_at, first_ru_created_at) if first_en_created_at and first_ru_created_at else first_en_created_at or first_ru_created_at
    messages_first_created_at.short_description = 'First Message Date'


@admin.register(Lobby_EN)
class Lobby_EN_Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message_text', 'created_at')
    search_fields = ('user', 'message_text')
    list_filter = ('user', 'created_at',)
    readonly_fields = ('user', 'message_text', 'created_at')
    fieldsets = (
        (('Основное'), {
            'fields': ('user', 'message_text', 'created_at')
        }),
    )


@admin.register(Lobby_RU)
class Lobby_RU_Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message_text', 'created_at')
    search_fields = ('user', 'message_text')
    list_filter = ('created_at',)
    readonly_fields = ('user', 'message_text', 'created_at')
    fieldsets = (
        (('Основное'), {
            'fields': ('user', 'message_text', 'created_at')
        }),
    )


