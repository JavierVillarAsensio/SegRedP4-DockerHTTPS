#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api
import requests
import json

import exceptions

app = Flask(__name__)
api = Api(app, errors=exceptions.HTTPS_ERROR)
app.config['SERVER_NAME'] = 'myserver.local:5000'
URL_AUTH = 'https://auth.local:5000'
URL_FILE = 'https://file.local:5000'

def check_data():
        content = sort_args("doc_content")[0]
        content = json.dumps(content)
        content_json = None

        if not content:
            raise exceptions.WrongContent

        try:
            content_json = json.loads(content)
        except ValueError:
            raise exceptions.WrongJson

        return content_json

def get_authorization():
    authorization = request.headers.get("Authorization")
    token = None
    splited_authorization = authorization.split()

    if not authorization:
        raise exceptions.NonExistingAuthorization

    if  splited_authorization[0] != "token" or len(splited_authorization) != 2:
        raise exceptions.WrongAuthorizationFormat

    token = splited_authorization[1]

    return authorization, token

def sort_args(*args):
    args_arr = [None] * len(args)
    i = 0

    req_json = request.get_json(silent=True, force=True)

    if req_json:
        for arg in args:
            args_arr[i] = req_json.get(arg)
            i = i + 1

    else:
        for arg in args:
            args_arr[i] = request.form.get(arg)
            if not args_arr[i]:
                break
            i = i + 1

    return tuple(args_arr)

@api.resource('/version', methods=["GET"])
class Version(Resource):
    def get(self):
        return {'Running version': '1.2.0'}

@api.resource("/signup", methods=["POST"])
class Signup(Resource):
    def post(self):
        username, password = sort_args("username", "password")
        url = URL_AUTH + '/signup'
        req = requests.post(url, json = {"username" : username, "password" : password }, verify = "auth.crt")
        ind = req.text.find("\"error code\": ")
        if ind > 0:
            error = req.text[ind+14:ind+17]
            if error == "409":
                raise exceptions.UserAlreadyExists
            if error == "400":
                raise exceptions.WrongFormat

        return json.loads(req.text)

@api.resource("/login", methods=["POST"])
class Login(Resource):
    def post(self):
        username, password = sort_args("username", "password")
        url = URL_AUTH + "/login"
        req = requests.post(url, json = {"username" : username, "password" : password}, verify = "auth.crt")
        ind = req.text.find("\"error code\": ")
        if ind > 0:
            error = req.text[ind+14:ind+17]
            if error == "401":
                raise exceptions.NonExistingUser
            if error == "400":
                raise exceptions.WrongFormat

        return json.loads(req.text)


@api.resource("/<string:username>/<string:doc_id>", methods=["GET", "POST", "PUT", "DELETE"])
class UserDocuments(Resource):
    
    def __init__(self):
        super().__init__()
        self.authorization, self.token = get_authorization()

    def get(self, username, doc_id):
        url = URL_FILE + "/" + username + "/" + doc_id
        req = requests.get(url, headers = {"Authorization" : "token " + self.token}, verify = "file.crt")
        ind = req.text.find("\"error code\": ")
        if ind > 0:
            error = req.text[ind+14:ind+17]
            if error == "401":
                raise exceptions.UnauthorizedToken
            if error == "404":
                raise exceptions.NonExistingFile
        return json.loads(req.content)


    def post(self, username, doc_id):
        url = URL_FILE + "/" + username + "/" + doc_id
        req = requests.post(url, headers = {"Authorization" : "token " + self.token}, data = {"doc_content" : check_data()}, verify = "file.crt")
        ind = req.text.find("\"error code\": ")
        if ind > 0:
            error = req.text[ind+14:ind+17]
            if error == "400":
                raise exceptions.WrongContent
            if error == "401":
                raise exceptions.UnauthorizedToken
            if error == "409":
                raise exceptions.FileAlreadyExists
        return json.loads(req.text)

    def put(self, username, doc_id):
        url = URL_FILE + "/" + username + "/" + doc_id
        req = requests.put(url, headers = {"Authorization" : "token " + self.token}, data = {"doc_content" : check_data()}, verify = "file.crt")
        ind = req.text.find("\"error code\": ")
        if ind > 0:
            error = req.text[ind+14:ind+17]
            if error == "400":
                raise exceptions.WrongContent
            if error == "404":
                raise exceptions.NonExistingFile
            if error == "401":
                raise exceptions.NonExistingAuthorization
            
        return json.loads(req.text)
        
    
    def delete(self, username, doc_id):
        url = URL_FILE + "/" + username + "/" + doc_id
        req = requests.delete(url, headers = {"Authorization" : "token " + self.token}, verify = "file.crt")
        ind = req.text.find("\"error code\": ")
        if ind > 0:
            error = req.text[ind+14:ind+17]
            if error == "404":
                raise exceptions.NonExistingFile
            if error == "401":
                raise exceptions.NonExistingAuthorization

        return json.loads(req.text)

@api.resource("/<string:username>/_all_docs", methods=["GET"])
class AllDocuments(Resource):
    
    def __init__(self):
        super().__init__()
        self.authorization, self.token = get_authorization()
    
    def get(self, username):
        url = URL_FILE + "/" + username + "/_all_docs"
        req = requests.get(url, headers = {"Authorization" : "token " + self.token}, verify = "file.crt")
        ind = req.text.find("\"error code\": ")
        if ind > 0:
            error = req.text[ind+14:ind+17]
            if error == "401":
                raise exceptions.NonExistingAuthorization
        print(req.json())
        return req.json()

if __name__ == '__main__':
    app.run(debug=True, port = 5000, ssl_context=("broker.crt", "broker.key"))
