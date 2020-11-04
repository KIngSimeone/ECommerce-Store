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
    USER_DELETION_FAILED = "Something went wrong, could not delete the user successfully"
    PASSWORD_RESET_FAILED = "Something went wrong, attempt to reset the password was unsuccessful"

    MAGENTO_SHOP_ALREADY_EXIST = "The specified magento shop already exist"
    PRESTASHOP_ALREADY_EXIST = "The specified prestashop already exist"
    MAGENTO_CREDENTIAL_CREATION_FAILED = "Something went wrong, could not create the magento credential successfully"
    PRESTASHOP_CREDENTIAL_CREATION_FAILED = "Something went wrong, could not create the prestashop credential successfully"
    WOOCOMMERCE_SHOP_ALREADY_EXIST = "The specified woocommerce shop already exist"
    WOOCOMMERCE_CREDENTIAL_CREATION_FAILED = "Something went wrong, could not create the woocommerce shop credential successfully"

    CDON_CREDENTIAL_ALREADY_EXIST = "The specified CDON token already exist for merchant"
    CDON_CREDENTIAL_CREATION_FAILED = "Something went wrong, could not create the CDON credential for merchant successfully"
    WISH_CREDENTIAL_ALREADY_EXIST = "The specified WISH token already exist for merchant"
    WISH_CREDENTIAL_CREATION_FAILED = "Something went wrong, could not create the WISH credential for merchant successfully"
    FYNDIQ_CREDENTIAL_ALREADY_EXIST = "The specified FYNDIQ token already exist for merchant"
    FYNDIQ_CREDENTIAL_CREATION_FAILED = "Something went wrong, could not create the FYNDIQ credential for merchant successfully"
    SHOPIFY_CREDENTIAL_ALREADY_EXIST = "The specified SHOPIFY token already exist for merchant"
    SHOPIFY_CREDENTIAL_CREATION_FAILED = "Something went wrong, could not create the SHOPIFY credential for merchant successfully"

    INVALID_COUNTRY_CODE = "The country code specified is invalid"
    INVALID_CURRENCY_CODE = "The currency code specified is invalid"

    ORDER_CREATION_FAILED = "Something went wrong, could not create the order for merchant successfully"
    ORDER_DELETION_FAILED = "Something went wrong, could not delete the order for merchant successfully"
    ORDER_DOES_NOT_EXIST = "The requested order does not exist"



## ACOUNT MANAGEMENT ERROR PACKET
def getInvalidCredentialsErrorPacket():
    return getError(code = ErrorCodes.INVALID_CREDENTIALS,
                    defaultMessage = DefaultErrorMessages.INVALID_CREDENTIALS)



## generic invalid errors
def getGenericInvalidParametersErrorPacket(message):
    return getError(code=ErrorCodes.GENERIC_INVALID_PARAMETERS, defaultMessage=message)


## base error
def getError(code, defaultMessage):
    try:
        errorRecord, _ = Error.objects.get_or_create(code=code.value, description=defaultMessage.value)
        return {'errorCode': errorRecord.code, 'message': errorRecord.description}

    except IntegrityError:
        return {'errorCode': code.value, 'message': defaultMessage.value}