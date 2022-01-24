from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Import Models
from .models import Loan, Gender
from users.models import User
# Import service
from .api.services import LoanApproval


# Loan ViewSet Test Case
class LoanViewSetTestCase(APITestCase):

    fixtures = ['genders.json']
    list_url = reverse('loansapi:new_loan-list')

    # Method to get loan status from service
    def get_loan_status(self):
        stat = LoanApproval().get_loan_approval(38522474)
        if stat:
            return True
        else:
            return False

    def setUp(self):
        # Create Users to use later
        self.user = User.objects.create(
            username='normal',
            email='normal@mail.com',
            name='name',
            last_name='surname',
            password='1234',
            )

        self.userStaff = User.objects.create(
            username='staff',
            email='staff@mail.com',
            name='name',
            last_name='surname',
            password='1234',
            is_staff=True
            )

        self.userSuper = User.objects.create(
            username='superuser',
            email='super@mail.com',
            name='name',
            last_name='surname',
            password='1234',
            is_superuser=True
            )

        # Create loan
        self.test_loan = Loan.objects.create(
            name='Luis',
            last_name='Suarez',
            email='luicho@gmail.com',
            gender=Gender.objects.get(gender_name='Masculino'),
            dni=38522474,
            amount=4000,
            status=self.get_loan_status()
        )

    # Test Loan Status
    def test_status(self):
        self.assertIsInstance(self.test_loan.status, bool)

    # Test Loan Creation
    def test_loan_creation(self):
        self.assertEqual(Loan.objects.count(), 1)

    # Create test
    def test_loan_create(self):
        data = {
            "dni": 38522474,
            "name": "Luis",
            "last_name": "Suarez",
            "email": "luicho@gmail.com",
            "gender": 2,
            "amount": 4000
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 2)

    # Listing tests w/ different users
    def test_loan_list_wouser(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_loan_list_nuser(self):
        self.client.force_authenticate(user=self.user)
        # User W/O staff or superuser permissions
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loan_list_staff(self):
        self.client.force_authenticate(user=self.userStaff)
        # User W/ staff permissions
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loan_list_super(self):
        self.client.force_authenticate(user=self.userSuper)
        # User W/ superuser permissions
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieving tests w/ different users
    def test_loan_retrieve_nuser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('loansapi:new_loan-detail',
                                           kwargs={'pk': self.test_loan.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loan_retrieve_staff(self):
        self.client.force_authenticate(user=self.userStaff)
        response = self.client.get(reverse('loansapi:new_loan-detail',
                                           kwargs={'pk': self.test_loan.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test data in the response
        self.assertEqual(response.data['name'], 'Luis')

    def test_loan_retrieve_super(self):
        self.client.force_authenticate(user=self.userSuper)
        response = self.client.get(reverse('loansapi:new_loan-detail',
                                           kwargs={'pk': self.test_loan.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Update test w/ superuser
    def test_loan_update(self):
        # This method is not authorized the choice of user is irrelevant
        self.client.force_authenticate(user=self.userSuper)
        response = self.client.put(
            reverse('loansapi:new_loan-detail',
                    kwargs={'pk': self.test_loan.id}),
            {'amount': 5000}
            )
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    # Delete test w/ different users
    def test_loan_delete_nuser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('loansapi:new_loan-detail',
                    kwargs={'pk': self.test_loan.id})
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loan_delete_staff(self):
        self.client.force_authenticate(user=self.userStaff)
        response = self.client.delete(
            reverse('loansapi:new_loan-detail',
                    kwargs={'pk': self.test_loan.id})
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_loan_delete_super(self):
        self.client.force_authenticate(user=self.userSuper)
        response = self.client.delete(reverse('loansapi:new_loan-detail',
                                      kwargs={'pk': self.test_loan.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Test DB, should be 1 loan remaining
        self.assertEqual(Loan.objects.count(), 1)
