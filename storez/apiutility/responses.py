from django.shortcuts import render
from django.http import JsonResponse

from http import HTTPStatus


def badRequestResponse(errorCode, message = "", body = {}):
    return errorResponse(HTTPStatus.BAD_REQUEST, errorCode, message= message, body= body)

def errorResponse(httpStatusCode, errorCode, message = "", body = {}):
    return JsonResponse({'errorCode': errorCode, 'data': body, 'message': message}, status=httpStatusCode, safe=False)

## success responses

def createdResponse(message="", body={}):
    return successResponse(HTTPStatus.CREATED, message=message, body=body)


def paginatedResponse(httpStatusCode=HTTPStatus.OK, message="", body={}, pagination={}):
    return successResponse(httpStatusCode=httpStatusCode, message=message, body={'data': body, 'pagination': pagination})

def successResponse(httpStatusCode=HTTPStatus.OK, message="", body={}):
    return JsonResponse({'data': body, 'message': message}, status=httpStatusCode, safe=False)