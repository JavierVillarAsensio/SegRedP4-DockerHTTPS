#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api
from secrets import token_urlsafe, token_hex
from hashlib import pbkdf2_hmac
import os
from threading import Timer

import exceptions

app = Flask(__name__)
api = Api(app, errors=exceptions.HTTPS_ERROR)
app.config['SERVER_NAME'] = 'auth.local:5000'
active_tokens = {}
ROOT = "users/"


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

def find_user(username):
    with open('credentials.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if username == line.split(":")[0]:
                return line
    return ''

def expire_token(token):
    active_tokens.pop(token)

def create_hash(salt, text):
    return pbkdf2_hmac('sha512', text.encode(), salt.encode(), 10000)

@api.resource("/signup", methods=["POST"])
class Signup(Resource):
    def post(self):
        username, password = sort_args("username", "password")
        if not username or not password:
            raise exceptions.WrongFormat

        if find_user(username):
            raise exceptions.UserAlreadyExists
        self.add_credential(username, password)
        token = token_urlsafe(32)
        active_tokens[token] = username

        Timer(300.0, expire_token, [token]).start()
        return {'access_token': token}


    def add_credential(self, username, password):
        with open('credentials.txt', 'a') as f:
            salt = token_hex(8)
            password_hash = create_hash(salt, password)

            new_credential = username + ":$6$" + salt + "$" + password_hash.hex() + "\n"
            f.write(new_credential)



@api.resource("/login", methods=["POST"])
class Login(Resource):
    def post(self):
        username, password = sort_args("username", "password")
        credential = find_user(username)

        if not username or not password:
            raise exceptions.WrongFormat

        if not credential:
            raise exceptions.NonExistingUser
  
        if not self.check_password(credential, password):
            raise exceptions.WrongPassword

        token = token_urlsafe(32)
        active_tokens[token] = username

        Timer(300.0, expire_token, [token]).start()
        return {'access_token': token}


    def check_password(self, credential, password):
        splited = credential.split("$")
        salt = splited[2]
        hash_password = splited[3].strip()

        password_hash = create_hash(salt, password)

        return hash_password == password_hash.hex()

@api.resource("/check_user/<string:username>/<string:token>", methods=["GET"])
class Check(Resource):
    def get(self, username, token):
        if active_tokens.get(token) != username:
            raise exceptions.UnauthorizedToken()
        return "authorized"

if __name__ == '__main__':
    app.run(debug=True, port = 5000, ssl_context=("auth.crt", "auth.key"))
