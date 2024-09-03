from django.contrib import admin

from .models import Branch, Institute, User, Profile

admin.site.register(Institute)
admin.site.register(Profile)
admin.site.register(Branch)
# admin.site.register(User)

@admin.action(description='Deactivate selected users')
def deactivate_user(model_admin, request, queryset):
    queryset.update(is_active=False)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','full_name','role')
    search_fields = ('email',)
    list_filter = ('role',)
    actions = [deactivate_user]

    def full_name(self, instance):
        return f'{instance.first_name} {instance.last_name}'
