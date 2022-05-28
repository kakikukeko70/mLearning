from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Memo

User = get_user_model()

class TestUserTests(TestCase):

    @classmethod 
    def setUpTestData(cls):
        user = User.objects.create(username='test', email='test@invalid.com')
        user.set_password('testuserpass')
        user.save()
        memo = Memo.objects.create(memo='', user=user)
        memo.save()

    def test_not_allowed(self):
        self.client.login(username='test', password='testuserpass')
        user = User.objects.get(username='test')

        response = self.client.get(f'/change_username/{user.id}/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')

        response = self.client.get(f'/delete_account/{user.id}/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')

        response = self.client.get(f'/password_change/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')

        response = self.client.get('/password_reset/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')