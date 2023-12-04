from django.contrib import admin

from .models import Branch, Institute, User, Profile

admin.site.register(Institute)
admin.site.register(Profile)
admin.site.register(Branch)
admin.site.register(User)

