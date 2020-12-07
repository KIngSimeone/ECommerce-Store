import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse

from account.views import getUserByAccessToken
from business.models import Product

from business.views import createProduct as createNewProduct

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
                        getBusinessDoesNotExistErrorPacket,
                        getProductCreationFailedErrorPacket   
                    )

from dataTransformer.jsonTransformer import(transformProduct,
                                            transformProductist
                                            ) 


from django.core.paginator import Paginator


import logging

logger = logging.getLogger(__name__)