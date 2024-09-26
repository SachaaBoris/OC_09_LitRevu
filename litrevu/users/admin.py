from django.contrib import admin
from users.models import CustomUser, UserFollows


admin.site.register(CustomUser)
admin.site.register(UserFollows)
