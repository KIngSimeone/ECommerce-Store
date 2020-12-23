from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

from http import HTTPStatus


def badRequestResponse(errorCode, message = "", body = {}):
    return errorResponse(HTTPStatus.BAD_REQUEST, errorCode, message= message, body= body)

def unAuthorizedResponse(errorCode, message = "", body = {}):
    return errorResponse(HTTPStatus.FORBIDDEN, errorCode, message= message, body= body)

def unAuthenticatedResponse(errorCode, message = "", body = {}):
    return errorResponse(HTTPStatus.UNAUTHORIZED, errorCode, message= message, body= body)

def resourceConflictResponse(errorCode, message = "", body = {}):
    return errorResponse(HTTPStatus.CONFLICT, errorCode, message= message, body = body)

def resourceNotFoundResponse(errorCode, message = "", body = {}):
    return errorResponse(HTTPStatus.NOT_FOUND, errorCode, message = message, body = body)

def internalServerErrorResponse(errorCode, message = "", body = {}):
    return errorResponse(HTTPStatus.INTERNAL_SERVER_ERROR, errorCode, message= message, body = body)

def errorResponse(httpStatusCode, errorCode, message = "", body = {}):
    return JsonResponse({'errorCode': errorCode, 'data': body, 'message': message}, status=httpStatusCode, safe=False)

## success responses

def createdResponse(message="", body={}):
    return successResponse(HTTPStatus.CREATED, message=message, body=body)


def paginatedResponse(httpStatusCode=HTTPStatus.OK, message="", body={}, pagination={}):
    return successResponse(httpStatusCode=httpStatusCode, message=message, body={'data': body, 'pagination': pagination})

def successResponse(httpStatusCode=HTTPStatus.OK, message="", body={}):
    return JsonResponse({'data': body, 'message': message}, status=httpStatusCode, safe=False)

def successimgResponse(httpStatusCode=HTTPStatus.OK, message="", body={}):
    return HttpResponse({'data': body, 'message': message}, status=httpStatusCode, safe=False)