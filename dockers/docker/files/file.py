#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api
from secrets import token_urlsafe, token_hex
from hashlib import pbkdf2_hmac
import json
import os
import requests

import exceptions

app = Flask(__name__)
api = Api(app, errors=exceptions.HTTPS_ERROR)
app.config['SERVER_NAME'] = 'file.local:5000'
ROOT = "users/"
URL = 'https://auth.local:5000'

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

def check_user(username, token):
    url = URL + "/check_user/" + username + "/" + token
    req = requests.get(url, verify = "auth.crt")
    ind = req.text.find("\"error code\": ")
    if ind > 0:
        error = req.text[ind+14:ind+17]
        if error == "401":
            raise exceptions.UnauthorizedToken

@api.resource("/<string:username>/<string:doc_id>", methods=["GET", "POST", "PUT", "DELETE"])
class UserDocuments(Resource):
    
    def __init__(self):
        super().__init__()
        self.authorization, self.token = get_authorization()

    def get(self, username, doc_id):
        check_user(username, self.token)
        path = f"{ROOT}{username}/{doc_id}"
        
        self.exists(path)

        with open(path) as f:
            doc_data = json.load(f)

        return doc_data


    def post(self, username, doc_id):
        check_user(username, self.token)
        content = self.check_data()
        print(content)
        path = f"{ROOT}{username}/{doc_id}"

        if os.path.isfile(path):
            raise exceptions.FileAlreadyExists

        if not os.path.isdir(ROOT + username):
            os.mkdir(ROOT + username)
        self.write_file(path, content)

        return {"size": os.path.getsize(path)}


    def put(self, username, doc_id):
        check_user(username, self.token)
        data = self.check_data()
        print(data)
        path = f"{ROOT}{username}/{doc_id}"
        
        self.exists(path)
        self.write_file(path, data)

        return {"size": os.path.getsize(path)}
        
    
    def delete(self, username, doc_id):
        check_user(username, self.token)
        path = f"{ROOT}{username}/{doc_id}"
        self.exists(path)
        os.remove(path)
        return {}

    def write_file(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f)

    def exists(self, path):
        if not os.path.isfile(path):
            raise exceptions.NonExistingFile


    def check_data(self):
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


@api.resource("/<string:username>/_all_docs", methods=["GET"])
class AllDocuments(Resource):
    
    def __init__(self):
        super().__init__()
        self.authorization, self.token = get_authorization()

    
    
    
    def get(self, username):
        check_user(username, self.token)
        data = {}
        path = f"{ROOT}{username}"

        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        for file in files:
            with open(f"{path}/{file}", "r") as f:
                data.update({file:json.load(f)})

        return data

if __name__ == '__main__':
    app.run(debug=True, port = 5000, ssl_context=("file.crt", "file.key"))
