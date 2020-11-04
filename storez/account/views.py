from django.shortcuts import render
from .models import(
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
from django.utils import 
from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# import bcrypt
import hashlib

import secrets

# import the logging library
import logging

# Create and instance of a logger
logger = logging.getLogger(__name__)

#Create user authentication function
def authenticateUser(email, password):
    try:
        # retrieve user by email
        user = User.objects.get(email__iexact=email)

        # compare if password hashes are the same
        if check_password(password, user.password):
            user.lastActiveOn = timezone.now()

            user.save()
            return user

        return None

    except User.DoesNotExist:
        return None

def authenticateManager(email, password):
    try:
        # retrieve manager by email
        manager = Manager.objects.get(email__iexact=email)

        # compare if password hashes are the same
        if check_password(password, manager.password):
            manager.lastActiveOn = timezone.now()

            manager.save()
            return manager

        return None

    except Manager.DoesNotExist:
        return None

def authenticateController(email, password):
    try:
        # retrieve controller by email
        controller = Controller.objects.get(email__iexact=email)

        # compare if password hashes are the same
        if check_password(password, controller.password):
            controller.lastActiveOn = timezone.now()

            controller.save()
            return controller

        return None

    except Controller.DoesNotExist:
        return None

def generateUserAccessToken(user):
    try:
        # confirm that the user isn't none
        if user is None:
            return None

        # retrieve user access token record if it exists
        userAccessTokenRecords = UserAccessTokens.objects.filter(user=user.id)

        userAccessTokenRecord = None
        if len(userAccessTokenRecords) > 0:
            userAccessTokenRecord = userAccessTokenRecords[0]
            if userAccessTokenRecord.expiresAt > timezone.now():

                return userAccessTokenRecord

        else:
            userAccessTokenRecord = UserAccessTokens(user=user)

        userAccessTokenRecord.accessToken = secrets.token_urlsafe()

        userAccessTokenRecord.expiresAt = getExpiresAt()

        userAccessTokenRecord.save()

        return userAccessTokenRecord

    except Exception as e:
        logger.error("generateUserAccessToken@Error")
        logger.error(e)
        return None


def generateManagerAccessToken(manager):
    try:
        # confrim that manager isn't none
        if manager is None:
            return None:

        # retrieve manager access token record it ir exists
        managerAccessTokenRecords = ManagerAccessTokens






def getExpiresAt():
    return (timezone.now() + timedelta(minutes=eval(settings.DURATION)))