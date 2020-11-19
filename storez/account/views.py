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
        # confrim that msanager isn't none
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

# Create User
def createUser(firstName, lastName, userName, email, password, phone):
    try:
        user = User(
            firstName=firstName,
            lastName=lastName,
            userName=userName,
            email=email,
            phone=phone,
    
        )

        # create and store password hash
        hashedPassword = make_password(password)
        user.password = hashedPassword

        user.save()
        return user
    except Exception as err:
        logger.error('createUser@error')
        logger.error(err)
        return None


# Create Manager
def createManager(firstName, lastName, userName, email, password, phone):
    try:
        manager = Manager(
            firstName=firstName,
            lastName=lastName,
            userName=userName,
            email=email,
            phone=phone,
            
        )

        # create and store password hash
        hashedPassword = make_password(password)
        manager.password = hashedPassword

        manager.save()
        return manager
    except Exception as err:
        logger.error('createManager@error')
        logger.error(err)
        return None


# Create Controller
def createController(firstName, lastName, userName, email, password, phone):
    try:
        controller = Controller(
            firstName=firstName,
            lastName=lastName,
            userName=userName,
            email=email,
            phone=phone,
            
        )

        # create and store password hash
        hashedPassword = make_password(password)
        controller.password = hashedPassword

        controller.save()
        return controller
    except Exception as err:
        logger.error('createController@error')
        logger.error(err)
        return None



def getUserByAccessToken(accessToken):
    try:
        userAccessTokenRecord = UserAccessTokens.objects.filter(
            accessToken=accessToken)
        if len(userAccessTokenRecord) > 0:
            userAccessTokenRecord = userAccessTokenRecord[0]
            if userAccessTokenRecord.expiresAt > timezone.now():
                associatedUser = userAccessTokenRecord.user
                if not associatedUser is None and userAccessTokenRecord.expiresAt > timezone.now():

                    associatedUser.lastActiveOn = timezone.now()
                    userAccessTokenRecord.expiresAt = getLastActiveForwarding()

                    userAccessTokenRecord.save()
                    associatedUser.save()

                    return userAccessTokenRecord.user

            return None
        else:
            return None
            
        return None
    except UserAccessTokens.DoesNotExist:
        print('getUserByAccessToken@error')
        return None

def getManagerByAccessToken(accessToken):
    try:
        managerAccessTokenRecord = ManagerAccessTokens.objects.filter(
            accessToken=accessToken)
        if len(managerAccessTokenRecord) > 0:
            managerAccessTokenRecord = managerAccessTokenRecord[0]
            if managerAccessTokenRecord.expiresAt > timezone.now():
                associatedManager = managerAccessTokenRecord.manager
                if not associatedManager is None and managerAccessTokenRecord.expiresAt > timezone.now():

                    associatedManager.lastActiveOn = timezone.now()
                    managerAccessTokenRecord.expiresAt = getLastActiveForwarding()

                    managerAccessTokenRecord.save()
                    associatedManager.save()

                    return userAccessTokenRecord.Manager

            return None
        else:
            return None
            
        return None
    except ManagerAccessTokens.DoesNotExist:
        print('getManagerByAccessToken@error')
        return None


def getControllerByAccessToken(accessToken):
    try:
        controllerAccessTokenRecord = ControllerAccessTokens.objects.filter(
            accessToken=accessToken)
        if len(controllerAccessTokenRecord) > 0:
            controllerAccessTokenRecord = controllerAccessTokenRecord[0]
            if controllerAccessTokenRecord.expiresAt > timezone.now():
                associatedController = controllerAccessTokenRecord.controller
                if not associatedController is None and controllerAccessTokenRecord.expiresAt > timezone.now():

                    associatedController.lastActiveOn = timezone.now()
                    controllerAccessTokenRecord.expiresAt = getLastActiveForwarding()

                    controllerAccessTokenRecord.save()
                    associatedController.save()

                    return userAccessTokenRecord.Controller

            return None
        else:
            return None
            
        return None
    except ControllerAccessTokens.DoesNotExist:
        print('getControllerByAccessToken@error')
        return None

