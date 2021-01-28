import os
import json
from django.conf import settings
from django.http import HttpResponse

from account.views import (
                           createUser as createUserRecord,
                           updateUser as updateUserRecord,
                           deleteUser as deleteUserRecord,
                           getUserByUserName,
                           getUserByEmail,
                           getUserByPhone,
                           getUserByAccessToken,
                           getUserById,
                           listAllUsers,
                           resetPassword,
                           getUserPasswordResetTokenByResetToken
                          )
                           
from account.userCategoryType import UserCategoryType
from wallet.views import (
                          createUserAccount,
                         )

from apiutility.responses import (
                                  unAuthorizedResponse,
                                  unAuthenticatedResponse,
                                  badRequestResponse,
                                  resourceConflictResponse,
                                  successResponse,
                                  resourceNotFoundResponse,
                                  paginatedResponse,
                                  internalServerErrorResponse
                )

from apiutility.validators import (
                                  validateEntry,
                                  validateKeys, 
                                  validateEmailFormat,
                                  validatePhoneFormat,
                                  validateThatAStringIsClean,
                                  validateThatStringIsEmptyAndClean,
                                  validateThatStringIsEmpty    
                                 )

from error.errorCodes import (
                              ErrorCodes,
                              getGenericInvalidParametersErrorPacket,
                              getUserAlreadyExistErrorPacket,
                              getUserCreationFailedErrorPacket,
                              getUnauthenticatedErrorPacket,
                              getUnauthorizedErrorPacket,
                              getUserDoesNotExistErrorPacket,
                              getUserUpdateFailedErrorPacket,
                              getUserCategoryInvalidErrorPacket,
                              getPasswordResetFailedErrorPacket,
                             )

from dataTransformer.jsonTransformer import transformUser,transformUsersList
from django.core.paginator import Paginator
                                            

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# handles "/users/" endpoint requests
def userAccountRouter(request):
    if request.method == "GET":
        return getAllUsers(request)

    elif request.method == "POST":
        return createUser(request)

# handles "/users/<int:userID>/" requests
def singleUserAccountRouter(request, userID):
    if request.method == "GET":
        return getUser(request, userID)

    elif request.method == "PUT":
        return updateUser(request, userID)

# handles "/users/<int:userID>/delete/" requests
def deleteUserAccountRouter(request, userID):
    if request.method == "DELETE":
        return deleteUser(request, userID)

# handles "/users/resetpassword/" requests
def passwordResetRouter(request):
    if request.method == "POST":
        return passwordReset(request)
