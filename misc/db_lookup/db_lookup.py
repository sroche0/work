__author__ = 'sroche'

"""
Given a list of email address, find organization name for each email address.

"""

import sys
import os
import csv

sys.path.append("/usr/share/pyshared")
from sqlalchemy import create_engine
from sqlalchemy import exc as dbException
# from sqlalchemy.sql import text


class FindOrgs(object):

    # Modify these to match your database connection parameters.
    DB_NAME = 'db_name'
    DB_USER = 'db_user'
    DB_PASSWORD = 'password'
    DB_HOST = 'host_url'

    def __init__(self):
        self.filename = 'dll_user_ids.csv'
        self.engine = self._get_alchemy_engine()
        self.data = self.parse_file()
        data = self.find_orgs()
        self.display(data)
    # end __init__

    def display(self, data):
        with open('dll_user_ids.csv', 'wb') as f:
            writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)

    def parse_file(self):
        user_list = []
        with open(self.filename, 'rb') as f:
            contents = csv.reader(f, delimiter=',', quotechar='"')
            for row in contents:
                user_list.append(row)

        return user_list

    def find_orgs(self):
        master_data = []
        try:
            for i in self.data:
                sql = """SELECT psk, FROM accounts.user WHERE lower("email") = '%s'""" % i
                print sql
                result = self.engine.execute(sql)

                for row in result:
                    data = [row['psk'], i]
                    master_data.append(data)
                result.close()
            return master_data

        except dbException.ProgrammingError, err:
            show_errors([str(err)])
    # end find_orgs

    def _get_alchemy_engine(self):
        dialect = 'postgresql'
        driver = 'psycopg2'
        user = FindOrgs.DB_USER
        password = FindOrgs.DB_PASSWORD
        host = FindOrgs.DB_HOST
        dbname = FindOrgs.DB_NAME

        uri = '%s+%s://%s:%s@%s/%s' % (dialect, driver, user, password, host, dbname)
        return create_engine(uri)
# end class


def show_usage():
    print('\n    Usage: ./find_orgs_by_email /path/to/email_list.txt\n')
    exit(1)


def show_errors(errors):
    print('')
    for error in errors:
        print('    Error: %s' % error)
    print('')
    exit(2)


def main():
    arg_count = len(sys.argv)

    if arg_count != 2:
        pass
        # show_usage()

    else:
        filename = sys.argv[1]

        if not os.path.exists(filename):
            show_errors(['Cannot find filename: "%s"' % filename])

        # no user syntax errors, so execute
        FindOrgs()

if __name__ == "__main__":
    main()
    exit(0)
