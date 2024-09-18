from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import SimpleRouter
from lms.views import (
    LessonListAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    LessonRetrieveAPIView,
    SubscriptionAPIView,
)
from lms.views import LmsViewSet

app_name = LmsConfig.name

router = SimpleRouter()
router.register("", LmsViewSet)

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson-list"),
    path(
        "lesson/<int:pk>/retrieve/",
        LessonRetrieveAPIView.as_view(),
        name="lesson-retrieve",
    ),
    path(
        "lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    ),
    path("course/subscribe/", SubscriptionAPIView.as_view(), name="course-subscribe"),
]
urlpatterns += router.urls
