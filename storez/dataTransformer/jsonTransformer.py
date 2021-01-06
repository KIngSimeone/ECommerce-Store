from apiutility.formatters import toUiReadableDateFormat
from django.conf import settings
from django.http import FileResponse


def generateLoginResponse(user, userAccessToken):
    user = {
        "id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "phone": user.phone,
        "userName": user.userName,
        "accessToken": userAccessToken.accessToken,
        "userCategoryType": user.userCategoryType,
        "lastActive": toUiReadableDateFormat(user.lastActiveOn)
    }
    return user

def transformUser(user):
    return {
        "id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "userName": user.userName,
        "email": user.email,
        "phone": user.phone,
        "userCategoryType": user.userCategoryType,
        "createdAt": toUiReadableDateFormat(user.createdAt)        
    }

def transformUsersList(Users):
    results = []
    for user in Users:
        results.append(transformUser(user))

    return results

def transformBusiness(business):
    user = business.user.firstName + " " + business.user.lastName
    return {
        "id": business.id,
        "name": business.businessName,
        "email": business.businessEmail,
        "phone": business.businessPhone,
        "createdAt": business.createdAt,
        "createdBy": user
    }

def transformBusinessList(businessList):
    results = []
    for business in businessList:
        results.append(transformBusiness(business))

    return results

def transformProduct(product):
    business = product.business.businessName + "'s products."  
    return {
        "id": product.id,
        "name": product.productName,
        "price": product.productPrice,
        "quantity": product.quantity
    }

def transformLogo(logo,address,logoImg):
    return {
        "business": logo.business.businessName,
        "logo": logoImg,
        "businessaddress": address.street + ", " + address.city + ", " + address.state + ", " + address.country
    }

def transformProductList(productList):
    results = []
    for product in productList:
        results.append(transformSProduct(product))
