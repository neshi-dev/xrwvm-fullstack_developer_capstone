import json
from django.test import TestCase
from django.contrib.auth.models import User


class GetCarsViewTest(TestCase):
    """Tests for the /djangoapp/get_cars endpoint."""

    def test_returns_200(self):
        response = self.client.get('/djangoapp/get_cars')
        self.assertEqual(response.status_code, 200)

    def test_response_contains_car_models_key(self):
        response = self.client.get('/djangoapp/get_cars')
        data = response.json()
        self.assertIn('CarModels', data)

    def test_car_models_is_list(self):
        response = self.client.get('/djangoapp/get_cars')
        data = response.json()
        self.assertIsInstance(data['CarModels'], list)


class RegistrationViewTest(TestCase):
    """Tests for the /djangoapp/register endpoint."""

    def _post(self, payload):
        return self.client.post(
            '/djangoapp/register',
            data=json.dumps(payload),
            content_type='application/json',
        )

    def test_successful_registration(self):
        payload = {
            'userName': 'testuser',
            'password': 'TestPass123!',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test@example.com',
        }
        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['userName'], 'testuser')
        self.assertEqual(data['status'], 'Authenticated')

    def test_duplicate_username_returns_error(self):
        User.objects.create_user(username='existinguser', password='pass')
        payload = {
            'userName': 'existinguser',
            'password': 'AnotherPass1!',
            'firstName': 'A',
            'lastName': 'B',
            'email': 'a@b.com',
        }
        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Already Registered')

    def test_missing_required_fields_returns_400(self):
        payload = {'userName': 'nopassword'}
        response = self._post(payload)
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_returns_400(self):
        response = self.client.post(
            '/djangoapp/register',
            data='not-json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class LoginViewTest(TestCase):
    """Tests for the /djangoapp/login endpoint."""

    def setUp(self):
        User.objects.create_user(username='loginuser', password='Correct1!')

    def _post(self, payload):
        return self.client.post(
            '/djangoapp/login',
            data=json.dumps(payload),
            content_type='application/json',
        )

    def test_valid_credentials_return_authenticated(self):
        response = self._post(
            {'userName': 'loginuser', 'password': 'Correct1!'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'Authenticated')

    def test_wrong_password_does_not_return_authenticated(self):
        response = self._post(
            {'userName': 'loginuser', 'password': 'WrongPass!'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotIn('status', data)

    def test_missing_fields_returns_400(self):
        response = self._post({'userName': 'loginuser'})
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_returns_400(self):
        response = self.client.post(
            '/djangoapp/login',
            data='bad-json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class LogoutViewTest(TestCase):
    """Tests for the /djangoapp/logout endpoint."""

    def test_logout_clears_session(self):
        User.objects.create_user(username='logoutuser', password='Pass1!')
        self.client.login(username='logoutuser', password='Pass1!')
        response = self.client.get('/djangoapp/logout')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['userName'], '')


class AddReviewViewTest(TestCase):
    """Tests for the /djangoapp/add_review endpoint."""

    def test_unauthenticated_request_returns_403(self):
        response = self.client.post(
            '/djangoapp/add_review',
            data=json.dumps({'review': 'Great!'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 403)

    def test_invalid_json_returns_400(self):
        User.objects.create_user(username='reviewer', password='Pass1!')
        self.client.login(username='reviewer', password='Pass1!')
        response = self.client.post(
            '/djangoapp/add_review',
            data='not-json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 400)
