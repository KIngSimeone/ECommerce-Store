from .models import Error
from enum import Enum, IntEnum
from django.db import IntegrityError

class ErrorCodes(IntEnum):
    UNAUTHENTICATED_REQUEST = 1
    UNAUTHORIZED_REQUEST = 2
    PRODUCT_DOES_NOT_EXIST = 3
    MISSING_FIELDS = 4
    GENERIC_INVALID_PARAMETERS = 5

    INVALID_CREDENTIALS = 25
    USER_ALREADY_EXIST = 26
    PASSWORD_RESET_FAILED = 27
    USER_DOES_NOT_EXIST = 28
    USER_WITH_USERNAME_ALREADY_EXIST = 29
    USER_CATEGORY_TYPE_INVALID = 30
    USER_WITH_EMAIL_ALREADY_EXIST = 31
    USER_CREATION_FAILED = 32
    USER_UPDATE_FAILED = 33
    USER_DELETION_FAILED = 34
    USER_CATEGORY_TYPE_INVALID = 35


class DefaultErrorMessages(str, Enum):
    UNATHENTICATED_REQUEST = "Your session has expired, Please login"
    UNAUTHORIZED_REQUEST = "Not authorized to carry out operation"
    PRODUCT_DOES_NOT_EXIST = "The requested product does not exist"
    MISSING_FIELDS = "The following key(s) are required"
    PRODUCT_UPDATE_FAILED = "Something went wrong, could not update the product successfully"
    PRODUCT_ALREADY_EXIST = "A product with same {} already exists"
    PRODUCT_CREATION_FAILED = "Something went wrong, could not create the product for merchant successfully"
    PRODUCT_DELETION_FAILED = "Something went wrong, could not delete the product for merchant successfully"

    INVALID_CREDENTIALS = "Invalid credentials"
    USER_ALREADY_EXIST = "A user with same {} already exists"
    USER_DOES_NOT_EXIST = "The requested user does not exist"
    USER_WITH_USERNAME_ALREADY_EXIST = "A user with same username already exist"
    USER_CATEGORY_TYPE_INVALID = "The specified user category type is invalid"
    USER_WITH_EMAIL_ALREADY_EXIST = "A user with same email already exist"
    USER_CREATION_FAILED = "Something went wrong, could not create the user successfully"
    USER_UPDATE_FAILED = "Something went wrong, could not update the user successfully"
    USER_CATEGORY_TYPE_INVALID = "The specified user category type is invalid"
    USER_DELETION_FAILED = "Something went wrong, could not delete the user successfully"
    PASSWORD_RESET_FAILED = "Something went wrong, attempt to res et the password was unsuccessful"

    INVALID_COUNTRY_CODE = "The country code specified is invalid"
    INVALID_CURRENCY_CODE = "The currency code specified is invalid"

    ORDER_CREATION_FAILED = "Something went wrong, could not create the order for merchant successfully"
    ORDER_DELETION_FAILED = "Something went wrong, could not delete the order for merchant successfully"
    ORDER_DOES_NOT_EXIST = "The requested order does not exist"


# AUTH ERROR PACKET
def getUnauthenticatedErrorPacket():
    return getError(code = ErrorCodes.UNAUTHENTICATED_REQUEST,
                    defaultMessage = DefaultErrorMessages.UNATHENTICATED_REQUEST)

def getUnauthorizedErrorPacket():
    return getError(code = ErrorCodes.UNAUTHORIZED_REQUEST,
                    defaultMessage = DefaultErrorMessages.UNAUTHORIZED_REQUEST)



## ACOUNT MANAGEMENT ERROR PACKET
def getInvalidCredentialsErrorPacket():
    return getError(code = ErrorCodes.INVALID_CREDENTIALS,
                    defaultMessage = DefaultErrorMessages.INVALID_CREDENTIALS)

def getUserAlreadyExistErrorPacket(value):
    return getError(code = ErrorCodes.USER_ALREADY_EXIST, 
                    defaultMessage = DefaultErrorMessages.USER_ALREADY_EXIST.format(value))

def getUserDoesNotExistErrorPacket():
    return getError(code=ErrorCodes.USER_DOES_NOT_EXIST,
                    defaultMessage = DefaultErrorMessages.USER_DOES_NOT_EXIST)

def getUserCategoryInvalidErrorPacket():
    return getError(code=ErrorCodes.USER_CATEGORY_TYPE_INVALID,
                    defaultMessage=DefaultErrorMessages.USER_CATEGORY_TYPE_INVALID)

## Manager already exist error packet
def getManagerAlreadyExistErrorPacket(value):
    return getError(code = ErrorCodes.USER_ALREADY_EXIST, 
                    defaultMessage = DefaultErrorMessages.USER_ALREADY_EXIST.format(value))

def getUserCreationFailedErrorPacket():
    return getError(code=ErrorCodes.USER_CREATION_FAILED,
                    defaultMessage=DefaultErrorMessages.USER_CREATION_FAILED)

def getUserUpdateFailedErrorPacket():
    return getError(code=ErrorCodes.USER_UPDATE_FAILED, 
                        defaultMessage=DefaultErrorMessages.USER_UPDATE_FAILED)

## generic invalid error
def getGenericInvalidParametersErrorPacket(message):
    return getError(code=ErrorCodes.GENERIC_INVALID_PARAMETERS, defaultMessage=message)


## base error
def getError(code, defaultMessage):
    try:
        errorRecord, _ = Error.objects.get_or_create(code=code.value, description=defaultMessage)
        return {'errorCode': errorRecord.code, 'message': errorRecord.description}

    except IntegrityError:
        return {'errorCode': code.value, 'message': defaultMessage}