def updateUser(user, firstName, lastName, userName, email, phone, password=None):
    try:
        user.firstName = firstName
        user.lastName = lastName
        user.userName = userName
        user.email = email
        user.phone = phone

        if password:
            hashedPassword = make_password(password)

            user.password = hashedPassword

        user.save()
        return user

    except Exception as err:
        logger.error('updateUser@error')
        logger.error(err)
        return None

def updateManager(manager, firstName, lastName, userName, email, phone, password=None):
    try:
        manager.firstName = firstName
        manager.lastName = lastName
        manager.userName = userName
        manager.email = email
        manager.phone = phone

        if password:
            hashedPassword = make_password(password)

            manager.password = hashedPassword

        manager.save()
        return manager

    except Exception as err:
        logger.error('updateManager@error')
        logger.error(err)
        return None


def updateController(controller, firstName, lastName, userName, email, phone, password=None):
    try:
        controller.firstName = firstName
        controller.lastName = lastName
        controller.userName = userName
        controller.email = email
        controller.phone = phone

        if password:
            hashedPassword = make_password(password)

            controller.password = hashedPassword

        controller.save()
        return controller

    except Exception as err:
        logger.error('updateController@error')
        logger.error(err)
        return None


def getUserByEmail(email):
    try:
        return User.objects.get(email=email)
    except Exception as err:
        logger.error('getUserByEmail@error')
        logger.error(err)
        return None

def getUserByEmailOnly(email):
    try:
        return User.objects.get(email=email)

    except Exception as err:
        logger.error('getUserByEmailOnly@error')
        logger.error(err)
        return None

def getUserByUserName(userName):   
    try:
        return User.objects.get(userName=userName)
    
    except Exception as err:
        logger.error('getUserByUserName@error')
        logger.error(err)
        return None

def getUserById(userId):
    try:
        return User.objects.get(id=userId)

    except Exception as err:
        logger.error('getUserById@error')
        logger.error(err)
        return None

def getUserByPhone(phone):
    try:
        return User.objects.get(phone=phone)

    except Exception as err:
        logger.error('getUserByPhone@error')
        logger.error(err)
        return None

## Manager functions

def getManagerByEmail(email):
    try:
        return Manager.objects.get(email=email)
    except Exception as err:
        logger.error('getManagerByEmail@error')
        logger.error(err)
        return None

def getManagerByEmailOnly(email):
    try:
        return Manager.objects.get(email=email)

    except Exception as err:
        logger.error('getManagerByEmailOnly@error')
        logger.error(err)
        return None

def getManagerByUserName(userName):   
    try:
        return Manager.objects.get(userName=userName)
    
    except Exception as err:
        logger.error('getManagerByUserName@error')
        logger.error(err)
        return None

def getManagerById(userId):
    try:
        return Manager.objects.get(id=userId)

    except Exception as err:
        logger.error('getManagerById@error')
        logger.error(err)
        return None

def getManagerByPhone(phone):
    try:
        return Manager.objects.get(phone=phone)

    except Exception as err:
        logger.error('getManagerByPhone@error')
        logger.error(err)
        return None

## Controller functions

def getControllerByEmail(email):
    try:
        return Controller.objects.get(email=email)
    except Exception as err:
        logger.error('getControllerByEmail@error')
        logger.error(err)
        return None

def getControllerByEmailOnly(email):
    try:
        return Controller.objects.get(email=email)

    except Exception as err:
        logger.error('getControllerByEmailOnly@error')
        logger.error(err)
        return None

def getControllerByUserName(userName):   
    try:
        return Controller.objects.get(userName=userName)
    
    except Exception as err:
        logger.error('getControllerByUserName@error')
        logger.error(err)
        return None

def getControllerById(userId):
    try:
        return Controller.objects.get(id=userId)

    except Exception as err:
        logger.error('getControllerById@error')
        logger.error(err)
        return None

def getControllerByPhone(phone):
    try:
        return Controller.objects.get(phone=phone)

    except Exception as err:
        logger.error('getControllerByPhone@error')
        logger.error(err)
        return None

def getExpiresAt():
    return (timezone.now() + timedelta(minutes=eval(settings.DURATION)))