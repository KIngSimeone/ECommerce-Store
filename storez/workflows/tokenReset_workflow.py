import json

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

from error.errorCodes import (
                        ErrorCodes, 
                        DefaultErrorMessages,
                        getUnauthenticatedErrorPacket,
                        getUnauthorizedErrorPacket,
                        getUserDoesNotExistErrorPacket,
                        getGenericInvalidParametersErrorPacket,
                    )

from apiutility.validators import (
                                validateKeys, 
                                validateEmailFormat, 
                            )

from account.views import (
                getUserByEmailOnly,
                setupUserPasswordResetToken,
                getUserPasswordResetTokenByResetToken,
                sendEmail
            )


def resetTokenURLRouter(request):
    if request.method == "POST":
        return resetToken(request)

def validateTokenURLRouter(request):
    if request.method == "POST":
        return validateToken(request)

def resetToken(request):
    # get the request payload
    body = json.loads(request.body)

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=['email'])
    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
    
    # check if email is in valid format
    email = body['email']
    if validateEmailFormat(email) is False:
        return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS, message="Email format is invalid")
    
    # confirm if an account is associated with the email
    user = getUserByEmailOnly(email)
    if user is None:
        return resourceNotFoundResponse(ErrorCodes.USER_DOES_NOT_EXIST, message=getUserDoesNotExistErrorPacket())
    
    # generate user access token
    userToken = setupUserPasswordResetToken(user)
    if userToken == None:
        return resourceNotFoundResponse(ErrorCodes.USER_DOES_NOT_EXIST, message=getUserDoesNotExistErrorPacket())
    
    # create and send notification to email channel
    createEmailMessage = sendEmail(email=email,token=userToken)

    return successResponse(message="An email was sent to your account if you have an account with us", body={})
    
def validateToken(request):
    # get the request payloads
    body = json.loads(request.body)

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=['token'])
    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
    
    # check if token is valid and hasn't expired
    token = body['token']
    isValid = (getUserPasswordResetTokenByResetToken(token) != None)
    
    if isValid == False:
        return badRequestResponse(ErrorCodes.GENERIC_INVALID_PARAMETERS, message= getGenericInvalidParametersErrorPacket(0, "invalid reset token"), body={"isValid": isValid})

    elif isValid == True:
        return successResponse(message="Token is valid", body={"isValid": isValid})