"""

# Create User
def createUser(request):
    # get Json information passed in
    body = json.loads(request.body)

    #check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=[
                                'firstName','lastName','email','phone','userName','userCategoryType','password'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
        

    #validate if the email is in the correct format
    if not validateEmailFormat(body['email']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

    #validate if the phone is in the correct formats
    if not validatePhoneFormat(body['phone']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Phone format is invalid"))

    if not validateThatStringIsEmptyAndClean(body['firstName']):
       return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket( "First name cannot be empty or contain special characters"))

    if not validateThatStringIsEmptyAndClean(body['lastName']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Last name cannot be empty or contain special characters"))

    if not validateThatStringIsEmpty(body['password']):
        return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                    message=getGenericInvalidParametersErrorPacket("Password cannot be empty"))

    #check if user with that username exists
    if getUserByUserName(body['userName']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('username'))

    #check if user with that email exists
    if getUserByEmail(body['email']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('email'))

    #Check if user with that phone exists
    if getUserByPhone(body['phone']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('phone'))

    # check that the user category type specified is correct
    confirmedUserCategoryTypeValidity = False
    for categoryType in UserCategoryType:
        if categoryType.value == body['userCategoryType'].lower():
            confirmedUserCategoryTypeValidity = True
            userCategoryType = categoryType.value

    if not confirmedUserCategoryTypeValidity:
        return badRequestResponse(errorCode=ErrorCodes.USER_CATEGORY_TYPE_INVALID,
                                message=getUserCategoryInvalidErrorPacket())

    createdUser = createUserRecord(firstName=body['firstName'],lastName=body['lastName'],
                                    userName=body['userName'], email=body['email'],
                                    password=body['password'], phone=body['phone'],
                                    userCategoryType=body['userCategoryType']
                                )

    if createdUser == None:
        return internalServerErrorResponse(ErrorCodes.USER_CREATION_FAILED,
                                            message=getUserCreationFailedErrorPacket())
    createAccount = createUserAccount(user=createdUser)

    return successResponse(message="successfully created user", body=transformUser(createdUser))
"""
# update user
def updateUser(request, userID):
    # verify that the calling user has a valid token
    body = json.loads(request.body)
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")
   
    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                       message=getUnauthenticatedErrorPacket())

    # validate to ensure that all required fields are present
    if 'password' in body:
        keys = ['email', 'userName', 'firstName',
                 'lastName', 'password', 'phone', 'userCategoryType']

    else:
        keys = ['email', 'userName', 'firstName',
                 'lastName', 'phone', 'userCategoryType']

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=keys)
    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")

    # check if userToBeUpdated already exists
    userToBeUpdated = getUserById(userID)
    if userToBeUpdated is None:
        return resourceNotFoundResponse(ErrorCodes.USER_DOES_NOT_EXIST, getUserDoesNotExistErrorPacket())

    # validate if the email is in the correct format
    if not validateEmailFormat(body['email']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

    # validate if the phone is in the correct format
    if not validatePhoneFormat(body['phone']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Phone format is invalid"))

    if not validateThatStringIsEmptyAndClean(body['firstName']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket( "First name cannot be empty or contain special characters"))

    if not validateThatStringIsEmptyAndClean(body['lastName']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Last name cannot be empty or contain special characters"))
    
    # check that the user category type specified is correct
    confirmedUserCategoryTypeValidity = False
    for categoryType in UserCategoryType:
        if categoryType.value == body['userCategoryType'].lower():
            confirmedUserCategoryTypeValidity = True
            userCategoryType = categoryType.value

    if not confirmedUserCategoryTypeValidity:
        return badRequestResponse(errorCode=ErrorCodes.USER_CATEGORY_TYPE_INVALID,
                                message=getUserCategoryInvalidErrorPacket())

    # check that username specified does not belong to another user
    userName = getUserByUserName(
        userName=body['userName'])
    if userName != None:
        if userName.id != userToBeUpdated.id:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                            message=getUserAlreadyExistErrorPacket(value="username"))

    # check that email specified does not belong to another user
    userEmail = getUserByEmail(body['email'])
    if userEmail != None:
        if userEmail.id != userToBeUpdated.id:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                            message=getUserAlreadyExistErrorPacket(value="email"))
                                                                                                                                                                                                                                                                                                                     
    # check that phone specified does not belong to another user
    userPhone = getUserByPhone(phone=body['phone'])
    if userPhone != None: 
        if userPhone.id != userToBeUpdated.id:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                            message=getUserAlreadyExistErrorPacket(value="phone"))


        if 'password' in body:
            updatedUser = updateUserRecord(userToBeUpdated, firstName=body['firstName'], lastName=body['lastName'],
                                        userName=body['userName'], email=body['email'],
                                        password=body['password'], phone=body['phone'], userCategoryType=body['userCategoryType']
                                        )

        else:
            updatedUser = updateUserRecord(userToBeUpdated, firstName=body['firstName'], lastName=body['lastName'],
                                        userName=body['userName'], email=body['email'],
                                        phone=body['phone'], userCategoryType=body['userCategoryType']
                                    )
    
    if updatedUser == None:
        return internalServerErrorResponse(ErrorCodes.USER_UPDATE_FAILED,
                                           message=getUserUpdateFailedErrorPacket())
    return successResponse(message="successfully updated user", body=transformUser(updatedUser))

def getAllUsers(request):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST, message=getUnauthenticatedErrorPacket())
    
    #Check if user has the privilege to read the resource
    if user.userCategoryType != 'controller':
        return unAuthorizedResponse(ErrorCodes.UNAUTHORIZED_REQUEST, message=getUnauthorizedErrorPacket())

    # retrieve a list of all users
    allUsersList = listAllUsers()

    # Paginate the retrieved users
    if request.GET.get('pageBy'):
        pageBy = request.GET.get('pageBy')
    else:
        pageBy = 10

    paginator = Paginator(allUsersList, pageBy)

    if request.GET.get('page'):
        pageNum = request.GET.get('page')
    else:
        pageNum = 1
    
    # try if the page requested exists or is empty
    try:
        paginated_UsersList = paginator.page(pageNum)

        paginationDetails = {
            "totalPages": paginator.num_pages,
            "limit": pageBy,
            "currentPage": pageNum
        }
    except Exception as e:
        print(e)
        paginated_UsersList = []
        paginationDetails = {}

    return paginatedResponse(message="successfully retrieved users", 
                            body=transformUsersList(paginated_UsersList), 
                            pagination=paginationDetails
                        )

