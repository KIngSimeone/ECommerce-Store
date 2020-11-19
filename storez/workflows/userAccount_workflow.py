import os
import json
from django.conf import settings

from account.views import (
                           createUser as createUserRecord,
                           createManager as createManagerRecord,
                           createController as createControllerRecord,
                           getUserByUserName,
                           getUserByEmail,
                           getUserByPhone,
                           getManagerByUserName,
                           getManagerByEmail,
                           getManagerByPhone,
                           getControllerByUserName,
                           getControllerByEmail,
                           getControllerByPhone,
                           getUserByAccessToken,
                           getUserById,
                          )
                           
from wallet.views import (
                          createUserAccount,
                          createManagerAccount,
                          createControllerAccount
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
                              getUserDoesNotExistErrorPacket,
                              getUserUpdateFailedErrorPacket
                             )
from dataTransformer.jsonTransformer import (
                                            transformUser,
                                            transformManager,
                                            transformController
                                            )

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# handles "/users/" endpoint requests
def userAccountRouter(request):
    if request.method == "POST":
        return createUser(request)

# handles "/managers/" endpoint requests
def managerAccountRouter(request):
    if request.method == "POST":
        return createManager(request)

# handles "/controllers/" endpoint requests
def controllerAccountRouter(request):
    if request.method == "POST":
        return createController(request)



# Create User
def createUser(request):
    # get Json information passed in
    body = json.loads(request.body)

    #check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=[
                                'firstName','lastName','email','phone','userName','password'])

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


    createdUser = createUserRecord(firstName=body['firstName'],lastName=body['lastName'],
                                    userName=body['userName'], email=body['email'],
                                    password=body['password'], phone=body['phone'],
                                )

    if createdUser == None:
        return internalServerErrorResponse(ErrorCodes.USER_CREATION_FAILED,
                                            message=getUserCreationFailedErrorPacket())
    createAccount = createUserAccount(user=createdUser)

    return successResponse(message="successfully created user", body=transformUser(createdUser))


# Create Manager
def createManager(request):
    # get Json information passed in
    body = json.loads(request.body)

    #check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=[
                                'firstName','lastName','email','phone','userName','password'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
        

    #validate if the email is in the correct format
    if not validateEmailFormat(body['email']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

    #validate if the phone is in the correct format
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

    #check if manager with that username exists
    if getManagerByUserName(body['userName']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('username'))

    #check if manager with that email exists
    if getManagerByEmail(body['email']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('email'))

    #Check if user with that phone exists
    if getManagerByPhone(body['phone']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('phone'))


    createdManager = createManagerRecord(firstName=body['firstName'],lastName=body['lastName'],
                                    userName=body['userName'], email=body['email'],
                                    password=body['password'], phone=body['phone'],
                                )

    if createdManager == None:
        return internalServerErrorResponse(ErrorCodes.USER_CREATION_FAILED,
                                            message=getUserCreationFailedErrorPacket())
    createAccount = createManagerAccount(manager=createdManager)

    return successResponse(message="successfully created manager", body=transformManager(createdManager))


# Create Controller
def createController(request):
    # get Json information passed in
    body = json.loads(request.body)

    #check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=[
                                'firstName','lastName','email','phone','userName','password'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
        

    #validate if the email is in the correct format
    if not validateEmailFormat(body['email']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

    #validate if the phone is in the correct format
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

    #check if controller with that username exists
    if getControllerByUserName(body['userName']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('username'))

    #check if controller with that email exists
    if getControllerByEmail(body['email']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('email'))

    #Check if controller with that phone exists
    if getControllerByPhone(body['phone']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST,
                                        message=getUserAlreadyExistErrorPacket('phone'))


    createdController = createControllerRecord(firstName=body['firstName'],lastName=body['lastName'],
                                    userName=body['userName'], email=body['email'],
                                    password=body['password'], phone=body['phone'],
                                )

    if createdController == None:
        return internalServerErrorResponse(ErrorCodes.USER_CREATION_FAILED,
                                            message=getUserCreationFailedErrorPacket())
    createAccount = createControllerAccount(controller=createdController)

    return successResponse(message="successfully created controller", body=transformController(createdController))



# update user
def updateUser(request, userID):
    # verify that the calling user has a valid token
    body = json.loads(request.body)
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                       message=getUnauthenticatedErrorPacket())

    # validate to ensure that all required fields are present
    if 'password' in body:
        keys = ['email', 'userName', 'firstName',
                 'lastName', 'password', 'phone']

    else:
        keys = ['email', 'userName', 'firstName',
                 'lastName', 'phone']

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
                                        password=body['password'], phone=body['phone']
                                        )

        else:
            updatedUser = updateUserRecord(userToBeUpdated, firstName=body['firstName'], lastName=body['lastName'],
                                        userName=body['userName'], email=body['email'],
                                        phone=body['phone']
                                    )

    if updatedUser == None:
        return internalServerErrorResponse(ErrorCodes.USER_UPDATE_FAILED,
                                           message=getUserUpdateFailedErrorPacket())