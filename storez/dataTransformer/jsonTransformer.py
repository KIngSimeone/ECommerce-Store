from apiutility.formatters import toUiReadableDateFormat


def generateLoginResponse(user, userAccessToken):
    user = {
        "id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "phone": user.phone,
        "userName": user.userName,
        "accessToken": userAccessToken.accessToken,
        "lastActive": toUiReadableDateFormat(user.lastActiveOn)
    }

    return user


def generateLoginResponseManager(manager, managerAccessToken):
    manager = {
        "id": manager.id,
        "firstName": manager.firstName,
        "lastName": manager.lastName,
        "email": manager.email,
        "phone": manager.phone,
        "userName": manager.userName,
        "accessToken": managerAccessToken.accessToken,
        "lastActive": toUiReadableDateFormat(manager.lastActiveOn)
    }

    return manager


def generateLoginResponseController(controller, controllerAccessToken):
    controller = {
        "id": controller.id,
        "firstName": controller.firstName,
        "lastName": controller.lastName,
        "email": controller.email,
        "phone": controller.phone,
        "userName": controller.userName,
        "accessToken": controllerAccessToken.accessToken,
        "lastActive": toUiReadableDateFormat(controller.lastActiveOn)
    }

    return controller

def transformUser(user):
    return {
        "id": user.id,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "userName": user.userName,
        "email": user.email,
        "phone": user.phone,
        "createdAt": toUiReadableDateFormat(user.createdAt)        
    }