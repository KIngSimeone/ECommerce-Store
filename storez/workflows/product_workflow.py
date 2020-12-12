import os
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse

from account.views import getUserByAccessToken
from business.models import Product, Business

from business.views import (
                            createProduct as createNewProduct,
                            getBusinessById,
                            getProductForBusiness
                            )
from apiutility.validators import (
                                    validateKeys,
                                    validateEmailFormat,
                                    validatePhoneFormat,
                                    validateThatStringIsEmptyAndClean,
                                    validateThatStringIsEmpty,
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
                                            transformProductList
                                            ) 


from django.core.paginator import Paginator


import logging

logger = logging.getLogger(__name__)

# Handles 'product/' endpoints requests
def productRouter(request):   
    if request.method =="POST":
        return createProduct(request)

# Handles 'product/ID' endpoint requets
def businessProduct(request,businessID):
    if request.method == "GET":
        return getBusinessProductByBusinessID(request,businessID)

# Create product
def createProduct(request):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)
    body = json.loads(request.body)

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                            message=getUnauthenticatedErrorPacket())
    
    # check if required fields are present in requets payload
    missingKeys = validateKeys(payload=body,requiredKeys=[
                               'productName','productPrice','quantity'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")
    
    # save passed information in varaibles
    productName = body['productName']
    productPrice = body['productPrice']
    quantity = body['quantity']

    business = Business.objects.get(user=user)

    if user.userCategoryType != 'manager':
        return unAuthorizedResponse(ErrorCodes.UNAUTHORIZED_REQUEST, message=getUnauthorizedErrorPacket())

    createdProduct = createNewProduct(business=business,productName=productName,productPrice=productPrice,quantity=quantity)

    if createdProduct == None:
        return internalServerErrorResponse(ErrorCodes.PRODUCT_CREATION_FAILED,
                                            message=getProductCreationFailedErrorPacket())

    return successResponse(message="successfully added product", body=transformProduct(createdProduct))

def getBusinessProductByBusinessID(request,businessID):
    # verify that calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                       message=getUnauthenticatedErrorPacket())
    
    # check if business with given ID exists
    businessToBeRetrieved = getBusinessById(businessID)
    if businessToBeRetrieved == None:
        return resourceNotFoundResponse(ErrorCodes.BUSINESS_DOES_NOT_EXIST,message=getBusinessDoesNotExistErrorPacket)
        
    products = getProductForBusiness(business=businessToBeRetrieved)
    if request.GET.get('pageBy') == '-1':
        paginationDetails = {
            "totalPages": 1,
            "limit": -1,
            "currentPage": 1
        }
        return paginatedResponse(message="list of all Products",
                               body=transformProductList(products),
                               pagination=paginationDetails
                            )
    if request.GET.get('pageBy'):
        pageBy = request.GET.get('pageBy')
    else:
        pageBy = 10

    paginator = Paginator(products, pageBy)

    if request.GET.get('page'):
        pageNum = request.GET.get('page')
        
    else:
        pageNum = 1
    # try if the page requested exists or is empty
    try:
        paginated_products = paginator.page(pageNum)

        paginationDetails = {

            "totalPages": paginator.num_pages,
            "limit": pageBy,
            "currentPage": pageNum
        }

    except Exception as err:
        logger.error(err)
        paginated_products = []
        paginationDetails = {}
    
    return paginatedResponse(message="list of all products",
                             body=transformProductList(paginated_products),
                             pagination=paginationDetails)
