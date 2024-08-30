from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import timedelta
from celery import shared_task


@shared_task
def check_users():
    # Получаем пользователей, которые неактивны более 30 дней
    users = User.objects.filter(last_login__lte=timezone.now() - timedelta(days=30), is_active=True)

    if users.exists():
        # Деактивируем пользователей
        users.update(is_active=False)

        # Собираем email адреса
        emails = [user.email for user in users]

        # Отправляем уведомление
        try:
            send_mail(
                subject='Внимание!!!',
                message='Вы заблокированы',
                from_email=EMAIL_HOST_USER,
                recipient_list=emails,
            )
        except Exception as e:
            print(f'Ошибка при отправке почты: {e}')
