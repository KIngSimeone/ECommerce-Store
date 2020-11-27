import os
import json
from django.conf import settings
from dotenv import load_dotenv
from django.http import HttpResponse, JsonResponse

from business.models import Business, BusinessAddress
from accounts.views import getUserByAccessToken

from business.views import (
                                createBusiness as createNewRestaurant,
                                createBusinessAddress
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
                        getUserDeletionFailedErrorPacket,
                        getPasswordResetFailedErrorPacket,
                        getBuisnessAlreadyExistErrorPacket,
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



# Create Restaurant
def createRestaurant(request):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                       message=getUnauthenticatedErrorPacket())
    
    # get Json information passed in
    data = json.loads(request.body)

    #check if required fields are present in request payload
    missingKeys = validateKeys(payload=data,requiredKeys=[
                               'restaurantName','restaurantEmail','restaurantLogo','street','city','state','country','zipCode'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")

    #validate if the email is in the correct format
    if not validateEmailFormat(data['restaurantEmail']):
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS,
                                  message=getGenericInvalidParametersErrorPacket("Email format is invalid"))

    #check if restaurant with that email exists
    if getRestaurantByEmail(data['restaurantEmail'])is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.RESTAURANT_ALREADY_EXIST,
                                            message=getRestaurantAlreadyExistErrorPacket(value="restaurantEmail"))

    restaurantName = data['restaurantName']
    restaurantEmail = data ['restaurantEmail']
    restaurantLogo = data['restaurantLogo']
    street = data['street']
    city = data['city']
    state = data['state']
    country = data['country']
    zipCode= data['zipCode']

    createdRestaurant = createNewRestaurant(
                                            user=user,
                                            restaurantName=restaurantName,
                                            restaurantEmail=restaurantEmail,
                                            restaurantLogo=restaurantLogo
                                            )

    if createdRestaurant == None:
        return internalServerErrorResponse(ErrorCodes.RESTAURANT_CREATION_FAILED,
                                            message=getRestaurantCreationFailedErrorPacket())

    restaurantAddress = createRestaurantAddress(user=user,
                                                restaurant=createdRestaurant,
                                                street= street,
                                                city= city,
                                                state= state,
                                                country= country,
                                                zipCode= zipCode,
                                                )

    if restaurantAddress == None:
        return internalServerErrorResponse(ErrorCodes.RESTAURANT_ADDRESS_CREATION_FIELD,
                                            message=getRestaurantCreationAddressFailedErrorPacket())

    restaurantMenu = createRestaurantMenu(user=user,
                                        restaurant=createdRestaurant
                                        )

    if restaurantMenu == None:
        return internalServerErrorResponse(ErrorCodes.RESTAURANT_MENU_CREATION_FAILED,
                                            message=getRestaurantMenuCreationFailedErrorPacket())

    return successResponse(message="successfully created restaurant", body=transformRestaurant(createdRestaurant))