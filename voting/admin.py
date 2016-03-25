from django.contrib import admin

from voting.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'voter_id', 'casted_vote', 'is_staff')
    search_fields = ['voter_id']

admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
