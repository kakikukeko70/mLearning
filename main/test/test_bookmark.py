from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Memo, Bookmark, Folder

User = get_user_model()

class BookmarkTests(TestCase):

    @classmethod 
    def setUpTestData(cls):
        user = User.objects.create(username='test', email='test@invalid.com')
        user.set_password('testuserpass')
        user.save()
        memo = Memo.objects.create(memo='', user=user)
        memo.save()
        Folder.objects.create(name='test_folder', user=user)
    
    def test_add_bookmark(self):
        self.client.login(username='test', password='testuserpass')
        data = {'name': 'test_bookmark', 'url': 'valid_url'}
        response = self.client.post('/add_bookmark/1/', data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], '/folder_detail/1/')