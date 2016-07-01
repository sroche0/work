__author__ = 'sroche'
import ast
import json
from subprocess import check_output

import requests

import endpoints


class Ease:
    def __init__(self, region):
        self.payload = {"id": 1, "apiVersion": "1.0", "method": "", "params": '', "jsonrpc": "2.0"}
        self.headers = {"Content-Type": "application/js"}
        self.token, self.trans_id, self.file_id = '', '', ''
        self.php_url = endpoints.URLs[region]['PHP Web Services']
        self.py_url = endpoints.URLs[region]['Python Web Services']
        self.up_url = endpoints.URLs[region]['File Uploader']

    def php_auth(self, user, password):
        """
        :rtype : basestring
        :param user: Admin username
        :param password: Admin password
        """
        self.payload['method'] = "com.apperian.eas.user.authenticateuser"
        self.payload['params'] = {"email": user, "password": password}

        r = requests.post(self.php_url, data=json.dumps(self.payload), headers=self.headers).json()

        token = r.get('result', {}).get('token')
        if token:
            print 'Authenticated'
            self.token = token
            return True
        else:
            print 'Authentication Failed.'
            return False

    def py_auth(self, user, password):
        """
        :rtype : basestring
        :param user: Username
        :param password: Password
        :return: Authentication Token
        """
        headers = {"Content-Type": "application/json"}
        payload = {'user_id': user,
                   'password': password}
        url = '%s/users/authenticate/' % self.py_url

        r = requests.post(url, data=json.dumps(payload), headers=headers).json()
        token = r.get('token')

        if token:
            print 'Authenticated'
            self.token = token
            return True
        else:
            print 'Authentication Failed.'
            return False

    def create(self):
        """
        Creates an entry in EASE for the publishing API to upload a file to.
        Uses a token from the php_auth function
        :return: Returns transaction ID
        """
        self.payload['method'] = "com.apperian.eas.apps.create"
        self.payload['params'] = {"token": self.token}

        r = requests.post(self.php_url, data=json.dumps(self.payload), headers=self.headers).json()
        trans_id = r.get('result', {}).get('transactionID')
        if trans_id:
            self.trans_id = trans_id
        else:
            print 'Failed to create entry'
            exit()

    def upload(self, file_name):
        """
        :param file_name: File name to upload. Must exist in CWD
        :return: returns fileID for the publish step
        """
        print '*' * 80
        up_key = 'LUuploadFile=@%s' % file_name
        url = '%s/upload?transactionID=%s' % (self.up_url, self.trans_id)
        file_id = ast.literal_eval(check_output(['curl', '--form', up_key, url]))
        print '*' * 80
        file_id = file_id['fileID']
        if file_id:
            self.file_id = file_id
            return True
        else:
            print 'File Upload Failed'
            print 'check upload command: curl --form', up_key, url
            exit(3)

    def publish(self, data):
        """
        :param data: Dict of the metadata that is required to upload to ease.
        :return: Returns appID
        """
        self.payload['method'] = 'com.apperian.eas.apps.publish'
        self.payload['params'] = {
            "EASEmetadata": data,
            "files": {"application": self.file_id},
            "token": self.token,
            "transactionID": self.trans_id}

        r = requests.post(self.php_url, data=json.dumps(self.payload), headers=self.headers).json()

        app_id = r.get('result', {}).get('appID')
        if app_id:
            return app_id
        else:
            print r
            exit()

    def delete_org(self, psk):
        """
        :param psk: psk of the organization to be deleted
        :return: returns "success", "auth", or the error message
        """
        headers = {'X-TOKEN': self.token}
        url = '%s/organizations/%s' % (self.py_url, psk)

        r = requests.delete(url, headers=headers).json()
        deleted = r.get('deleted_organization')
        message = r.get('error', {}).get('message')

        if deleted:
            print 'Deleted org %s' % psk
            return 'success'
        elif message == 'Missing token or session expired':
            print 'Missing token or session expired'
            return 'auth'
        else:
            return message

    def users_delete(self, psk):
        """
        :param psk: psk of the user to be deleted
        :return: returns "success", "auth", or the error message
        """
        headers = {'X-TOKEN': self.token}
        url = '%s/users/%s' % (self.py_url, psk)

        r = requests.delete(url, headers=headers).json()
        deleted = r.get('delete_user_response')
        message = r.get('error', {}).get('message')

        if deleted:
            return 'success'
        elif message == 'Missing token or session expired':
            return 'auth'
        else:
            return message

    def users_list(self):
        headers = {'X-TOKEN': self.token}
        url = '%s/users' % self.py_url

        r = requests.get(url, headers=headers).json()
        return r['users']