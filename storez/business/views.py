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

def createBusiness(user,businessName,businessEmail,phone):
    try:
        business = Business(
                    user=user,
                    businessName=businesstName,
                    businessEmail=businessEmail,
                    phone=phone
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