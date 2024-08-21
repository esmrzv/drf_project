from rest_framework.serializers import ValidationError


class LessonCustomValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not (value.startswith('https://youtube.com') or value.startswith('https://www.youtube.com')):
            raise ValidationError('Запрещены сторонние ссылки, кроме YouTube.')
