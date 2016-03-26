from django.contrib import admin

from voting.models import CustomUser, Party


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'voter_id', 'casted_vote', 'is_staff')
    search_fields = ['voter_id']

    def has_add_permission(self, request):
        return False


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Party)


# Register your models here.
