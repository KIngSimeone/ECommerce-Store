from django.contrib import admin

from .models import (
                    User,
                    UserAccessTokens,
                    UserPasswordResetTokens,
)
admin.site.register(User)
admin.site.register(UserAccessTokens)
admin.site.register(UserPasswordResetTokens)
