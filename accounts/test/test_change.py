from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Memo

User = get_user_model()

class UserTests(TestCase):

    @classmethod 
    def setUpTestData(cls):
        testuser = User.objects.create(username='test', email='test@invalid.com')
        testuser.set_password('testuser')
        testuser.save()
        memo = Memo.objects.create(memo='', user=testuser)
        memo.save()
