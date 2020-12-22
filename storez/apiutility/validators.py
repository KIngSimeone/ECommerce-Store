import re
from datetime import datetime

def stringIsNumber(value):
    try:
        return (stringIsInteger(value) or stringIsFloat(value))
    except:
        return False


def stringIsInteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def stringIsFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def stringIsBoolean(value):
    try:
        bool(value)
        return True
    except ValueError:
        return False


def validateEmailFormat(email):
    emailPattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'

    if(re.search(emailPattern, email)):
        return True
    
    return False


def validatePhoneFormat(phone):
    if not stringIsInteger(phone):
        return False

    # valid phone format for Nigeria with and without international dialing code 
    # e.g +2349099514739 or 09099514739

    return len(phone) >=11 and len(phone) <=13

def validateThatAStringIsClean(value):
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]') 
    return (regex.search(value) == None)

def validateThatStringIsEmpty(value):
    return (len(value.strip()) > 0)

def validateThatStringIsEmptyAndClean(value):
    is_clean = (re.compile(r'[@_!#$%^&*()<>?/\|}{~:]').search(value) == None)
    not_empty = (len(value.strip()) != 0)

    return (is_clean and not_empty)

def validateKeys(payload, requiredKeys):
    # extract keys from payload
    payloadKeys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missingKeys = []
    for key in requiredKeys:
        if key not in payloadKeys:
            missingKeys.append(key)

    return missingKeys
