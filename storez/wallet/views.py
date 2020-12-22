from django.shortcuts import render
from .models import UserAccount
import random

import string

import logging

logger = logging.getLogger(__name__)


def createUserAccount(user):
    try:
        if user is None:
            return None

        useraccount = UserAccount(user=user)       
        useraccount.balance = 0

        useraccount.save()

        return useraccount

    except Exception as e:
        logger.error("createUserAccount@Error")
        logger.error(e)
        return None
