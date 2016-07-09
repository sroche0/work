import logging
import os
import sys
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
            print 'To set default values, edit config.json in app directory'
            os.makedirs(self.app_path)

        if not os.path.exists('{}/config.json'.format(self.app_path)):
            with open('{}/config.json'.format(self.app_path), 'wb') as f:
                example = {'ease_admin': '',
                           'jenkins_user': '',
                           }
                f.write(json.dumps(example, indent=2, separators=(',', ': ')))

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

    @staticmethod
    def status_print(message):
        sys.stdout.write(message.ljust(30, '.'))
        sys.stdout.flush()
