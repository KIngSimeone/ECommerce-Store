from django.http import JsonResponse
import json

from account.views import (
                           authenticateUser,
                           generateUserAccessToken,
                          )

from apiutility.responses import (
                                  badRequestResponse,
                                  successResponse
                                 )

from dataTransformer.jsonTransformer import (
                                             generateLoginResponse,
                                            )

from apiutility.validators import validateKeys, validateThatStringIsEmpty
from error.errorCodes import (
                             ErrorCodes,
                             getInvalidCredentialsErrorPacket,
                             getGenericInvalidParametersErrorPacket
                             )
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# handle  user "/authenticate" route
def authenticationRouter(request):
    if request.method == 'POST':
        ## call authenticate
        return login(request)

# Authenticate User
def login(request):
    body = json.loads(request.body)

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=['email', 'password'])
    if missingKeys:
        return badRequestResponse(errorCode=ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")

    email = body['email']
    password = body['password']

    # check if email is not empty
    if not validateThatStringIsEmpty(email):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket(message="Email field cannot be empty"))
    
    # check if password is not empty
    if not validateThatStringIsEmpty(password):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket(message="Password field cannot be empty"))

    user = authenticateUser(email, password)

    if user is None:
        return badRequestResponse(ErrorCodes.INVALID_CREDENTIALS, message=getInvalidCredentialsErrorPacket())

    userAccessToken = generateUserAccessToken(user)

    return successResponse(message="successfully authenticated", body=generateLoginResponse(user, userAccessToken))
