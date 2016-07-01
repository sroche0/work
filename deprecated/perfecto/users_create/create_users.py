#########################
# !/usr/bin/python2.7
# encoding: utf-8
# Author: sroche0@gmail.com
# Date: 07/02/2015
#########################
try:
    import requests
except ImportError(requests):
    print 'Python module "requests" is required to run this script. See http://docs.python-requests.org/en/latest/ ' \
          'for installation instructions'
    print 'Exiting...'
    exit()
import csv
import argparse

ADMIN_USERNAME = ''
ADMIN_PASSWORD = ''
ROLES = 'QSP_GENERAL'
CLOUD = None

parser = argparse.ArgumentParser(
    prog='Bulk User Creation',
    usage='python create_users.py --user ADMIN_USER --pass, ADMIN_PASSWORD --roles ADMINISTRATOR,Other_role,ETC '
          '--cloud BASE_CLOUD_URL '
          '\n\nAll parameters are optional. Roles set in the user_data.csv for each user will '
          '\noverride values passed via --roles. To avoid setting user and password at runtime, '
          '\nedit the default values in the script itself. Current defaults are:'
          '\n    User - {}'
          '\n    Password - {}'
          '\n    Roles - {}'
          '\n    Cloud - {}'.format(ADMIN_USERNAME, ADMIN_PASSWORD, ROLES, CLOUD))

parser.add_argument('--cloud', default=CLOUD, help='Base URL for cloud. EX: https://mobilecloud.perfectomobile.com')
parser.add_argument('--roles', default=ROLES, help='If passing multiple roles separate with commas')
parser.add_argument('--user', default=ADMIN_USERNAME, help='Must be an admin on the target cloud')
parser.add_argument('--password', default=ADMIN_PASSWORD)


def main():
    args = parser.parse_args()
    info = {'admin_u': args.user,
            'admin_pw': args.password,
            'user_data': 'user_data.csv',
            'roles': args.roles}

    if args.cloud:
        clouds = list(args.cloud)
    else:
        with open('cloud_data.txt', 'rb') as f:
            clouds = []
            for row in f:
                clouds.append(row.rstrip())

    with open(info['user_data'], 'rb') as f:
        users = []
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)

    failed, count, progress = [], 0, 0
    total = len(clouds) * len(users)
    for cloud in clouds:
        for user in users:
            count += 1
            info.update(cloud)
            info.update(user)
            url = '%(cloud)s/services/users?operation=create&user=%(admin_u)s&password=%(admin_pw)s&email=%(email)s' \
                  '&userPassword=%(password)s&firstName=%(firstname)s&lastName=%(lastname)s&roles=%(roles)s' \
                  '&account.unlimited=true&companyName=%(company)s&sendNotification=True'.format(info)

            try:
                r = requests.get(url)
                if r.ok:
                    pass
                else:
                    failed.append([info['cloud'], info['email'], '{} Error'.format(str(r.status_code))])
            except requests.ConnectionError:
                failed.append([info['cloud'], info['email'], requests.ConnectionError])

            if progress != (float(count) / float(total)) * 100:
                progress = int((float(count) / float(total)) * 100)
                print '{}% Completed'.format(progress)

    if failed:
        print '%d users failed to create. Check failed.csv for details\n' % len(failed)

        with open('failed.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(failed)

if __name__ == '__main__':
    main()
