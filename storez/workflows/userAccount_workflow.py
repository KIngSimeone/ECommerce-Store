import os
import json
from django.conf import settings

from account.views import (
                           createUser as createUserRecord,
                           getUserByUserName,
                           getUserByEmail,
                           getUserByPhone
                          )
                           
from wallet.views import createUserAccount
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
                              getUserCreationFailedErrorPacket
                             )
from dataTransformer.jsonTransformer import transformUser

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# handles "/users/" endpoint requests
def userAccountRouter(request):
    if request.method == "POST":
        return createUser(request)



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
