from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Memo

User = get_user_model()

class TodoTests(TestCase):

    @classmethod 
    def setUpTestData(cls):
        user = User.objects.create(username='test', email='test@invalid.com')
        user.set_password('testuserpass')
        user.save()
        memo = Memo.objects.create(memo='', user=user)
        memo.save()

    def test_add_todo(self):
        self.client.login(username='test', password='testuserpass')
        today = date.today()
        
        data = {'text': ['統計学'], 'deadline': [today]}
        response = self.client.post('/add_todo/', data=data, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(response.status_code, 200)

        data = {'text': ['統計学']}
        response = self.client.post('/add_todo/', data=data, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/error/')
    
    def test_update_todo(self):
        self.client.login(username='test', password='testuserpass')
        user = User.objects.get(username='test')