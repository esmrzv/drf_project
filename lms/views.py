from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


class LmsViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsModer | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner | ~IsModer]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.requests.user
        course_id = self.reqests.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.all().filter(user=user).filter(course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(course=course_item, user=user)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})


