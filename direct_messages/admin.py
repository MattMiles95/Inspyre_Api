from django.contrib import admin
from .models import Conversation, DirectMessage

admin.site.register(Conversation)
admin.site.register(DirectMessage)
