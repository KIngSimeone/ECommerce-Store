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
from django.utils import timezone
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
            return None

        # retrieve manager access token record if it exists
        managerAccessTokenRecords = ManagerAccessTokens.objects.filter(manager=manager.id)

        managerAccessTokenRecord = None
        if len(managerAccessTokenRecords) > 0:
            managerAccessTokenRecord = managerAccessTokenrecords[0]
            if managerAccessTokenRecord.expiresAt > timezone.now():

                return managerAccessTokenRecord

        else:
            managerAccessTokenRecord = ManagerAccessTokens(manager=manager)

        managerAccessTokenRecord.accessToken = secrets.token_urlsafe()

        managerAccessTokenRecord.expiresAt = getExpiresAt()

        managerAccessTokenRecord.save()

        return managerAccessTokenRecord

    except Exception as e:
        logger.error("generateManagerAccessToken@Error")
        logger.error(e)
        return None

def generateControllerAccessToken(controller):
    try:
        # confirm that the controller isn't none
        if controller is None:
            return None

        # retrieve controller access token record if it exists
        controllerAccessTokenRecords = ControllerAccessTokens.objects.filter(controller=controller.id)

        controllerAccessTokenRecord = None
        if len(controllerAccessTokenRecords) > 0:
            controllerAccessTokenRecord = controllerAccessTokenRecords[0]
            if controllerAccessTokenRecord.expiresAt > timezone.now():

                return controllerAccessTokenRecord

        else:
            controllerAccessTokenRecord = ControllerAccessTokens(controller=controller)

        controllerAccessTokenRecord.accessToken = secrets.token_urlsafe()

        controllerAccessTokenRecord.expiresAt = getExpiresAt()

        controllerAccessTokenRecord.save()

        return controllerAccessTokenRecord

    except Exception as e:
        logger.error("generateControllerAccessToken@Error")
        logger.error(e)
        return None



def getExpiresAt():
    return (timezone.now() + timedelta(minutes=eval(settings.DURATION)))