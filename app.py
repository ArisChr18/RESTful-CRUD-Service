# Importing libraries
from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from google.cloud import firestore
import hashlib
import os


# Database connection and app initialisation
db = firestore.Client()
app = Flask(__name__)
api = Api(app)


# Defining error if account don't exist
def abort_if_account_doesnt_exist(accountid): # accountid is determined by the GCLOUD_PROJECT environment variable
    accounts_ref = db.collection('Accounts')
    ref = accounts_ref.where(u'accountid', u'==', accountid)
    if not ref:
        abort(404, message="Account {} doesn't exist".format(accountid))


# Parsing fields
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('email')
parser.add_argument('password')


# Creating a class for Accounts format and hashing password
class Account(object):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email

        # Hashing password
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100)
        
        self.password = salt + key
        self.password = str(self.password)

    def to_dict(self):
        account = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        return account

    def __repr__(self):
        return 'Account(username={}, email={}, password={})'.format(self.username, self.email, self.password)


# Class for defining GET and POST functions
class AccountList(Resource):

    # GET function that gets all accounts
    def get(self):
        accounts_ref = db.collection('Accounts')
        docs = accounts_ref.stream()
        accounts = {}
        for doc in docs:
            accounts[doc.id]= doc.to_dict()
        return accounts

    # POST function
    def post(self):
        args = parser.parse_args()
        account = Account(username=args['username'], email=args['email'], password=args['password'])
        db.collection('Accounts').add(account.to_dict())
        return account.to_dict(), 201


# Class for defining GET(by ID), PUT and DELETE functions
class AccountListById(Resource):

    # GET function that gets account by ID
    def get(self, accountid):
        doc_ref = db.collection('Accounts').document(accountid)
        if doc_ref:
            return doc_ref.get().to_dict()
        return abort_if_account_doesnt_exist(accountid)

    # PUT function
    def put(self, accountid):
        args = parser.parse_args()
        accounts_ref = db.collection('Accounts')
        accounts_ref.document(accountid).update({"username": args['username'], "email": args['email']})
        return True, 201

    # DELETE function
    def delete(self, accountid):
        accounts_ref = db.collection('Accounts')
        accounts_ref.document(accountid).delete()
        return True, 201


# URL path for accounts list
api.add_resource(AccountList, '/accounts')
# URL path for accounts list by ID
api.add_resource(AccountListById, '/accounts/<accountid>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)