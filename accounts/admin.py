from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


# Inline profile editor shown within User admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


# Extend default User admin to include Profile
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_select_related = ("profile",)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Unregister the original User admin, then re-register with our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Optionally register Profile separately (useful for search/filter)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "country", "city", "phone")
    search_fields = ("full_name", "user__email", "country", "city", "phone")
    list_filter = ("country", "city")
