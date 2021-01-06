# Add payment option
import os
import boto3
import json
import io
from PIL import Image

from django.conf import settings
from django.http import HttpResponse, JsonResponse, FileResponse
from sendfile import sendfile

from business.models import Business, BusinessAddress
from account.views import getUserByAccessToken
from datetime import datetime, date, timedelta

from business.views import (
                                createBusiness as createNewBusiness,
                                createBusinessAddress,
                                getBusinessByEmail,
                                getBusinessByPhone,
                                getBusinessById,
                                listAllBusinesses,
                                uploadFileToS3,
                                getBusinessLogo,
                                getBusinessAddress,
                                getClient
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
                        getBusinessDoesNotExistErrorPacket,
                        getLogoDoesNotExistErrorPacket,
                        getAddressDoesNotExistErrorPacket
                    )

from apiutility.responses import (
                    unAuthorizedResponse,
                    unAuthenticatedResponse,
                    badRequestResponse,
                    resourceConflictResponse,
                    successResponse,
                    resourceNotFoundResponse,
                    paginatedResponse,
                    internalServerErrorResponse,
                    successimgResponse
                )

from dataTransformer.jsonTransformer import(transformBusiness,
                                            transformBusinessList,
                                            transformLogo
                                            ) 

from django.core.paginator import Paginator

import logging

logger = logging.getLogger(__name__)


# Handles 'business/' endpoints requests
def userBusinessRouter(request):
    if request.method == "GET":
        return getAllBusiness(request)
        
    if request.method =="POST":
        return createBusiness(request)

# Handles 'upload/' endpoints requests
def uploadFileRouter(request):        
    if request.method =="POST":
        return uploadFile(request)

# Handles 'file/ID/' endpoints requests
def getFile(request,businessID):
    if request.method == "GET":
        return getBusinessLogoByBusinessID(request, businessID)

# Create Business
def createBusiness(request):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token) 

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")

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

def getAllBusiness(request):
    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")
    
    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST, message=getUnauthenticatedErrorPacket())

    # retrieve a list of all businesses
    allBusinessList = listAllBusinesses()

    # Paginate the retrieved businesses
    if request.GET.get('pageBy'):
        pageBy = request.GET.get('pageBy')
    else:
        pageBy = 10

    paginator = Paginator(allBusinessList, pageBy)

    if request.GET.get('page'):
        pageNum = request.GET.get('page')
    else:
        pageNum = 1
    
    # try if the page requested exists or is empty
    try:
        paginated_BusinessList = paginator.page(pageNum)

        paginationDetails = {
            "totalPages": paginator.num_pages,
            "limit": pageBy,
            "currentPage": pageNum
        }
    except Exception as e:
        print(e)
        paginated_BusinessList = []
        paginationDetails = {}

    return paginatedResponse(message="successfully retrieved businesses", 
                            body=transformBusinessList(paginated_BusinessList), 
                            pagination=paginationDetails
                        )

"""
def updateBusiness(request, businessID):
    # verify that the calling user has a valid token
    body = json.loads(request.body)
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST,
                                        message=getUnauthenticatedErrorPacket())

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body,requiredKeys=[
                               'businessName','businessEmail','businessPhone','street','city','state','country','zipCode'])

    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")

    # check if businesToBeUpdated already exists
    businessToBeUpdated = getBusinessById(businessID)
    if businessToBeUpdated is None:
        return resourceNotFoundResponse(ErrorCodes.BUSINESS_DOES_NOT_EXIST, getBusinessDoesNotExistErrorPacket())

    # Check if user has the privilege to perform action
    if user != businessToBeUpdated.user:
        return unAuthorizedResponse(ErrorCodes.UNAUTHORIZED_REQUEST, message=getUnauthorizedErrorPacket())

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
"""

def uploadFile(request):

    # verify that the calling user has a valid token
    token = request.headers.get('accessToken')
    user = getUserByAccessToken(token)

    if token is None:
        return badRequestResponse(errorCode=ErrorCodes.GENERIC_INVALID_PARAMETERS, message="accessToken is missing in the request headers")

    if user is None:
        return unAuthenticatedResponse(ErrorCodes.UNAUTHENTICATED_REQUEST, message=getUnauthenticatedErrorPacket())


    listOfFileRecord = list()

    if request.FILES.__contains__("image"):
        image = request.FILES.get("image")
        imgName = image.name

        # verify if the file format to upload is supported
        if not imgName.lower().endswith(('jpg','jpeg', 'png')):
            return badRequestResponse(ErrorCodes.FILE_FORMAT_INVALID,
                                    message="The file format isn't supported for Restaurant Logos")

        listOfFileRecord.append((image, 'others'))

    for item in listOfFileRecord:
        file = item[0]
        typeOfFile = item[1]

        name = file.name

        # take the file and store it in a temporary folder
        fileName = str(datetime.now().timestamp()) + name
        filePath = '' + fileName

        if not uploadFileToS3(filepath=filePath, s3FileName=fileName):
            return internalServerErrorResponse(ErrorCodes.FILE_UPLOAD_FAILED,
                                                message=DefaultErrorMessages.FILE_UPLOAD_FAILED)
    
    return successResponse(message="successfully uploaded file", body="done")


def getBusinessLogoByBusinessID(request,businessID):
    # verify that the calling user has a valid token
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
        return resourceNotFoundResponse(ErrorCodes.BUSINESS_DOES_NOT_EXIST,message=getBusinessDoesNotExistErrorPacket())
    
    logo = getBusinessLogo(business=businessToBeRetrieved)
    if logo == None:
        return resourceNotFoundResponse(ErrorCodes.LOGO_DOES_NOT_EXIST,message=getLogoDoesNotExistErrorPacket())

    # get business address
    address = getBusinessAddress(business=businessToBeRetrieved)
    if address == None:
        return resourceNotFoundResponse(ErrorCodes.ADDRESS_DOES_NOT_EXIST,message=getAddressDoesNotExistErrorPacket)
    """
    img = Image.open(logo.logo)
    output = io.BytesIO()
    img_as_string = output.getvalue()   

    logo_img = (str(img_as_string[:20])) 

    return successResponse(message="successfully created restaurant", body=transformLogo(logo=logo,address=address,logoImg=logo_img))
"""
    return FileResponse(logo.logo)
    
    
    

