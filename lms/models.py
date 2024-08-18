from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='media/course', verbose_name='Превью', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='владелец')

    def __str__(self):
        return f'{self.name} - {self.description}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='media/lesson', verbose_name="Превью", null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    video_link = models.URLField(verbose_name='Ссылка на видео', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='владелец')

    def __str__(self):
        return f'{self.name} - {self.description}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
