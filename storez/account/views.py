from django.shortcuts import render
from .models import(
                    User,
                    UserAccessTokens,
                    UserPasswordResetTokens,
                    )
from django.utils import timezone
from datetime import datetime, date, timedelta
from django.conf import settings
from account.userCategoryType import UserCategoryType
from django.contrib.auth.hashers import make_password, check_password

# import bcrypt
import hashlib

import secrets

# import the logging library
import logging

# Create and instance of a logger
logger = logging.getLogger(__name__)



# Create Send Email Function
def sendEmail(email,token):
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        server.login((settings.SERVER_EMAIL),((settings.SERVER_PASSWORD)))
        sender = settings.SERVER_EMAIL
        message = ('\nThe following is your reset email token: ' + str(token))

        server.sendmail(from_addr=sender,to_addrs=(email),msg=message)
    except Exception as e:
        logger.error("sendEmail@Error")
        logger.error(e)
        return None

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


# Create User
def createUser(firstName, lastName, userName, email, password, phone,userCategoryType):
    try:
        user = User(
            firstName=firstName,
            lastName=lastName,
            userName=userName,
            email=email,
            phone=phone,
            userCategoryType = userCategoryType
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

def updateUser(user, firstName, lastName, userName, email, phone, userCategoryType, password=None):
    try:
        user.firstName = firstName
        user.lastName = lastName
        user.userName = userName
        user.email = email
        user.phone = phone
        user.userCategoryType = userCategoryType

        if password:
            hashedPassword = make_password(password)

            user.password = hashedPassword

        user.save()
        return user

    except Exception as err:
        logger.error('updateUser@error')
        logger.error(err)
        return None

def listAllUsers():
    try:
        return User.objects.filter(isDeleted=False)
    except Exception as err:
        logger.error('listAllUsers@error')
        logger.error(err)
        return None

def deleteUser(user):
    # permanent or temporarily delete
    try:
        user.isDeleted = True
        user.save()

        return user
    except Exception as err:
        logger.error('deleteUser@error')
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

def getUserPasswordResetTokenByResetToken(passwordResetToken):
    try:
        userPasswordTokenRecord = UserPasswordResetTokens.objects.filter(
            resetToken=passwordResetToken)
        if len(userPasswordTokenRecord) > 0:
            userPasswordTokenRecord = userPasswordTokenRecord[0]
            currentDateTime = datetime.now().date()
            if currentDateTime <= userPasswordTokenRecord.expiresAt:
                return userPasswordTokenRecord

            return None

        return None
    except UserPasswordResetTokens.DoesNotExist:
        logger.error('getUserByPasswordResetToken@Error')
        logger.error(e)
        return None


def getUserPasswordResetTokenByUserId(userId):
    try:
        userPasswordTokenRecord = UserPasswordResetTokens.objects.filter(user=userId)
        if len(userPasswordTokenRecord) > 0:
            userPasswordTokenRecord = userPasswordTokenRecord[0]
            currentDateTime = datetime.now().date()
            if currentDateTime <= userPasswordTokenRecord.expiresAt:
                return userPasswordTokenRecord

            return None

        return None
    except UserPasswordResetTokens.DoesNotExist:
        logger.error('getUserByPasswordResetToken@Error')
        # logger.error(e)
        return None

def setupUserPasswordResetToken(user):
    try:
        userResetTokenRecord = getUserPasswordResetTokenByUserId(user.id)
        currentDateTime = datetime.now().date()

        if userResetTokenRecord is None:
            userResetTokenRecord = UserPasswordResetTokens(user=user, 
                        resetToken=hashlib.sha256(getHashKey(user).encode('utf-8')).hexdigest(),
                        expiresAt=getExpiresAt()
                        )

            userResetTokenRecord.save()

            return userResetTokenRecord

        if userResetTokenRecord.expiresAt <= currentDateTime:
            userResetTokenRecord.expiresAt = getExpiresAt()
            userResetTokenRecord.save()

            return userResetTokenRecord

        return userResetTokenRecord

    except UserPasswordResetTokens.DoesNotExist:
        logger.error('setupUserPasswordResetToken@Error')
        # logger.error(e)
        return None

        
def resetPassword(user, password):
    try:
        # save the encrypted password
        # salt = bcrypt.gensalt()
        # hashedPassword = bcrypt.hashpw(password, salt)
        # user.password = hashedPassword
        hashedPassword = make_password(password)
        user.password = hashedPassword

        user.save()
        return True
    except Exception as e:
        logger.error('resetPassword@error')
        logger.error(e)
        return False



def getExpiresAt():
    return (timezone.now() + timedelta(minutes=eval(settings.DURATION)))

def getLastActiveForwarding():
    return (timezone.now() + timedelta(minutes=eval(settings.DURATION)))
