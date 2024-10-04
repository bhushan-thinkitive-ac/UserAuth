from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ["id", "first_name", "last_name", "email","age", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "date_of_birth", "phone", "address"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["first_name", "last_name", "date_of_birth", "email", "phone","address", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "id", "first_name", "last_name"]
    ordering = ["id"]
    filter_horizontal = []
    def get_readonly_fields(self, request, obj=None):
        if obj:  # When editing an existing user
            return ["age"]
        return []

# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
