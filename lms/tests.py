from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(last_name='test', first_name='test', email='test@test.ru', phone='89066594545',
                                        city='moscow')
        self.course = Course.objects.create(name='Python', description='backend', owner=self.user)
        self.lesson = Lesson.objects.create(name='Урок по ООП', description='пробный урок', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson-retrieve', args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name
        )
        self.assertEqual(
            data.get('description'), self.lesson.description,
        )
        self.assertEqual(
            data.get('course'), self.course.pk
        )
        self.assertEqual(
            data.get('owner'), self.user.pk
        )

    def test_lesson_update(self):
        url = reverse('lms:lesson-update', args=[self.lesson.pk])
        data = {'name': 'Урок по джанго', 'description': 'Платный урок по джанго'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        ),
        self.assertEqual(
            data.get('name'), 'Урок по джанго'
        ),
        self.assertEqual(
            data.get('description'), 'Платный урок по джанго'
        )

    def test_lesson_create(self):
        url = reverse('lms:lesson-create')
        data = {'name': 'аутентификация', 'description': 'права доступа', 'course': self.course.pk,
                'owner': self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_delete(self):
        url = reverse('lms:lesson-delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_lesson_list(self):
        url = reverse('lms:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "preview": None,
                    "description": self.lesson.description,
                    "video_link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            result, data
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(last_name='adamasov', first_name='adam', email='test1@test.ru', phone='89066594545',
                                        city='kair')
        self.course = Course.objects.create(name='Python3', description='backender')
        self.client.force_authenticate(user=self.user)

    def test_subscription_add(self):
        url = reverse('lms:course-subscribe')
        data = {'course': self.course.pk, 'user': self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {'message': 'подписка добавлена'}
        )

    def test_subscription_deactivate(self):
        url = reverse('lms:course-subscribe')
        Subscription.objects.create(user=self.user, course=self.course)
        data = {'user': self.user.id,
                'course': self.course.id}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'подписка удалена'})






