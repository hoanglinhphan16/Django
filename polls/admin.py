from django.contrib import admin

from .models.question import Question
from .models.choice import Choice

admin.site.register(Question)
# Register your models here.
admin.site.register(Choice)
