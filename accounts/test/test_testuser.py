from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Memo

User = get_user_model()

class TestUserTests(TestCase):

    @classmethod 
    def setUpTestData(cls):
        testuser = User.objects.create(username='test', email='test@invalid.com')
        testuser.set_password('testuser')
        testuser.save()
        memo = Memo.objects.create(memo='', user=testuser)
        memo.save()
    
    def test_testuser_login(self):
        response = self.client.get('/testuser_login/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/')
        
    def test_not_allowed(self):
        self.client.get('/testuser_login/')
        user = User.objects.get(username='test')

        response = self.client.get(f'/change_username/{user.id}/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')

        response = self.client.get(f'/delete_account/{user.id}/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')

        response = self.client.get(f'/password_change/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')

        response = self.client.get('/password_reset/')
        self.assertEqual(response.template_name[0], 'accounts/testuser_not_allowed.html')
