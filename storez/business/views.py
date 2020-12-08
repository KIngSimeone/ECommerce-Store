from django.shortcuts import render

from django.shortcuts import render
from .models import(
                    Business,
                    BusinessAddress,
                    Product,
                    )
from django.utils import timezone
from datetime import datetime, date, timedelta
from django.conf import settings


import secrets

# import the logging library
import logging

# Create and instance of a logger 
logger = logging.getLogger(__name__)

def createBusiness(user,businessName,businessEmail,businessPhone):
    try:
        business = Business(
                    user=user,
                    businessName=businessName,
                    businessEmail=businessEmail,
                    businessPhone=businessPhone
                    )

        business.save()
        return business

    except Exception as e:
        logger.error("createBusiness@error")
        logger.error(e)
        return None

def createBusinessAddress(user,business,street,city,state,country,zipCode): 
    try:
        address = BusinessAddress(
                user=user,
                business=business,
                street=street,
                city=city,
                state=state,
                country=country,
                zipCode=zipCode
                )

        address.save()
        return address
    except Exception as e:
        logger.error("CreateBusinessAddress@error")
        logger.error(e)
        return None

def getBusinessByEmail(email):
    try:
        return Business.objects.get(businessEmail=email)
    except Exception as err:
        logger.error("getBusinessByEmail@error")
        logger.error(err)
        return None

def getBusinessByPhone(phone):
    try:
        return Business.objects.geta(businessPhone=phone)
    except Exception as err:
        logger.error("getBusinessByPhone@error")
        logger.error(err)
        return None

def getBusinessById(businessId):
    try:
        return Business.objects.get(id=businessId)

    except Exception as err:
        logger.error('getBusinessById@error')
        logger.error(err)
        return None

def listAllBusinesses():
    try:
        return Business.objects.filter(isDeleted=False)
    except Exception as err:
        logger.error('listAllBusinesses@error')
        logger.error(err)
        return None

def uploadFileToS3(filepath, s3FileName):
    s3 = boto3.client('s3',endpoint_url=settings.AWS_S3_CUSTOM_DOMAIN,
                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                        )
    try:
        s3.upload_file(
            filepath,
            settings.AWS_STORAGE_BUCKET_NAME,
            s3FileName
        )

        return True
    except Exception as e:
        logger.error("uploadFileToS3@error")
        logger.error(e)
        return False

## PRODUCT VIEWS

def createProduct(business,productName,productPrice,quantity):
    try:
        product = Product(
            business=business,
            productName=productName,
            productPrice=productPrice,
            quantity=quantity
            )
        product.save()
        return product
    except Exception as e:
        logger.error("createProduct@error")
        logger.error(e)
        return None


def getProductsForBusiness(business):
    try:
        return Product.objects.filter(business=business)
    except Exception as e:
        logger.error('getProductForBusiness@error')
        logger.error(e)
        return None