def getUser(request, userID):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)
    
    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST, message=getUnauthenticatedErrorPacket())
    
    #check if the user exists and retrieve
    userToBeRetrieved = getUserById(userID)
    if userToBeRetrieved == None:
        return resourceNotFoundResponse(ErrorCodes.USER_DOES_NOT_EXIST,
                                        message=getUserDoesNotExistErrorPacket())

    return successResponse(message="successfully retrieved user", body=transformUser(userToBeRetrieved))

def deleteUser(request, userID):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                       message=getUnauthenticatedErrorPacket())
    
    # check is UserID exists
    userToBeDeleted = getUserById(userID)
    
    if userToBeDeleted == None:
        return resourceNotFoundResponse(ErrorCodes.USER_DOES_NOT_EXIST,
                                        message=getUserDoesNotExistErrorPacket())
    
    # check if user has the privileges to delete the resource
    if user.userCategoryType != 'controller' or user != userToBeDeleted:
        return unAuthorizedResponse(ErrorCodes.UNAUTHORIZED_REQUEST, message=getUnauthorizedErrorPacket())

    userDeleted = deleteUserRecord(userToBeDeleted)
    if userDeleted is None:
        return internalServerErrorResponse(ErrorCodes.USER_DELETION_FAILED,
                                            message=getUserDeletionFailedErrorPacket())

    return successResponse(message="Successfully deleted user", body={})

def passwordReset(request):
    body = json.loads(request.body)

    # check if required fields are present in request payload
    missingKeys = validateKeys(
        payload=body, requiredKeys=['token', 'password'])
    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")

    userPasswordResetToken = getUserPasswordResetTokenByResetToken(body['token'])
    if userPasswordResetToken is None:
        return badRequestResponse(ErrorCodes.GENERIC_INVALID_PARAMETERS, message=getGenericInvalidParametersErrorPacket(0, "invalid reset token"))

    # reset user's password
    password = body['password']
    passwordReset = resetPassword(userPasswordResetToken.user, password)
    if passwordReset == False:
        return internalServerErrorResponse(ErrorCodes.PASSWORD_RESET_FAILED,
                                           message=getPasswordResetFailedErrorPacket())

    return successResponse(message="Password Reset was successful")





"""
# Create User
def createUser(request):
    # get Json information passed in
    body = json.loads(request.body)

    #check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=['users'])

    users = body['users']

    for user in users:

        # check if required fields are present in request payload
        missingKeys = validateKeys(payload=users, requiredKeys=[
                                'firstName','lastName','email','phone','userName','userCategoryType','password'])

        if missingKeys:
            return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
            

        #validate if the email is in the correct format
        if not validateEmailFormat(body['email']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                    message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

        #validate if the phone is in the correct formats
        if not validatePhoneFormat(body['phone']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                    message=getGenericInvalidParametersErrorPacket("Phone format is invalid"))

        if not validateThatStringIsEmptyAndClean(body['firstName']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                    message=getGenericInvalidParametersErrorPacket( "First name cannot be empty or contain special characters"))

        if not validateThatStringIsEmptyAndClean(body['lastName']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                    message=getGenericInvalidParametersErrorPacket("Last name cannot be empty or contain special characters"))

        if not validateThatStringIsEmpty(body['password']):
            return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                        message=getGenericInvalidParametersErrorPacket("Password cannot be empty"))

        #check if user with that username exists
        if getUserByUserName(body['userName']) is not None:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                            message=getUserAlreadyExistErrorPacket('username'))

        #check if user with that email exists
        if getUserByEmail(body['email']) is not None:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                            message=getUserAlreadyExistErrorPacket('email'))

        #Check if user with that phone exists
        if getUserByPhone(body['phone']) is not None:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                            message=getUserAlreadyExistErrorPacket('phone'))

        # check that the user category type specified is correct
        confirmedUserCategoryTypeValidity = False
        for categoryType in UserCategoryType:
            if categoryType.value == body['userCategoryType'].lower():
                confirmedUserCategoryTypeValidity = True
                userCategoryType = categoryType.value

        if not confirmedUserCategoryTypeValidity:
            return badRequestResponse(errorCode=ErrorCodes.USER_CATEGORY_TYPE_INVALID,
                                    message=getUserCategoryInvalidErrorPacket())

        createdUsers = createUserRecord(firstName=user['firstName'],lastName=user['lastName'],
                                        userName=user['userName'], email=user['email'],
                                        password=user['password'], phone=user['phone'],
                                        userCategoryType=user['userCategoryType']
                                    )

        if createdUsers == None:
            return internalServerErrorResponse(ErrorCodes.USER_CREATION_FAILED,
                                                message=getUserCreationFailedErrorPacket())
        createAccount = createUserAccount(user=createdUsers)

        return successResponse(message="successfully created users", body=transformUser(createdUsers))

"""

