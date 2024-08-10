from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта', unique=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    city = models.CharField(max_length=50, verbose_name='Город')
    avatar = models.ImageField(upload_to='media/photo', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, null=True, blank=True,
                               on_delete=models.CASCADE)  # Урок может быть не обязательно
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=[('cash', 'Наличные'), ('transfer', 'Перевод на счет')],
                                      default='transfer', verbose_name='способ оплаты')

    def __str__(self):
        return f'Оплатил: {self.user} по {self.course} в {self.payment_date}'
