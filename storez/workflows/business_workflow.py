import os
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse

from business.models import Business, BusinessAddress
from account.views import getUserByAccessToken

from business.views import (
                                createBusiness as createNewBusiness,
                                createBusinessAddress,
                                getBusinessByEmail,
                                getBusinessByPhone
                               )

from apiutility.validators import (
                                    validateKeys,
                                    validateEmailFormat,
                                    validatePhoneFormat,
                                    validateThatStringIsEmptyAndClean,
                                    validateThatStringIsEmpty,
                                    )
from error.errorCodes import (
                        ErrorCodes,
                        getGenericInvalidParametersErrorPacket,
                        getUserAlreadyExistErrorPacket,
                        getUserCreationFailedErrorPacket,
                        getUserDoesNotExistErrorPacket,
                        getUserUpdateFailedErrorPacket,
                        getUnauthenticatedErrorPacket,
                        DefaultErrorMessages,
                        getUnauthenticatedErrorPacket,
                        getUnauthorizedErrorPacket,
                        getPasswordResetFailedErrorPacket,
                        getBusinessAlreadyExistErrorPacket,
                        getBusinessCreationFailedErrorPacket,
                        getBusinessCreationAddressFailedErrorPacket,
                        getBusinessDoesNotExistErrorPacket    
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

from dataTransformer.jsonTransformer import(transformBusiness,
                                            transformBusinessList,
                                            ) 

from django.core.paginator import Paginator

import logging

logger = logging.getLogger(__name__)


# Handles 'businesses/' endpoints requests
def userBusinessRouter(request):
    if request.method == "GET":
        return getAllBusiness(request)
        
    if request.method =="POST":
        return createBusiness(request)


# Create Business
def createBusiness(request):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                       message=getUnauthenticatedErrorPacket())
    
    # Check if user has the privilege to create the resource
    if user.userCategoryType != 'manager':
        return unAuthorizedResponse(ErrorCodes.UNAUTHORIZED_REQUEST, message=getUnauthorizedErrorPacket())

    # get Json information passed in
    body = json.loads(request.body)

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body,requiredKeys=[
                               'businessName','businessEmail','businessPhone','street','city','state','country','zipCode'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")

    # validate if the email is in the correct format
    if not validateEmailFormat(body['businessEmail']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

    # validate if the phone is in the correct format
    if not validatePhoneFormat(body['businessPhone']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Phone format is invalid"))

    # check if business with that email exists
    if getBusinessByEmail (body['businessEmail']) is not None:        
        return resourceConflictResponse(errorCode=ErrorCodes.BUSINESS_ALREADY_EXIST,
                                            message=getBusinessAlreadyExistErrorPacket("businessEmail"))
    
    # Check if business with that phone exists
    if getBusinessByPhone(body['businessPhone']) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.BUSINESS_ALREADY_EXIST,
                                        message=getBusinessAlreadyExistErrorPacket('businessPhone'))

    businessName = body['businessName']
    businessEmail = body ['businessEmail']
    businessPhone = body['businessPhone']
    street = body['street']
    city = body['city']
    state = body['state']
    country = body['country']
    zipCode= body['zipCode']

    createdBusiness = createNewBusiness(
                                            user=user,
                                            businessName=businessName,
                                            businessEmail=businessEmail,
                                            businessPhone=businessPhone
                                            )

    if createdBusiness == None:
        return internalServerErrorResponse(ErrorCodes.BUSINESS_CREATION_FAILED,
                                            message=getBusinessCreationFailedErrorPacket())

    businessAddress = createBusinessAddress(user=user,
                                                business=createdBusiness,
                                                street= street,
                                                city= city,
                                                state= state,
                                                country= country,
                                                zipCode= zipCode,
                                                )

    if businessAddress == None:
        return internalServerErrorResponse(ErrorCodes.Business_ADDRESS_CREATION_FIELD,
                                            message=getBusinessCreationAddressFailedErrorPacket())

    return successResponse(message="successfully created restaurant", body=transformBusiness(createdBusiness))