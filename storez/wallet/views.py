from django.shortcuts import render
from .models import UserAccount, ManagerAccount, ControllerAccount
import random

import string

import logging

logger = logging.getLogger(__name__)

# Create your views here.

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


def createManagerAccount(manager):
    try:
        if manager is None:
            return None

        manageraccount = ManagerAccount(manager=manager)       
        manageraccount.balance = 0

        manageraccount.save()

        return manageraccount

    except Exception as e:
        logger.error("createManagerAccount@Error")
        logger.error(e)
        return None


def createControllerAccount(controller):
    try:
        if controller is None:
            return None

        controlleraccount = ControllerAccount(controller=controller)       
        controlleraccount.balance = 0

        controlleraccount.save()

        return controlleraccount

    except Exception as e:
        logger.error("createControllerrAccount@Error")
        logger.error(e)
        return None
