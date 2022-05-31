from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Memo, Folder

User = get_user_model()

class FolderTests(TestCase):

    @classmethod 
    def setUpTestData(cls):
        user = User.objects.create(username='test', email='test@invalid.com')
        user.set_password('testuserpass')
        user.save()
        memo = Memo.objects.create(memo='', user=user)
        memo.save()

    def test_add_folder(self):
        self.client.login(username='test', password='testuserpass')
        data = {'name': 'test_folder'}
        response = self.client.post('/create_folder/', data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], '/bookmark_folders/')