from celery import shared_task
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


@shared_task
def check_subscribe(email):
    try:
        send_mail(
            subject="Обновление курса",
            message="Курс по подписке обновлен",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )
    except Exception as e:
        print(f"Ошибка при отправке письма {e}")
