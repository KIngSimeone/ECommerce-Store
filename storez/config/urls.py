"""storez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from workflows.tokenReset_workflow import resetTokenURLRouter, validateTokenURLRouter
from workflows.authentication_workflow import (
                                               authenticationRouter
                                              )
from workflows.userAccount_workflow import (
                                            userAccountRouter,
                                            singleUserAccountRouter,
                                            deleteUserAccountRouter,
                                            passwordResetRouter
                                            )

from workflows.business_workflow import (
                                  userBusinessRouter
                                 )



urlpatterns = [
    path('admin/', admin.site.urls),

    # authentication endpoints
    path('authenticate/',authenticationRouter,name="userauthentication-router"),

    # account-related endpoints
    path('users/', userAccountRouter, name="user-Router"),
    path('users/<int:userID>/', singleUserAccountRouter, name="singleUserAccount-router"),
    path('users/<int:userID>/delete/', deleteUserAccountRouter, name="deleteUserAccount-router"),
    path('users/passwordreset/', passwordResetRouter, name="passwordReset-router"),

        # reset password endpoints
    path('resettoken/', resetTokenURLRouter, name="resetTokenURL-router"),
    path('validatetoken/', validateTokenURLRouter, name="validateTokenURL-router"),

    # business endpoints
    path('business/', userBusinessRouter, name="business-Router")
]
