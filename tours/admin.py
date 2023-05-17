from django.contrib import admin
from django.apps import apps
from .models import *
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
                sender_person=request.user,
                recipient_person=obj.customer,
                content=f'Статус вашей заявки изменен на: {obj.status}\n' + additional_message
            )
            message.save()

        super().save_model(request, obj, form, change)


admin.site.register(BookingRequest, BookingRequestAdmin)

#Те модели которые не нужно регистрировать!!! Их нужно импортнуть отдельно
NOT_REGISTERED_MODELS = [Message, BookingRequest, BookingRequestPosition]
for model in app_config.get_models():
    if not (model in NOT_REGISTERED_MODELS):
        admin.site.register(model)
