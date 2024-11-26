from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse


class RegisterViewTest(APITestCase):
    @patch('accounts.signals.send_verification_phone')  # Mock the verification task
    def test_register_user_success(self, mock_send_verification):
        url = reverse('accounts:register')  # Adjust this to the actual URL of your RegisterView
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'saida0525',
            'confirm_password': 'saida0525',
            'phone_number': '+998123456789',
            'email': 'johndoe@gmail.com'
        }

        response = self.client.post(url, data, format='json')

        # Check if status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if user is created but inactive
        try:
            user = get_user_model().objects.get(username='johndoe')
            self.assertIsNotNone(user)
            self.assertFalse(user.is_active)  # Ensure the user is not active yet
        except get_user_model().DoesNotExist:
            self.fail('UserModel matching query does not exist')

    @patch('accounts.signals.send_verification_phone')  # Mock the verification task
    def test_password_mismatch(self, mock_send_verification):
        url = reverse('accounts:register')  # Adjust this to the actual URL of your RegisterView
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'password123',
            'confirm_password': 'password124',  # Mismatched password
            'phone_number': '+998123456789',
            'email': 'johndoe@gmail.com',
        }

        response = self.client.post(url, data, format='json')

        # Ensure that the password mismatch raises a validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords must match', response.data['non_field_errors'])

        # Ensure user has not been created due to password mismatch
        # Check if the user exists or not
        user_exists = get_user_model().objects.filter(username='johndoe').exists()
        self.assertFalse(user_exists, "User should not be created when passwords do not match")

    def tearDown(self):
        # Clean up any users or data created during the tests to ensure isolation between tests
        get_user_model().objects.filter(username='johndoe').delete()
        super().tearDown()  # Call the parent class's tearDown to ensure normal cleanup
