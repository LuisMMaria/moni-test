from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Import Models
from .models import User


# User Test Case
class UserViewSetTestCase(APITestCase):

    list_url = reverse('usersapi:users-list')

    def setUp(self):
        # Create User
        self.user = User.objects.create(
            username='luisuarez',
            email='luicho@gmail.com',
            name='Luis',
            last_name='Suarez',
            password='1234',
            is_staff=True,
            is_superuser=True
            )

    # Test User Creation
    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)

    # Test Token Creation
    def test_token_creation(self):
        self.assertEqual(Token.objects.count(), 1)

    # Create User Test
    def test_user_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "name": "Test",
            "last_name": "Testing",
            "password": "1234",
            "is_staff": True,
            "is_superuser": False
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    # Listing tests w/ different users
    def test_user_list_wouser(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_super(self):
        self.client.force_authenticate(user=self.user)
        # User W/O staff or superuser permissions
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieving tests w/ different users
    def test_user_retrieve_nuser(self):
        response = self.client.get(
            reverse('usersapi:users-detail',
                    kwargs={'pk': self.user.id})
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_retrieve_super(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('usersapi:users-detail',
                    kwargs={'pk': self.user.id})
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test data in the response
        self.assertEqual(response.data['username'], 'luisuarez')

    # Update test w/ superuser
    def test_user_update(self):
        self.client.force_authenticate(user=self.user)
        # Incomplete PUT
        response = self.client.put(
            reverse('usersapi:users-detail',
                    kwargs={'pk': self.user.id}),
            {'name': 'Luisillo'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # PATCH
        response = self.client.patch(
            reverse('usersapi:users-detail',
                    kwargs={'pk': self.user.id}),
            {'name': 'Luisillo'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Data updated
        self.assertEqual(response.data[1]['name'], 'Luisillo')
        # Complete PUT
        data = {
            "username": "luisuarez",
            "email": "luicho@gmail.com",
            "name": "Luisillo",
            "last_name": "Villar",
            "password": "1234"
        }
        response = self.client.put(
            reverse('usersapi:users-detail',
                    kwargs={'pk': self.user.id}),
            data
        )
        # Test data
        self.assertEqual(response.data[1]['last_name'], 'Villar')

    # Delete test w/ different users
    def test_user_delete_nuser(self):
        # W/O user
        response = self.client.delete(
            reverse('usersapi:users-detail',
                    kwargs={'pk': self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_delete_super(self):
        # Super User
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('usersapi:users-detail',
                    kwargs={'pk': self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Test DB, should be 1 user remaining
        self.assertEqual(User.objects.count(), 1)
