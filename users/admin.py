from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User

    # Define which fields should be displayed on the User admin page
    list_display = ("email", "is_staff", "is_superuser", "user_type")
    list_filter = ("is_superuser", "is_staff", "user_type")

    # Specify the fields to be used in detail view and change form
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("second_last_name", "phone")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "user_type")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "user_type",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
