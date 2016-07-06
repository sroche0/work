import logging
import os
import getpass
import csv
import datetime
import json


class AdminUtilBase:
    def __init__(self, app_path):
        self.success = []
        self.failed = []
        self.psks = []
        self.app_path = app_path
        self.today = datetime.date.today()
        self.application_init()
        self.logging_init()

    def logging_init(self):
        cwd = os.getcwd()

        os.chdir(self.app_path)
        log_files = sorted([x for x in os.listdir('.') if '.log' in x], key=os.path.getctime)

        if len(log_files) > 4:
            os.remove(log_files[0])

        logging.basicConfig(filename='{}.log'.format(self.today),
                            filemode='a',
                            format="[%(levelname)8s] %(message)s",
                            level=logging.DEBUG
                            )

        logging.info('=' * 80)
        logging.info('New Run'.center(80))
        logging.info('=' * 80)

        os.chdir(cwd)

    def application_init(self):
        if not os.path.exists(self.app_path):
            print 'First time run detected, creating app directory at {}'.format(self.app_path)
            print 'To set default credentials, rename config.json.example to config.json and set values accordingly'
            os.makedirs(self.app_path)
            with open('{}/config.json.example'.format(self.app_path), 'wb') as f:
                example = {'username': 'user@example.com', 'password': 'password'}
                f.write(json.dumps(example, indent=4, separators=(',', ': ')))

    def log_results(self):
        if self.failed:
            print '{} failed. Check {}/failed_{}.csv for details\n'.format(len(self.failed), self.app_path, self.today)
            with open('{}/failed_{}.csv'.format(self.app_path, self.today), 'wb') as f:
                writer = csv.writer(f)
                writer.writerows(self.failed)

        if self.success:
            with open('{}/deleted_master.csv'.format(self.app_path), 'ab') as f:
                writer = csv.writer(f)
                writer.writerows(self.success)
            with open('{}/deleted_{}.csv'.format(self.app_path, self.today), 'ab') as f:
                writer = csv.writer(f)
                writer.writerows(self.success)

    def authenticate(self):
        count = 0
        while self.ease.status != 200 and count < 3:
            count += 1
            user = raw_input('Username > ')
            pw = getpass.getpass('Password > ')
            self.ease.auth(user, pw)

            if self.ease.status != 200:
                if count < 3:
                    print 'Unable to authenticate, enter credentials again\n'
                else:
                    exit('Failed attempts exceeded, check your credentials')