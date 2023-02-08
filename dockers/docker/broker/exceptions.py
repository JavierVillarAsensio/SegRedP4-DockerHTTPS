#!/usr/bin/env python3

from werkzeug import exceptions


class WrongFormat(exceptions.BadRequest):
    pass

class WrongAuthorizationFormat(exceptions.BadRequest):
    pass

class WrongContent(exceptions.BadRequest):
    pass

class WrongJson(exceptions.BadRequest):
    pass

class NonExistingUser(exceptions.Unauthorized):
    pass

class NonExistingAuthorization(exceptions.Unauthorized):
    pass

class UnauthorizedToken(exceptions.Unauthorized):
    pass

class WrongPassword(exceptions.Unauthorized):
    pass

class UserAlreadyExists(exceptions.Conflict):
    pass

class FileAlreadyExists(exceptions.Conflict):
    pass

class NonExistingFile(exceptions.NotFound):
    pass


HTTPS_ERROR = {
    'WrongFormat': {
        'info': "The format is incorrect, check the values (username, password) or the json input",
        'error code': 400
    },
    'WrongAuthorizationFormat': {
        'info': "The format is incorrect, check the syntax and the introduced token",
        'error code': 400
    },
    'WrongContent': {
        'info': "The content/json specified is incorrect or does not exist",
        'error code': 400
    },
    'WrongJson': {
        'info': "The input is not valid, it should be a json object",
        'error code': 400
    },
    'UnauthorizedToken':{
        'info': "This token is not authorized or expired",
        'error code': 401,
    },
    'NonExistingAuthorization': {
        'info': "The user does not exist or the authorization was not introduced/incorrect",
        'error code': 401
    },
    'NonExistingUser':{
        'info': "User introduced does not exist, or the password introduced is incorrect",
        'error code': 401,
    },
    'WrongPassword':{
        'info': "The password introduced is not correct",
        'error code': 401,
    },
    'NotFound':{
        'info': "The resource introduced does not exist",
        'error code': 404,
    },
    'NonExistingFile':{
        'info': "The file introduced does not exist",
        'error code': 404,
    },
    'MethodNotAllowed': {
        'info': "Method not allowed",
        'error code': 405,
    },
    'UserAlreadyExists':{
        'info': "User already exists",
        'error code': 409,
    },
    'FileAlreadyExists':{
        'info': "File already exists",
        'error code': 409,
    },
}