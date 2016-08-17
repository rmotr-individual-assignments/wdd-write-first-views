from datetime import date
from copy import deepcopy

from django.contrib.auth.models import User
from django.test import TestCase

from students import views


class BaseTestCase(TestCase):

    def setUp(self):
        views.STUDENTS = [
            {
                "id": 10,
                "name": "John Snow",
                "age": 36,
                "birth_date": date(1980, 1, 1),
                "active": True
            },
            {
                "id": 23,
                "name": "Daenerys Targaryen",
                "age": 30,
                "birth_date": date(1986, 1, 1),
                "active": True
            },
            {
                "id": 4,
                "name": "Arya Stark",
                "age": 20,
                "birth_date": date(1996, 1, 1),
                "active": False
            },
        ]


class StudentListTestCase(BaseTestCase):

    def test_students_list(self):
        response = self.client.get('/students')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response._headers['content-type'],
            ('Content-Type', 'text/html; charset=utf-8'))
        content = response.content.decode('utf-8')
        self.assertIn('<li>Daenerys Targaryen (30)</li>', content)
        self.assertIn('<li>John Snow (36)</li>', content)
        self.assertNotIn('<li>Arya Stark (20)</li>', content)  # not showing inactive students

    def test_students_list_json_response(self):
        response = self.client.get('/students', {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response._headers['content-type'],
            ('Content-Type', 'application/json'))
        expected = {
            'students': [
                {
                    'id': 10,
                    'birth_date': '1980-01-01',
                    'active': True,
                    'age': 36,
                    'name': 'John Snow'
                },
                {
                    'id': 23,
                    'birth_date': '1986-01-01',
                    'active': True,
                    'age': 30,
                    'name': 'Daenerys Targaryen'
                },
                {
                    'id': 4,
                    'birth_date': '1996-01-01',
                    'active': False,
                    'age': 20,
                    'name': 'Arya Stark'
                }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_students_create(self):
        payload = {
            'id': 40,
            'birth_date': '1995-01-01',
            'active': True,
            'age': 21,
            'name': 'Joffrey Baratheon'
        }
        response = self.client.post('/students', data=payload)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/students', {'format': 'json'})
        self.assertEqual(len(response.json()['students']), 4)
        expected = {
            'active': True,
            'birth_date': '1995-01-01',
            'age': 21,
            'name': 'Joffrey Baratheon',
            'id': 40
        }
        self.assertEqual(response.json()['students'][3], expected)

    def test_students_create_missing_required_fields(self):
        payload = {
            'foo': 'bar'
        }
        response = self.client.post('/students', data=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         'POSTed student data is incomplete or invalid')

    def test_students_create_invalid_fields_types(self):
        payload = {
            'id': 'foobar',
            'birth_date': 123,
            'active': 'something',
            'age': True,
            'name': None
        }
        response = self.client.post('/students', data=payload)
        self.assertEqual(response.status_code, 400)


class StudentDetailTestCase(BaseTestCase):

    def test_students_detail(self):
        response = self.client.get('/students/10')
        self.assertEqual(response.status_code, 200)
        expected = {
            'id': 10,
            'name': 'John Snow',
            'birth_date': '1980-01-01',
            'active': True,
            'age': 36,
        }
        self.assertEqual(response.json(), expected)

    def test_students_detail_not_found(self):
        response = self.client.get('/students/10000')
        self.assertEqual(response.status_code, 404)


class StudentMeTestCase(BaseTestCase):

    def setUp(self):
        super(StudentMeTestCase, self).setUp()
        self.user = User.objects.create(id=10)

    def test_students_me_not_authenticated(self):
        response = self.client.get('/students/me')
        self.assertEqual(response.status_code, 302)  # redirects to login

    def test_students_me(self):
        self.client.force_login(self.user)
        response = self.client.get('/students/me', follow=True)
        self.assertEqual(response.status_code, 200)
        expected = {
            'id': 10,  # authenticated user has id=10
            'age': 36,
            'birth_date': '1980-01-01',
            'active': True,
            'name': 'John Snow'
        }
        self.assertEqual(response.json(), expected)

    def test_students_me_post(self):
        self.client.force_login(self.user)
        response = self.client.post('/students/me', follow=True)
        self.assertEqual(response.status_code, 405)


class StudentSearchTestCase(BaseTestCase):

    def test_student_search_missing_query_param(self):
        response = self.client.get('/students/search')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'),
                         '"query" param must be provided')

    def test_student_search(self):
        response = self.client.get('/students/search', {'query': 'snow'})
        self.assertEqual(response.status_code, 200)
        expected = {
            'results': [
                {
                    'birth_date': '1980-01-01',
                    'active': True,
                    'age': 36,
                    'id': 10,
                    'name': 'John Snow'
                }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_student_search_case_insensitive(self):
        response = self.client.get('/students/search', {'query': 'sNoW'})
        self.assertEqual(response.status_code, 200)
        expected = {
            'results': [
                {
                    'birth_date': '1980-01-01',
                    'active': True,
                    'age': 36,
                    'id': 10,
                    'name': 'John Snow'
                }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_student_search_multiple_match(self):
        response = self.client.get('/students/search', {'query': 'ar'})
        self.assertEqual(response.status_code, 200)
        expected = {
            'results': [
                {
                    'birth_date': '1986-01-01',
                    'active': True,
                    'age': 30,
                    'id': 23,
                    'name': 'Daenerys Targaryen'
                },
                {
                    'birth_date': '1996-01-01',
                    'active': False,
                    'age': 20,
                    'id': 4,
                    'name': 'Arya Stark'
                }
            ]
        }
        self.assertEqual(response.json(), expected)
