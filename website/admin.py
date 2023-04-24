from django.contrib import admin
from website.models import *

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Notification)