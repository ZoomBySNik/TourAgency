from django.contrib import admin
from django.apps import apps
from django.contrib.admin import SimpleListFilter
from .models import *
from django.db.models import Q
app_config = apps.get_app_config('tours')


class BookingPositionInline(admin.TabularInline):
    model = BookingRequestPosition
    extra = 0
    verbose_name_plural = 'Позиции заявки'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BookingRequestAdmin(admin.ModelAdmin):
    inlines = [BookingPositionInline]
    readonly_fields = ('customer', 'date_of_request')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()

        if 'status' in form.changed_data:
            if obj.status == 'processing':
                additional_message = f'В скором времени вы будете приглашены для заключения договора в офис турагентства'
            elif obj.status == 'approved':
                additional_message = f'Ваша заявка подтверждена, просьба явиться в офис турагентства в ближайшее время работы, время уточняйте на странице информации о турагентстве'
            else:
                additional_message = ''

            message = PrivateMessage(
                sender_person=User.objects.get(username='system'),
                recipient_person=obj.customer,
                content=f'Статус вашей заявки изменен на: {obj.status}\n' + additional_message
            )
            message.save()

        super().save_model(request, obj, form, change)


admin.site.register(BookingRequest, BookingRequestAdmin)


class UserMessageFilter(SimpleListFilter):
    title = 'Пользователь'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        users = User.objects.filter(Q(sender_person__isnull=False) | Q(recipient_person__isnull=False))\
            .exclude(username='system').distinct()
        choices = [(user.id, user.get_full_name()) for user in users]
        return choices

    def queryset(self, request, queryset):
        user_id = self.value()
        if user_id:
            return queryset.filter(Q(sender_person_id=user_id) | Q(recipient_person_id=user_id))
        return queryset


class PrivateMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('sender_person',)
    ordering = ('departure_date',)
    list_display = ('__str__', 'content')
    list_filter = (UserMessageFilter,)

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.sender_person = User.objects.get(username='system')
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    def content_admin_order_field(self, obj):
        return None


admin.site.register(PrivateMessage, PrivateMessageAdmin)

#Те модели которые не нужно регистрировать!!! Их нужно импортнуть отдельно
NOT_REGISTERED_MODELS = [Message, BookingRequest, BookingRequestPosition, PrivateMessage]
for model in app_config.get_models():
    if not (model in NOT_REGISTERED_MODELS):
        admin.site.register(model)
