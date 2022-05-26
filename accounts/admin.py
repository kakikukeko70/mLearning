from django.contrib import admin
from .models import User, Memo, Folder, Bookmark, Todo

# Register your models here.
admin.site.register(User)
admin.site.register(Memo)
admin.site.register(Folder)
admin.site.register(Bookmark)
admin.site.register(Todo)