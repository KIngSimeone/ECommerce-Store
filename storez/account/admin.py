from django.contrib import admin

from .models import (
                    User,
                    UserAccessTokens,
                    UserPasswordResetTokens,
                    Manager,
                    ManagerAccessTokens,
                    ManagerPasswordResetTokens,
                    Controller,
                    ControllerAccessTokens,
                    ControllerPasswordResetTokens

)

admin.site.register(User)
admin.site.register(UserAccessTokens)
admin.site.register(UserPasswordResetTokens)
admin.site.register(Manager)
admin.site.register(ManagerAccessTokens)
admin.site.register(ManagerPasswordResetTokens)
admin.site.register(Controller)
admin.site.register(ControllerAccessTokens)
admin.site.register(ControllerPasswordResetTokens)