# Create User
def createUser(request):
    # get Json information passed in
    body = json.loads(request.body)
    
    #check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=['users'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
    
    
    users = body['users']
    for user in users:

        index= users.index
        fields = ['firstName','lastName','userName','email','phone','password','userCategoryType']
    
        #check if required fields are present in request payload
        missingKeys = validateKeys(payload=user, requiredKeys=fields)

        if missingKeys:
            return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys} for {index(user)}")

        #validate if the email is in the correct format
        if not validateEmailFormat(user['email']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

        #validate if the phone is in the correct formats
        if not validatePhoneFormat(user['phone']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Phone format is invalid"))

        if not validateThatStringIsEmptyAndClean(user['firstName']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket( "First name cannot be empty or contain special characters"))

        if not validateThatStringIsEmptyAndClean(user['lastName']):
            return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Last name cannot be empty or contain special characters"))

        if not validateThatStringIsEmpty(user['password']):
            return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                    message=getGenericInvalidParametersErrorPacket("Password cannot be empty"))

        #check if user with that username exists
        if getUserByUserName(user['userName']) is not None:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('username'))

        #check if user with that email exists
        if getUserByEmail(body['email']) is not None:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('email'))

        #Check if user with that phone exists
        if getUserByPhone(body['phone']) is not None:
            return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('phone'))

        # check that the user category type specified is correct
        confirmedUserCategoryTypeValidity = False
        for categoryType in UserCategoryType:
            if categoryType.value == body['userCategoryType'].lower():
                confirmedUserCategoryTypeValidity = True
                userCategoryType = categoryType.value

    return HttpResponse("Success")

    """
    #validate if the email is in the correct format
    if not validateEmailFormat(body['email']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

    #validate if the phone is in the correct formats
    if not validatePhoneFormat(body['phone']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Phone format is invalid"))

    if not validateThatStringIsEmptyAndClean(body['firstName']):
       return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket( "First name cannot be empty or contain special characters"))

    if not validateThatStringIsEmptyAndClean(body['lastName']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Last name cannot be empty or contain special characters"))

    if not validateThatStringIsEmpty(body['password']):
        return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                    message=getGenericInvalidParametersErrorPacket("Password cannot be empty"))

    #check if user with that username exists
    if getUserByUserName(body['userName']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('username'))

    #check if user with that email exists
    if getUserByEmail(body['email']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('email'))

    #Check if user with that phone exists
    if getUserByPhone(body['phone']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('phone'))

    # check that the user category type specified is correct
    confirmedUserCategoryTypeValidity = False
    for categoryType in UserCategoryType:
        if categoryType.value == body['userCategoryType'].lower():
            confirmedUserCategoryTypeValidity = True
            userCategoryType = categoryType.value

    if not confirmedUserCategoryTypeValidity:
        return badRequestResponse(errorCode=ErrorCodes.USER_CATEGORY_TYPE_INVALID,
                                message=getUserCategoryInvalidErrorPacket())

    createdUser = createUserRecord(firstName=body['firstName'],lastName=body['lastName'],
                                    userName=body['userName'], email=body['email'],
                                    password=body['password'], phone=body['phone'],
                                    userCategoryType=body['userCategoryType']
                                )

    if createdUser == None:
        return internalServerErrorResponse(ErrorCodes.USER_CREATION_FAILED,
                                            message=getUserCreationFailedErrorPacket())
    createAccount = createUserAccount(user=createdUser)

    return successResponse(message="successfully created user", body=transformUser(createdUser))
    """