from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import LessonCustomValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def validate_video_link(self, value):
        validator = LessonCustomValidator(field='video_link')
        validator(value)
        return value


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    subscribers = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'lesson_count', 'lessons', 'subscribers')

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
