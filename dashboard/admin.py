from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event, Tutor, Video

# Register your models here.

admin.site.register(Event)
admin.site.register(Tutor)
admin.site.register(Video)
admin.site.register(User, UserAdmin)