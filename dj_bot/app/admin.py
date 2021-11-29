from django.contrib import admin
from .models import *


class TicketAdmin(admin.ModelAdmin):

    list_display = ('user', 'event',)
    list_filter = ('event__date',)
    search_fields = ('user__user_name', 'user__id_tg', 'event__slug', 'event__id',)


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user_name', )
    search_fields = ('user_name', 'id_tg')


class EventAdmin(admin.ModelAdmin):
    fields = ('price', 'slug', 'count_tickets', 'date', 'bank', 'busy_tickets')
    list_filter = ('date', 'price', 'count_tickets', 'bank')
    search_fields = ('slug',)


class BalanceAdmin(admin.ModelAdmin):

    list_filter = ('created_at', 'updated_at',)
    search_fields = ('user__user_name', 'user__id_tg',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(ArchiveGame)
