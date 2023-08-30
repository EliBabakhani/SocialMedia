from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('slug','created_at', 'id')
    search_fields=['slug']
    prepopulated_fields={'slug': ('body',)}
    list_filter=('user','created_at')



