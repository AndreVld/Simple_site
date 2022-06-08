from django.contrib import admin

# Register your models here.
from .models import Info, Post, Tag, Certificates

admin.site.register(Info)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Certificates)