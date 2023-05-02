from django.contrib import admin
from .models import Plan, Image



admin.site.register(Plan)
admin.site.site_header = "Disco Admin"
admin.site.site_title = "Disco Admin Portal"
admin.site.index_title = "Welcome to Disco Admin Portal"
# admin.site.register(Image)

